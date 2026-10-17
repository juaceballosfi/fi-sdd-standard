#!/usr/bin/env python3
"""Deterministic inventory of a repository for /project-context (fi-sdd-standard).

Usage (from the repository root):
    python inventory.py [--root .] [--out <file.md>] [--endpoints <file.md>]

It reads manifests and configuration only (never secrets: no appsettings values, no .env values)
and prints a Markdown report with the source file of every fact:
.NET solutions and projects, Node packages and lockfiles, CI pipelines, Docker, submodules,
existing documentation (docs/, DocFX), translation files, tests, Entity Framework, existing AI
configuration (AGENTS.md, CLAUDE.md, .claude/, .github/) and, with --endpoints, the REST endpoints
read from ASP.NET controllers. Everything is best effort: the skill confirms what matters.

It also writes the environment preflight (local SDK and Node against what the repository asks for,
package manager, dependencies installed, broken links and submodules) and the secrets committed in
configuration files. For those it prints the file, the line and the key name, never the value.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

EXCLUDED = {"node_modules", "bin", "obj", ".git", "dist", "build", "_site", "TestResults", ".vs",
            "packages", "coverage", ".next", ".angular", "wwwroot", ".idea", "__pycache__"}
KEY_NODE_DEPS = ["react", "react-dom", "typescript", "antd", "i18next", "react-i18next", "react-router",
                 "react-router-dom", "mobx", "redux", "@reduxjs/toolkit", "inversify", "axios", "jest",
                 "@testing-library/react", "@testing-library/jest-dom", "vitest", "eslint", "prettier",
                 "@craco/craco", "react-scripts", "vite", "next", "husky", "stylelint", "less"]
TEST_PACKAGES = ("xunit", "nunit", "mstest", "microsoft.net.test.sdk")
I18N_NAME = re.compile(r"(^i18n.*\.(json|ts|js)$)|(\.resx$)|(\.po$)|(\.xlf$)", re.I)
BROKEN_LINKS: list[Path] = []  # filled by walk(): links or junctions whose target is missing
# Secrets committed in configuration (ADR-0028). Only key names and lines are reported.
SECRET_FILES = re.compile(r"(^appsettings.*\.json$)|(\.config$)|(^\.npmrc$)|(^launchSettings\.json$)|"
                          r"(^docker-compose.*\.ya?ml$)|(^secrets\.json$)", re.I)
SECRET_KEY = re.compile(r"(secret|password|passwd|pwd|token|apikey|api_key|accesskey|privatekey|"
                        r"licen[cs]e_?key|signature|pat)$|^(pat|sas)$|clientsecret|cleartextpassword", re.I)
SECRET_VALUE = re.compile(r"(password|pwd)\s*=\s*[^;\s\"']{3,}|accountkey\s*=|sharedaccesskey\s*=|[?&]sig=", re.I)
PLACEHOLDER = re.compile(r"^\s*$|[{}<>]|\$\(|#\{|^__|^(changeme|todo|xxx+|none|null|true|false)$", re.I)


def walk(root: Path):
    """All files under root, skipping generated and dependency folders."""
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = sorted(d.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            continue
        for p in entries:
            if os.path.lexists(p) and not p.exists():
                BROKEN_LINKS.append(p)
                continue
            if p.is_dir():
                if p.name not in EXCLUDED and not p.is_symlink():
                    stack.append(p)
            elif p.is_file():
                yield p


def read(p: Path) -> str:
    data = p.read_bytes()
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16", errors="replace")
    return data.decode("utf-8-sig", errors="replace")


def rel(p: Path, root: Path) -> str:
    return p.relative_to(root).as_posix()


def xml_values(text: str, tag: str) -> list[str]:
    return [m.strip() for m in re.findall(rf"<{tag}>([^<]+)</{tag}>", text)]


def run_version(*cmd: str) -> str | None:
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        res = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=30)
        return (res.stdout or res.stderr).strip().splitlines()[0] if res.returncode == 0 else None
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def git_lines(root: Path, *args: str) -> list[str]:
    try:
        res = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=30)
        return res.stdout.splitlines() if res.returncode == 0 else []
    except (OSError, subprocess.SubprocessError):
        return []


def major(version: str) -> str:
    m = re.search(r"(\d+)", version)
    return m.group(1) if m else ""


def environment(files: list[Path], root: Path, out: list[str]) -> None:
    """Preflight: what the repository needs against what this machine has (Step 0 of the skill)."""
    rows: list[tuple[str, str, str]] = []
    if any(f.suffix.lower() in {".sln", ".slnx", ".csproj"} for f in files):
        local = run_version("dotnet", "--version")
        g = root / "global.json"
        want = re.search(r'"version"\s*:\s*"([^"]+)"', read(g)) if g.exists() else None
        tfms = sorted({m for f in files if f.suffix.lower() == ".csproj"
                       for m in re.findall(r"<TargetFrameworks?>([^<]+)<", read(f))})
        need = want.group(1) if want else ("framework " + ", ".join(tfms) if tfms else "—")
        if not local:
            rows.append(("✗", "SDK de .NET", f"no está instalado (el repositorio pide {need})"))
        elif want and major(local) != major(want.group(1)):
            rows.append(("⚠", "SDK de .NET", f"local {local}; global.json pide {want.group(1)}"))
        else:
            rows.append(("✓", "SDK de .NET", f"local {local}; el repositorio pide {need}"))
        for cfg in (f for f in files if f.name.lower() == "nuget.config"):
            sources = re.findall(r'<add\s+key="([^"]+)"\s+value="(https?://[^"]+)"', read(cfg))
            private = [k for k, url in sources if "nuget.org" not in url]
            if private:
                rows.append(("·", "NuGet", f"`{rel(cfg, root)}` usa orígenes privados ({', '.join(private)}): "
                             "dotnet restore comprueba las credenciales (Paso 0)"))
    for pkg in (f for f in files if f.name == "package.json"):
        d = pkg.parent
        try:
            data = json.loads(read(pkg))
        except json.JSONDecodeError:
            continue
        want = next((read(f).strip() for f in (d / ".nvmrc", d / ".node-version") if f.exists()), None)
        want = want or (data.get("engines") or {}).get("node")
        local = run_version("node", "--version")
        where = rel(d, root) or "."
        if not local:
            rows.append(("✗", f"Node ({where})", f"no está instalado (pide {want or 'sin versión fijada'})"))
        elif want and major(want) and major(want) != major(local):
            rows.append(("⚠", f"Node ({where})", f"local {local}; el repositorio pide {want}: usa esa versión (nvm)"))
        else:
            rows.append(("✓", f"Node ({where})", f"local {local}" + (f"; pide {want}" if want else "")))
        locks = {"yarn.lock": "yarn", "package-lock.json": "npm", "pnpm-lock.yaml": "pnpm"}
        manager = next((m for lock, m in locks.items() if (d / lock).exists()), None)
        if manager and not shutil.which(manager):
            rows.append(("✗", f"{manager} ({where})", "el lockfile lo pide y no está instalado"))
        if not (d / "node_modules").is_dir():
            rows.append(("⚠", f"dependencias ({where})", "sin node_modules: se instalan en el Paso 3 si lo apruebas"))
    for link in BROKEN_LINKS:
        rows.append(("✗", "enlace roto", f"`{rel(link, root)}` apunta a una ruta que no existe"))
    for line in git_lines(root, "ls-files", "-s"):
        mode, _, rest = line.partition(" ")
        path = rest.split("\t", 1)[-1] if "\t" in rest else ""
        p = root / path
        if mode == "120000" and path and p.is_file() and not p.is_symlink() and p.stat().st_size < 512:
            rows.append(("✗", "enlace de git", f"`{path}` es un enlace simbólico en git y aquí es un archivo de texto: "
                         "créalo (Windows: mklink /J, o git config core.symlinks true y vuelve a hacer checkout)"))
    gm = root / ".gitmodules"
    if gm.exists():
        for path in re.findall(r"path\s*=\s*(\S+)", read(gm)):
            p = root / path
            if not p.is_dir() or not any(p.iterdir()):
                rows.append(("✗", "submódulo", f"`{path}` está vacío: git submodule update --init --recursive"))
    if not rows:
        return
    out.append("## Entorno (preflight)\n")
    out.append("| | Qué | Detalle |\n| --- | --- | --- |")
    out.extend(f"| {m} | {w} | {d} |" for m, w, d in rows)
    out.append("\n✗ = bloquea el Paso 3 (lo arregla una persona; la sesión no toca credenciales ni la "
               "configuración del sistema) · ⚠ = se registra y, si hay que arreglarlo, va a un borrador\n")


def committed_secrets(files: list[Path], root: Path, out: list[str]) -> None:
    """Secret-looking keys with a real value in versioned configuration files. Never prints values."""
    tracked = set(git_lines(root, "ls-files"))
    hits: list[tuple[str, int, str]] = []
    for f in files:
        path = rel(f, root)
        if not SECRET_FILES.search(f.name) or (tracked and path not in tracked):
            continue
        for n, line in enumerate(read(f).splitlines(), 1):
            pairs = re.findall(r'"([\w.:$-]+)"\s*:\s*"([^"]*)"', line)
            pairs += re.findall(r'<add\s+key="([^"]+)"\s+value="([^"]*)"', line, re.I)
            pairs += re.findall(r"^\s*([\w:/.@-]*_(?:authToken|password))\s*=\s*(\S+)", line)
            if f.suffix.lower() in {".yml", ".yaml"}:
                pairs += re.findall(r"^\s*-?\s*([\w.-]+)\s*[:=]\s*[\"']?([^\"'\s#]+)", line)
            for key, value in pairs:
                name = key.rsplit(":", 1)[-1].rsplit("/", 1)[-1]
                by_key = SECRET_KEY.search(name) and len(value) >= 8 and not PLACEHOLDER.search(value) \
                    and not value.lower().startswith(("http://", "https://"))
                if by_key or SECRET_VALUE.search(value):
                    hits.append((path, n, name))
    if not hits:
        return
    out.append("## Secretos versionados\n")
    out.append("Claves con aspecto de secreto y un valor real, en archivos que git versiona. "
               "Solo se listan el archivo, la línea y la clave: el valor no se lee ni se copia.\n")
    out.append("| Archivo:línea | Clave |\n| --- | --- |")
    out.extend(f"| `{p}:{n}` | `{k}` |" for p, n, k in hits)
    out.append("\nCada archivo va a `secrets` de `sdd-guardrails.json` y cada secreto a un borrador **Urgente** "
               "(rotarlo y sacarlo del repositorio), sin el valor.\n")


def dotnet(files: list[Path], root: Path, out: list[str]) -> dict:
    slns = [f for f in files if f.suffix.lower() in {".sln", ".slnx"}]
    projs = [f for f in files if f.suffix.lower() == ".csproj"]
    info = {"test_projects": [], "projects": []}
    if not slns and not projs:
        return info
    out.append("## .NET\n")
    for s in slns:
        out.append(f"- Solución: `{rel(s, root)}`")
    for name in ("global.json", "Directory.Build.props", "Directory.Packages.props", "nuget.config", ".editorconfig"):
        f = root / name
        if f.exists():
            extra = ""
            if name == "global.json":
                m = re.search(r'"version"\s*:\s*"([^"]+)"', read(f))
                extra = f" (SDK {m.group(1)})" if m else ""
            if name == "Directory.Packages.props":
                extra = " (versiones centralizadas: los paquetes se versionan aquí)"
            out.append(f"- `{name}`{extra}")
    central = {}
    cpm = root / "Directory.Packages.props"
    if cpm.exists():
        central = dict(re.findall(r'<PackageVersion\s+Include="([^"]+)"\s+Version="([^"]+)"', read(cpm)))
    out.append("\n| Proyecto | SDK | Framework | Tipo | Referencias a proyectos | Paquetes clave |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for p in projs:
        t = read(p)
        sdk = (re.search(r'<Project\s+Sdk="([^"]+)"', t) or [None, "—"])[1]
        tfm = ", ".join(xml_values(t, "TargetFramework") + xml_values(t, "TargetFrameworks")) or "—"
        pkgs = re.findall(r'<PackageReference\s+Include="([^"]+)"(?:\s+Version="([^"]+)")?', t)
        names = [n for n, _ in pkgs]
        is_test = "true" in [v.lower() for v in xml_values(t, "IsTestProject")] or any(
            n.lower().startswith(TEST_PACKAGES) for n in names)
        kind = "pruebas" if is_test else (xml_values(t, "OutputType") or ["web" if "Web" in sdk else "biblioteca"])[0]
        refs = [Path(r.replace("\\", "/")).stem for r in re.findall(r'<ProjectReference\s+Include="([^"]+)"', t)]
        key = [f"{n} {v or central.get(n, '')}".strip() for n, v in pkgs if re.match(
            r"(Microsoft\.EntityFrameworkCore(\.SqlServer)?|Hangfire\.Core|MediatR|AutoMapper|xunit(\.v3)?|Moq|NSubstitute|"
            r"FluentAssertions|Serilog|Swashbuckle.*|Microsoft\.AspNetCore\.SpaServices.*|docfx.*)$", n, re.I)]
        out.append(f"| `{rel(p, root)}` | {sdk} | {tfm} | {kind} | {', '.join(refs) or '—'} | {', '.join(key[:8]) or '—'} |")
        info["projects"].append(rel(p, root))
        if is_test:
            info["test_projects"].append(rel(p, root))
    if not info["test_projects"]:
        out.append("\n**⚠ No hay ningún proyecto de pruebas .NET.**")
    out.append("")
    return info


def node(files: list[Path], root: Path, out: list[str]) -> None:
    pkgs = [f for f in files if f.name == "package.json"]
    if not pkgs:
        return
    out.append("## Node / frontend\n")
    for p in pkgs:
        try:
            data = json.loads(read(p))
        except json.JSONDecodeError:
            out.append(f"- `{rel(p, root)}`: JSON no válido")
            continue
        d = p.parent
        locks = [n for n in ("yarn.lock", "package-lock.json", "pnpm-lock.yaml") if (d / n).exists()]
        manager = {"yarn.lock": "yarn", "package-lock.json": "npm", "pnpm-lock.yaml": "pnpm"}
        out.append(f"### `{rel(p, root)}`\n")
        if data.get("packageManager"):
            out.append(f"- `packageManager`: {data['packageManager']}")
        if len(locks) > 1:
            out.append(f"- **⚠ Varios archivos de bloqueo:** {', '.join(locks)}. Decide cuál vale (mira el pipeline)")
        elif locks:
            out.append(f"- Gestor: **{manager[locks[0]]}** (`{locks[0]}`)")
        else:
            out.append("- Sin archivo de bloqueo")
        for n in (".nvmrc", ".node-version"):
            for f in (d / n, d / "src" / n):
                if f.exists():
                    out.append(f"- Node: `{read(f).strip()}` ({rel(f, root)})")
        if data.get("engines"):
            out.append(f"- `engines`: {json.dumps(data['engines'])}")
        scripts = data.get("scripts", {})
        if scripts:
            out.append("- Scripts:")
            for k, v in scripts.items():
                out.append(f"  - `{k}`: `{v}`")
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        key = [f"{k} {deps[k]}" for k in KEY_NODE_DEPS if k in deps]
        if key:
            out.append(f"- Dependencias clave: {', '.join(key)}")
        if "@testing-library/react" not in deps:
            out.append("- Sin `@testing-library/react`: los componentes no tienen pruebas unitarias")
        tsconfig = d / "tsconfig.json"
        if tsconfig.exists():
            t = read(tsconfig)
            flags = [f for f in ("strict", "ignoreDeprecations", "noEmit", "skipLibCheck") if f in t]
            out.append(f"- `tsconfig.json`: {', '.join(flags) or 'sin opciones destacadas'}")
        tests = [f for f in files if d in f.parents and re.search(r"\.(test|spec)\.(t|j)sx?$", f.name)]
        if tests:
            dirs = sorted({rel(f.parent, root) for f in tests})
            out.append(f"- Pruebas: {len(tests)} archivo(s) en {', '.join(dirs[:5])}{' …' if len(dirs) > 5 else ''}")
        else:
            out.append("- Pruebas: ninguna")
        for cfg in ("craco.config.js", "vite.config.ts", "vite.config.js", ".eslintrc", ".eslintrc.js", ".eslintrc.json",
                    ".prettierrc", ".stylelintrc.json", ".husky"):
            if (d / cfg).exists():
                out.append(f"- `{cfg}`")
        out.append("")


def ci(files: list[Path], root: Path, out: list[str]) -> None:
    pipes = [f for f in files if re.search(r"(azure-pipelines.*|.*pipelines?.*)\.ya?ml$", f.name, re.I)
             or ".github/workflows/" in rel(f, root)]
    if not pipes:
        out.append("## CI\n\n- Sin pipelines\n")
        return
    out.append("## CI\n")
    for p in pipes:
        t = read(p)
        out.append(f"### `{rel(p, root)}`\n")
        if "trigger" in t:
            block = re.search(r"trigger:[ \t]*\n((?:[ \t-].*\n){1,20})", t)
            if block:
                out.append("- Trigger: " + " ".join(l.strip() for l in block.group(1).splitlines() if l.strip())[:300])
        cmds = []
        for line in t.splitlines():
            s = line.strip().lstrip("- ").strip()
            if re.match(r"^(script:|bash:|pwsh:|powershell:|command:|arguments:|projects:)?\s*['\"]?"
                        r"(dotnet|yarn|npm|pnpm|npx|docker|kubectl|helm|bash|sh|\./)\b", s) or s.startswith(
                    ("task: DotNetCoreCLI", "task: Npm", "task: Docker", "command:", "projects:")):
                cmds.append(s[:160])
        for c in list(dict.fromkeys(cmds))[:25]:
            out.append(f"- `{c}`")
        versions = re.findall(r"(?:versionSpec|version|node-version|dotnet-version)\s*:\s*['\"]?([\w.x*-]+)", t)
        tools = re.findall(r"task:\s*(NodeTool@\d+|UseDotNet@\d+|UseNode@\d+)", t)
        if versions or tools:
            out.append(f"- Versiones en CI: {', '.join(tools)} {', '.join(dict.fromkeys(versions))}".rstrip())
        out.append("")


def misc(files: list[Path], root: Path, out: list[str]) -> None:
    out.append("## Ejecución local, contenedores y submódulos\n")
    start = len(out)
    for f in files:
        if f.name.lower() in {"dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml"}:
            line = f"- `{rel(f, root)}`"
            if "compose" in f.name.lower():
                services = re.findall(r"^  ([\w-]+):\s*$", read(f), re.M)
                line += f" — servicios: {', '.join(services)}" if services else ""
            out.append(line)
    gm = root / ".gitmodules"
    if gm.exists():
        for path, url in re.findall(r"path\s*=\s*(\S+)\s*\n\s*url\s*=\s*(\S+)", read(gm)):
            out.append(f"- Submódulo (ruta protegida): `{path}` ← {url.split('/')[-1]}")
    for f in files:
        if f.name.lower().startswith("appsettings") and f.suffix == ".json":
            try:
                keys = list(json.loads(read(f)).keys())
            except json.JSONDecodeError:
                keys = ["(JSON con comentarios)"]
            out.append(f"- `{rel(f, root)}`: secciones {', '.join(keys[:12])} (no se leen valores)")
        if f.name in {"launchSettings.json"}:
            urls = re.findall(r'"applicationUrl"\s*:\s*"([^"]+)"', read(f))
            out.append(f"- `{rel(f, root)}`: {', '.join(urls)}")
        if re.match(r"\.env(\..+)?$", f.name):
            out.append(f"- `{rel(f, root)}` (no se lee: puede tener secretos)")
    if len(out) == start:
        out.append("- Nada detectado")
    out.append("")


def ef(files: list[Path], root: Path, out: list[str]) -> None:
    ctx = []
    for f in files:
        if f.suffix == ".cs" and not f.name.endswith(".Designer.cs"):
            t = read(f)
            for m in re.finditer(r"class\s+(\w+)\s*(?:\([^)]*\))?\s*:\s*(?:[\w.]*\.)?(?:Identity)?DbContext\b", t):
                ctx.append(f"`{m.group(1)}` ({rel(f, root)})")
    migs = [f for f in files if f.suffix == ".cs" and "Migrations" in f.parts and re.match(r"^\d{14}_", f.name)
            and not f.name.endswith(".Designer.cs")]
    configs = [f for f in files if f.suffix == ".cs" and "IEntityTypeConfiguration<" in read(f)] if ctx else []
    if ctx or migs:
        out.append("## Datos (Entity Framework)\n")
        out.append(f"- DbContext: {', '.join(ctx) or '—'}")
        if migs:
            dirs = sorted({rel(m.parent, root) for m in migs})
            out.append(f"- Migraciones: {len(migs)} en {', '.join(dirs)} (última: {sorted(m.name for m in migs)[-1]})")
        if configs:
            out.append(f"- Configuraciones `IEntityTypeConfiguration`: {len(configs)}")
        out.append("")


def i18n(files: list[Path], root: Path, out: list[str]) -> None:
    cands = [f for f in files if I18N_NAME.search(f.name) or "locales" in f.parts]
    if not cands:
        out.append("## Traducciones\n\n- Sin archivos de traducción detectados\n")
        return
    out.append("## Traducciones\n")
    for f in cands[:20]:
        line = f"- `{rel(f, root)}` ({f.stat().st_size // 1024} KB)"
        t = read(f)
        if f.suffix == ".json":
            try:
                data = json.loads(t)
                if isinstance(data, dict):
                    langs = [k for k, v in data.items() if isinstance(v, dict) and re.fullmatch(r"[a-z]{2}(-[A-Z]{2})?", k)]
                    if langs:
                        sizes = ", ".join(f"{k}: {len(data[k])} claves" for k in langs)
                        line += f" — idiomas {sizes}"
                    elif all(isinstance(v, str) for v in list(data.values())[:50]):
                        line += f" — {len(data)} claves planas"
            except json.JSONDecodeError:
                line += " — JSON no válido o con comentarios"
        elif f.suffix in {".ts", ".js"}:
            langs = sorted(set(re.findall(r"^\s*['\"]?([a-z]{2})['\"]?\s*:\s*\{", t, re.M)))
            if langs:
                line += f" — bloques de idioma: {', '.join(langs)}"
        if "generated" in f.name.lower() or "auto-generated" in t[:400].lower() or "do not edit" in t[:400].lower():
            line += " — **parece generado: confirma si se edita a mano**"
        out.append(line)
    out.append("")


def docs(files: list[Path], root: Path, out: list[str]) -> None:
    out.append("## Documentación existente\n")
    d = root / "docs"
    if d.is_dir():
        for f in sorted(d.glob("*.md")):
            t = read(f)
            empty = "Completar con el contexto real" in t or len(t.strip().splitlines()) <= 3
            out.append(f"- `docs/{f.name}` ({len(t.splitlines())} líneas{', plantilla vacía' if empty else ''})")
        adr = d / "adr"
        if adr.is_dir():
            out.append(f"- `docs/adr/`: {len(list(adr.glob('*.md')))} archivo(s)")
    for f in files:
        if f.name == "docfx.json":
            t = read(f)
            globs = re.findall(r'"files"\s*:\s*\[([^\]]*)\]', t)
            out.append(f"- DocFX: `{rel(f, root)}` — content {'; '.join(g.strip() for g in globs)}")
    for f in (root / "README.md", root / "CHANGELOG.md", d / "CHANGELOG.md"):
        if f.exists():
            out.append(f"- `{rel(f, root)}` ({len(read(f).splitlines())} líneas)")
    out.append("")


def ai_config(root: Path, out: list[str]) -> None:
    out.append("## Configuración de IA existente\n")
    a = root / "AGENTS.md"
    if a.exists():
        t = read(a)
        kit = "<!-- sdd-kit:base:start -->" in t
        ctx = t.split("<!-- sdd-kit:base:end -->", 1)[1] if kit and "<!-- sdd-kit:base:end -->" in t else t
        heads = re.findall(r"^## (.+)$", ctx, re.M)
        out.append(f"- `AGENTS.md`: {len(t.splitlines())} líneas, bloque del kit {'sí' if kit else 'no'}; "
                   f"secciones de contexto: {', '.join(heads) or 'ninguna'}")
    c = root / "CLAUDE.md"
    if c.exists():
        t = read(c)
        out.append(f"- `CLAUDE.md`: {len(t.splitlines())} líneas"
                   + (" (solo importa `@AGENTS.md`)" if t.strip() == "@AGENTS.md" else " — **tiene contenido propio: pasarlo a AGENTS.md**"))
    for d in (root / ".claude", root / ".github"):
        if d.is_dir():
            for sub in ("agents", "skills", "hooks", "commands", "prompts", "instructions"):
                s = d / sub
                if s.is_dir():
                    items = sorted(p.name for p in s.iterdir())
                    out.append(f"- `{rel(s, root)}/`: {', '.join(items[:15])}")
            for f in ("settings.json", "copilot-instructions.md"):
                if (d / f).exists():
                    out.append(f"- `{rel(d / f, root)}`")
    kit = root / ".sdd-kit.json"
    if kit.exists():
        try:
            out.append(f"- `.sdd-kit.json`: fi-sdd-standard v{json.loads(read(kit)).get('version')}")
        except json.JSONDecodeError:
            pass
    out.append("")


ATTR = r'\[(?:[^\]"]|"[^"]*")+\]'  # an attribute, allowing "]" inside strings ("[controller]")


def endpoints(files: list[Path], root: Path) -> list[str]:
    rows = ["# Endpoints REST (leídos de los controladores)\n",
            "| Controlador | Método HTTP | Ruta | Acción | Autorización |", "| --- | --- | --- | --- | --- |"]
    attr = re.compile(r"\[(Http(Get|Post|Put|Delete|Patch))(?:\(\s*(?:template:\s*)?\"([^\"]*)\"[^)]*\))?\]")
    for f in files:
        if not (f.suffix == ".cs" and f.name.endswith("Controller.cs")):
            continue
        t = read(f)
        cls = re.search(rf"((?:{ATTR}\s*)*)public\s+(?:sealed\s+|abstract\s+|partial\s+)*class\s+(\w+)", t)
        if not cls:
            continue
        head, name = cls.group(1), cls.group(2)
        route = (re.search(r'\[Route\("([^"]*)"\)\]', head) or [None, ""])[1]
        cauth = "; ".join(re.findall(r"\[((?:Authorize\w*|AllowAnonymous)(?:\([^)]*\))?)\]", head)) or "—"
        body = t[cls.end():]
        for m in re.finditer(rf"((?:{ATTR}\s*)+)public\s+(?:async\s+)?[\w<>\[\],.? ]+\s+(\w+)\s*\(", body):
            attrs, action = m.group(1), m.group(2)
            h = attr.search(attrs)
            if not h:
                continue
            sub = h.group(3) or (re.search(r'\[Route\("([^"]*)"\)\]', attrs) or [None, ""])[1]
            path = "/".join(x for x in (route.strip("/"), sub.strip("/")) if x).replace("[controller]", name[:-10])
            mauth = "; ".join(re.findall(r"\[((?:Authorize\w*|AllowAnonymous)(?:\([^)]*\))?)\]", attrs))
            dup = " ⚠ nombre repetido" if any(f"| {action} |" in r_ and f"| {name} |" in r_ for r_ in rows) else ""
            rows.append(f"| {name} | {h.group(2).upper()} | `{path}` | {action}{dup} | {mauth or cauth} |")
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Inventario del repositorio para /project-context")
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--endpoints", type=Path, help="Escribe aquí la tabla de endpoints REST")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    root = args.root.resolve()
    files = list(walk(root))
    out = [f"# Inventario de `{root.name}`\n", "Generado por inventory.py (fi-sdd-standard). Cada dato indica su archivo.\n"]
    environment(files, root, out)
    committed_secrets(files, root, out)
    info = dotnet(files, root, out)
    node(files, root, out)
    ci(files, root, out)
    misc(files, root, out)
    ef(files, root, out)
    i18n(files, root, out)
    docs(files, root, out)
    ai_config(root, out)
    if args.endpoints:
        rows = endpoints(files, root)
        args.endpoints.write_text("\n".join(rows) + "\n", encoding="utf-8")
        out.append(f"## Endpoints\n\n- {len(rows) - 3} endpoint(s) en `{args.endpoints}`\n")
    text = "\n".join(out) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"Inventario en {args.out} ({len(text.splitlines())} líneas) · proyectos .NET: {len(info['projects'])} · "
              f"de pruebas: {len(info['test_projects'])}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
