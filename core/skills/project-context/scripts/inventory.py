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
"""
from __future__ import annotations

import argparse
import json
import re
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
