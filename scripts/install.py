#!/usr/bin/env python3
"""Install or update the fi-sdd-standard kit in a project repository (minimal version for pilots).

Usage (from the kit root):
    python scripts/install.py --target <path-to-project> [--tools copilot,claude,visualstudio] [--dry-run]

Tools:
    copilot       Skills in .agents/skills/ and prompts in .github/prompts/ (VS Code, Visual Studio,
                  Codex also read .agents/skills/). Committed to the project. Default.
    claude        Claude Code copy in .claude/skills/<skill>/ with Claude-only fields. Local: each
                  generated folder is added to .gitignore (VS Code also reads .claude/skills and
                  would show the skills twice).
    visualstudio  .github/copilot-instructions.md generated from AGENTS.md (Visual Studio does not
                  document AGENTS.md support). Local copy in .gitignore (ADR-0027). Check VS Code does
                  not load the rules twice.

Rules:
    - Never overwrites a project file. Kit-managed files (listed in .sdd-kit.json) are refreshed.
    - AGENTS.md: created if missing; if it has the kit markers, only the kit block is refreshed;
      otherwise it is left untouched and the script says what to do.
    - Agents (core/agents): only those with `status: stable` are installed (ADR-0017).
      copilot → .github/agents/<name>.agent.md (committed; VS Code and Visual Studio read it).
      claude  → .claude/agents/<name>.md (local copy with model and Claude tool names; .gitignore).
    - What is not committed (ADR-0027) goes to .gitignore: the attachments, commit-message.md and
      test-cases.csv of each work item, .claude/settings.local.json and .github/copilot-instructions.md.
      Files of that list that are already committed are reported (REVISAR), never removed.
    - The kit manual (docs/manual/) stays in the kit repository: it is never copied to a project.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
VERSION = (KIT / "VERSION").read_text(encoding="utf-8").strip()
CORE = KIT / "core"
MARK_START = "<!-- sdd-kit:base:start -->"
MARK_END = "<!-- sdd-kit:base:end -->"
CLAUDE_EXTRAS = {
    "*": {"allowed-tools": "Read Write Edit Glob Grep Bash"},
    "wbs-execution": {"model": "sonnet"},
    "project-context": {"model": "opus"},
    "quick-fix": {"model": "sonnet"},
    "test-cases": {"model": "sonnet"},
}
CLAUDE_HEADER = "# GENERATED from fi-sdd-standard by scripts/install.py - do not edit this copy\n"  # ASCII: PowerShell 5.1 shows UTF-8 without BOM as ANSI
# Neutral agent fields → tool formats (ADR-0017). Model tiers are reviewed monthly (ADR-0014).
AGENT_TOOLS_CLAUDE = {"read": ["Read", "Grep", "Glob"], "edit": ["Edit", "Write"], "execute": ["Bash"]}
AGENT_TOOLS_COPILOT = {"read": ["read", "search"], "edit": ["edit"], "execute": ["execute"]}
CLAUDE_MODEL = {"fast": "haiku", "standard": "sonnet", "reasoning": "opus"}
# Guardrails (ADR-0023): files the project versions, and what is merged into .claude/settings.json.
PROJECT_SCRIPTS = ["pr-check.py", "check-sdd-item.py", "check-encoding.py"]
DENY_RULES = [
    "Read(./.env)", "Read(./.env.*)", "Read(./**/.env)", "Read(./**/.env.*)", "Read(./**/appsettings.*.json)",
    "Read(./**/secrets.json)", "Read(./**/*.pfx)", "Read(./**/*.pem)", "Read(./**/*.key)",
    "Bash(git commit *)", "Bash(git push *)", "Bash(git push)", "Bash(git reset --hard *)", "Bash(git clean *)",
    "Bash(git branch -D *)", "Bash(rm -rf *)",
    "PowerShell(git commit *)", "PowerShell(git push *)", "PowerShell(git reset --hard *)",
    "PowerShell(Remove-Item * -Recurse *)",
]
GUARD = "${CLAUDE_PROJECT_DIR}/.agents/hooks/sdd_guard.py"
HOOKS = {
    "PreToolUse": {"matcher": "Read|Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell",
                   "hooks": [{"type": "command", "command": "python", "args": [GUARD, "pre"], "timeout": 30}]},
    "PostToolUse": {"matcher": "Edit|Write|MultiEdit",
                    "hooks": [{"type": "command", "command": "python", "args": [GUARD, "post"], "timeout": 120}]},
}


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Simple 'key: value' frontmatter (the neutral agent format) and the body."""
    if not text.startswith("---\n"):
        return {}, text
    head, body = text[4:].split("\n---\n", 1)
    fields = {}
    for line in head.splitlines():
        if line and not line.startswith((" ", "#")) and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, body.lstrip("\n")


def parse_list(value: str) -> list[str]:
    value = value.strip().strip("[]")
    return [v.strip() for v in value.split(",") if v.strip()]


class Installer:
    def __init__(self, target: Path, tools: set[str], dry_run: bool) -> None:
        self.target = target
        self.tools = tools
        self.dry = dry_run
        self.state_file = target / ".sdd-kit.json"
        self.state = json.loads(self.state_file.read_text(encoding="utf-8")) if self.state_file.exists() else {}
        self.managed: set[str] = set(self.state.get("managed", []))
        self.new_managed: set[str] = set()
        self.report: list[tuple[str, str]] = []

    # -- helpers ---------------------------------------------------------------------------------
    def rel(self, path: Path) -> str:
        return path.relative_to(self.target).as_posix()

    def log(self, action: str, what: str) -> None:
        self.report.append((action, what))

    def write(self, path: Path, content: str, managed: bool = True) -> None:
        rel = self.rel(path)
        if path.exists():
            if path.read_text(encoding="utf-8") == content:
                self.log("igual", rel)
                if managed:
                    self.new_managed.add(rel)
                return
            if rel not in self.managed:
                self.log("CONFLICTO", f"{rel} ya existe y no es del kit: no se toca")
                return
            self.log("actualizado", rel)
        else:
            self.log("creado", rel)
        if managed:
            self.new_managed.add(rel)
        if not self.dry:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")

    def copy_tree(self, src: Path, dst: Path, transform=None) -> None:
        for f in sorted(src.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc":
                text = f.read_text(encoding="utf-8")
                if transform:
                    text = transform(f, text)
                self.write(dst / f.relative_to(src), text)

    # -- steps -----------------------------------------------------------------------------------
    def skills_copilot(self) -> None:
        for skill in sorted(p for p in (CORE / "skills").iterdir() if p.is_dir()):
            self.copy_tree(skill, self.target / ".agents" / "skills" / skill.name)
        for prompt in sorted((CORE / "prompts").glob("*.prompt.md")):
            text = prompt.read_text(encoding="utf-8").replace("](../skills/", "](../../.agents/skills/")
            self.write(self.target / ".github" / "prompts" / prompt.name, text)

    def skills_claude(self) -> None:
        ignore_lines = []
        for skill in sorted(p for p in (CORE / "skills").iterdir() if p.is_dir()):
            def add_extras(f: Path, text: str, name=skill.name) -> str:
                if f.name != "SKILL.md":
                    return text
                extras = {**CLAUDE_EXTRAS["*"], **CLAUDE_EXTRAS.get(name, {})}
                lines = "".join(f"{k}: {v}\n" for k, v in extras.items())
                head, body = text.split("\n---\n", 1)
                return head.replace("---\n", "---\n" + CLAUDE_HEADER, 1) + "\n" + lines + "---\n" + body
            self.copy_tree(skill, self.target / ".claude" / "skills" / skill.name, add_extras)
            ignore_lines.append(f".claude/skills/{skill.name}/")
        self.gitignore(ignore_lines, "# fi-sdd-standard: copias locales para Claude Code")

    def agents(self) -> None:
        stable = []
        for md in sorted((CORE / "agents").glob("*.md")):
            if md.name == "README.md":
                continue
            fields, body = split_frontmatter(md.read_text(encoding="utf-8"))
            if fields.get("status") == "stable":
                stable.append((fields, body))
        ignore_lines = []
        for f, body in stable:
            name = f["name"]
            perms = parse_list(f.get("permissions", ""))
            desc = json.dumps(f["description"], ensure_ascii=False)
            if "copilot" in self.tools:
                tools = [tool for p in perms for tool in AGENT_TOOLS_COPILOT[p]]
                head = (f"---\n{CLAUDE_HEADER}name: {name}\ndescription: {desc}\n"
                        f"tools: {json.dumps(tools)}\nuser-invocable: false\n---\n")
                self.write(self.target / ".github" / "agents" / f"{name}.agent.md", head + body)
            if "claude" in self.tools:
                tools = ", ".join(tool for p in perms for tool in AGENT_TOOLS_CLAUDE[p])
                model = CLAUDE_MODEL.get(f.get("model_tier", ""), "inherit")
                head = (f"---\n{CLAUDE_HEADER}name: {name}\ndescription: {desc}\n"
                        f"tools: {tools}\nmodel: {model}\n---\n")
                self.write(self.target / ".claude" / "agents" / f"{name}.md", head + body)
                ignore_lines.append(f".claude/agents/{name}.md")
        if ignore_lines:
            self.gitignore(ignore_lines, "# fi-sdd-standard: agentes locales para Claude Code")

    def guardrails(self) -> None:
        """Hook, PR checks and the per-project guardrails config (ADR-0023)."""
        self.write(self.target / ".agents" / "hooks" / "sdd_guard.py",
                   (CORE / "hooks" / "sdd_guard.py").read_text(encoding="utf-8"))
        for name in PROJECT_SCRIPTS:
            self.write(self.target / ".agents" / "scripts" / name, (KIT / "scripts" / name).read_text(encoding="utf-8"))
        cfg = self.target / "sdd-guardrails.json"
        if cfg.exists():
            self.log("existe", "sdd-guardrails.json")
        else:
            self.write(cfg, (CORE / "templates" / "sdd-guardrails.json").read_text(encoding="utf-8"), managed=False)
            self.log("PENDIENTE", "sdd-guardrails.json: /project-context añade las rutas protegidas y los patrones")

    def claude_settings(self) -> None:
        """Merge the kit's deny rules and hooks into .claude/settings.json without touching the rest."""
        path = self.target / ".claude" / "settings.json"
        try:
            ignored = subprocess.run(["git", "-C", str(self.target), "check-ignore", "-q", "--no-index", ".claude/settings.json"],
                                     capture_output=True, timeout=10).returncode == 0
        except (OSError, subprocess.SubprocessError):
            ignored = False
        if ignored:
            self.log("REVISAR", ".gitignore ignora .claude/settings.json: añade «!.claude/settings.json» para "
                     "versionar los permisos y hooks del equipo")
        try:
            current = json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}
        except ValueError:
            self.log("REVISAR", ".claude/settings.json no es JSON válido: no se ha tocado")
            return
        settings = json.loads(json.dumps(current))
        deny = settings.setdefault("permissions", {}).setdefault("deny", [])
        added = [rule for rule in DENY_RULES if rule not in deny]
        deny.extend(added)
        hooks = settings.setdefault("hooks", {})
        for event, group in HOOKS.items():
            groups = [g for g in hooks.get(event, []) if "sdd_guard.py" not in json.dumps(g)]
            hooks[event] = groups + [group]
        if settings == current:
            self.log("igual", ".claude/settings.json")
            return
        self.log("actualizado" if path.exists() else "creado",
                 f".claude/settings.json (+{len(added)} reglas deny, hooks del kit)")
        if not self.dry:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    def gitignore(self, lines: list[str], comment: str) -> None:
        path = self.target / ".gitignore"
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        missing = [l for l in lines if l not in current.splitlines()]
        if not missing:
            return
        self.log("actualizado" if current else "creado", f".gitignore (+{len(missing)} líneas)")
        if not self.dry:
            sep = "" if current.endswith("\n") or not current else "\n"
            path.write_text(current + sep + "\n" + comment + "\n" + "\n".join(missing) + "\n", encoding="utf-8", newline="\n")

    def gitmessage(self) -> None:
        src = (CORE / "templates" / ".gitmessage").read_text(encoding="utf-8")
        dst = self.target / ".gitmessage"
        if dst.exists() and dst.read_text(encoding="utf-8").replace("\r\n", "\n") != src and ".gitmessage" not in self.managed:
            self.log("REVISAR", ".gitmessage existe y es distinto del estándar (ADR-0004): compáralos")
            return
        self.write(dst, src)

    def agents_md(self) -> None:
        base = (CORE / "AGENTS.base.md").read_text(encoding="utf-8").strip()
        block = f"{MARK_START}\n{base}\n{MARK_END}"
        path = self.target / "AGENTS.md"
        if not path.exists():
            template = (CORE / "templates" / "AGENTS.project.md").read_text(encoding="utf-8")
            start, end = template.index(MARK_START), template.index(MARK_END) + len(MARK_END)
            self.write(path, template[:start] + block + template[end:], managed=False)
            self.log("PENDIENTE", "AGENTS.md: ejecuta /project-context para escribir «Project context»")
            return
        text = path.read_text(encoding="utf-8")
        if MARK_START in text and MARK_END in text:
            start, end = text.index(MARK_START), text.index(MARK_END) + len(MARK_END)
            new = text[:start] + block + text[end:]
            if new == text:
                self.log("igual", "AGENTS.md (bloque del kit)")
            else:
                self.log("actualizado", "AGENTS.md (solo el bloque del kit)")
                if not self.dry:
                    path.write_text(new, encoding="utf-8", newline="\n")
        else:
            self.log("PENDIENTE", f"AGENTS.md sin marcas del kit: añade {MARK_START} … {MARK_END} al principio")

    def claude_md(self) -> None:
        path = self.target / "CLAUDE.md"
        if not path.exists():
            self.write(path, "@AGENTS.md\n", managed=False)
        elif "@AGENTS.md" not in path.read_text(encoding="utf-8"):
            self.log("PENDIENTE", "CLAUDE.md no importa @AGENTS.md: pasa su contenido a AGENTS.md (Project context)")

    def copilot_instructions(self) -> None:
        agents = self.target / "AGENTS.md"
        if not agents.exists():
            self.log("PENDIENTE", ".github/copilot-instructions.md: crea antes AGENTS.md")
            return
        header = "<!-- GENERATED from AGENTS.md by fi-sdd-standard for Visual Studio — do not edit -->\n"
        self.write(self.target / ".github" / "copilot-instructions.md", header + agents.read_text(encoding="utf-8"))
        self.log("REVISAR", "VS Code suma AGENTS.md y .github/copilot-instructions.md: para no duplicar las reglas, "
                 "pon \"github.copilot.chat.codeGeneration.useInstructionFiles\": false en .vscode/settings.json")

    def docs(self) -> None:
        src = KIT / "project-templates" / "docs"
        for f in sorted(src.rglob("*")):
            if f.is_file() and f.name != "README.md":
                dst = self.target / "docs" / f.relative_to(src)
                if dst.exists():
                    self.log("existe", self.rel(dst))
                else:
                    self.write(dst, f.read_text(encoding="utf-8"), managed=False)
        sdd = self.target / "docs" / "sdd"
        if not sdd.exists():
            self.log("creado", "docs/sdd/")
            if not self.dry:
                sdd.mkdir(parents=True)
                (sdd / ".gitkeep").write_text("", encoding="utf-8")

    LOCAL_ONLY = [
        "docs/sdd/*/assets/",
        "docs/sdd/*/commit-message.md",
        "docs/sdd/*/test-cases.csv",
        ".claude/settings.local.json",
        ".github/copilot-instructions.md",
        ".agents/**/__pycache__/",
    ]

    def local_only(self) -> None:
        """ADR-0027: what each person generates or downloads stays out of git."""
        lines = list(self.LOCAL_ONLY)
        instructions = self.target / ".github" / "copilot-instructions.md"
        if instructions.exists() and "GENERATED from AGENTS.md" not in instructions.read_text(encoding="utf-8"):
            lines.remove(".github/copilot-instructions.md")  # the project's own file: it stays versioned
        self.gitignore(lines, "# fi-sdd-standard: no se versiona (ADR-0027)")
        if not (self.target / ".git").exists():
            return
        specs = [f":(glob){l}**" if l.endswith("/") else f":(glob){l}" for l in lines]
        out = subprocess.run(["git", "-C", str(self.target), "ls-files", "--", *specs],
                             capture_output=True, text=True, encoding="utf-8", errors="replace")
        tracked = [l for l in out.stdout.splitlines() if l.strip()]
        if tracked:
            sample = ", ".join(tracked[:3]) + (" …" if len(tracked) > 3 else "")
            self.log("REVISAR", f"{len(tracked)} archivo(s) versionados que ya no se versionan (ADR-0027): {sample}. "
                     "Para dejar de versionarlos sin borrarlos del disco: git rm -r --cached <rutas>")

    def save_state(self) -> None:
        state = {
            "kit": "fi-sdd-standard",
            "version": VERSION,
            "installed": date.today().isoformat(),
            "tools": sorted(self.tools),
            "managed": sorted(self.new_managed | (self.managed if self.dry else set())),
        }
        if not self.dry:
            self.state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        self.log("creado" if not self.state else "actualizado", ".sdd-kit.json")

    def run(self) -> int:
        if not (self.target / ".git").exists():
            print(f"⚠️  {self.target} no parece un repositorio git. Continúo igualmente.")
        if "copilot" in self.tools:
            self.skills_copilot()
        if "claude" in self.tools:
            self.skills_claude()
        self.agents()
        self.guardrails()
        if "claude" in self.tools:
            self.claude_settings()
        self.gitmessage()
        self.agents_md()
        self.claude_md()
        if "visualstudio" in self.tools:
            self.copilot_instructions()
        self.docs()
        self.local_only()
        self.save_state()
        self.print_report()
        return 1 if any(a == "CONFLICTO" for a, _ in self.report) else 0

    def print_report(self) -> None:
        title = "SIMULACIÓN (no se ha escrito nada)" if self.dry else "Instalación"
        print(f"\nfi-sdd-standard v{VERSION} · {title} en {self.target}\n")
        counts: dict[str, int] = {}
        for action, what in self.report:
            counts[action] = counts.get(action, 0) + 1
            if action != "igual":
                print(f"  {action:<12} {what}")
        print("\n  " + " · ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
        steps = []
        if counts.get("CONFLICTO"):
            steps.append("resuelve los CONFLICTO de arriba (el kit no los ha tocado)")
        if counts.get("PENDIENTE") or counts.get("REVISAR"):
            steps.append("revisa los PENDIENTE / REVISAR de arriba")
        if self.commit_template() != ".gitmessage":
            steps.append("git config commit.template .gitmessage")
        agents_md = self.target / "AGENTS.md"
        if not agents_md.exists() or "**Generado con:** project-context" not in agents_md.read_text(encoding="utf-8"):
            steps.append("/project-context en una sesión nueva (contexto del proyecto, documentación base y pruebas)")
        elif not (self.target / "docs" / "sdd" / "_documentacion" / "plan.md").exists():
            steps.append("/document-project en una sesión nueva (documentación completa, por bloques; opcional)")
        print("\n  " + ("Siguiente: " + "  ·  ".join(steps) if steps else "Todo en orden: no hay nada pendiente.") + "\n")

    def commit_template(self) -> str:
        """Current commit.template of the target repository, or '' if git is unavailable or unset."""
        try:
            out = subprocess.run(["git", "-C", str(self.target), "config", "--get", "commit.template"],
                                 capture_output=True, text=True, timeout=10)
            return out.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Instala fi-sdd-standard en un proyecto")
    parser.add_argument("--target", required=True, type=Path, help="Ruta del repositorio del proyecto")
    parser.add_argument("--tools", default="copilot", help="copilot,claude,visualstudio (por defecto: copilot)")
    parser.add_argument("--dry-run", action="store_true", help="Muestra lo que haría sin escribir nada")
    args = parser.parse_args()
    tools = {t.strip() for t in args.tools.split(",") if t.strip()}
    unknown = tools - {"copilot", "claude", "visualstudio"}
    if unknown:
        print(f"Herramientas desconocidas: {', '.join(sorted(unknown))}")
        return 2
    target = args.target.resolve()
    if not target.is_dir():
        print(f"No existe la carpeta {target}")
        return 2
    if target == KIT or KIT in target.parents:
        print("El destino no puede ser el propio kit")
        return 2
    return Installer(target, tools, args.dry_run).run()


if __name__ == "__main__":
    sys.exit(main())
