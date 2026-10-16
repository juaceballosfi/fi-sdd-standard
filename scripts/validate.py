#!/usr/bin/env python3
"""Validate the fi-sdd-standard kit: skills, agents, shared rules and ADRs.

Usage (from the repository root):  python scripts/validate.py
Exit code 0 = no errors (warnings allowed), 1 = errors found.

Based on validate-skills.py from the SDD flow v2.3 (Juan Antonio Ceballos).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "core" / "skills"  # single source (ADR-0011); tool copies are generated
AGENTS_DIR = ROOT / "core" / "agents"
PROMPTS_DIR = ROOT / "core" / "prompts"
BASE_RULES = ROOT / "core" / "AGENTS.base.md"
ADR_DIR = ROOT / "docs" / "adr"
AGENT_PERMISSIONS = {"read", "edit", "execute"}
MODEL_TIERS = {"fast", "standard", "reasoning"}
BASE_RULES_MAX_LINES = 120  # leaves room for project context under 200 lines (ADR-0014)
FLOW = ["enrich-us", "technical-analysis", "wbs-execution", "qa-review", "document-code", "project-context",
        "document-project", "quick-fix", "test-cases"]

# Fields understood by every target (Agent Skills spec + Claude Code + Copilot).
PORTABLE_FIELDS = {"name", "description", "argument-hint", "license", "compatibility", "metadata",
                   "user-invocable"}
# Claude Code-only fields: they belong in the generated .claude/skills copy (sync script), not here.
CLAUDE_ONLY_FIELDS = {
    "model": "short model names like 'sonnet' are Claude Code-only; the VS Code test of v2.0 "
             "froze on the only skill that had it",
    "allowed-tools": "uses Claude Code tool names (Read, Bash…) that Copilot does not know",
}
# Required anchors: file (relative to skill dir) -> anchors
REQUIRED_ANCHORS = {
    "enrich-us/templates/pbi.md": ["sdd:pending", "sdd:acceptance-criteria", "sdd:i18n"],
    "enrich-us/templates/bug.md": ["sdd:pending", "sdd:acceptance-criteria", "sdd:i18n"],
    "enrich-us/templates/bitacora.md": ["sdd:log"],
    "technical-analysis/templates/01-current-state-report.md": ["sdd:i18n"],
    "technical-analysis/templates/00-executive-summary.md": ["sdd:markers"],
    "technical-analysis/templates/04-implementation-plan.md": ["sdd:specs"],
    "technical-analysis/templates/05-wbs-estimation.md": ["sdd:tasks", "sdd:task-log"],
    "technical-analysis/templates/06-risks-mitigations.md": ["sdd:risks"],
    "qa-review/templates/qa-report.md": ["sdd:qa-findings"],
    "quick-fix/templates/fix-plan.md": ["sdd:fix-gate", "sdd:fix-cause", "sdd:fix-tests", "sdd:tasks"],
    "test-cases/templates/test-cases.md": ["sdd:test-cases"],
    "document-project/templates/plan.md": ["sdd:doc-areas", "sdd:doc-blocks", "sdd:doc-findings", "sdd:log"],
}

# Templates a person fills (ADR-0015): no AI stamp. Each string must stay in the template because
# scripts/new-sdd-item.py replaces it.
PERSON_TEMPLATES = {"story.md"}
NEW_ITEM_STRINGS = {
    "enrich-us/templates/story.md": ["# Work item <ID> — <Título>",
                                     "**Preparado por:** <persona> · **Leído:** <AAAA-MM-DD>",
                                     "<PBI | Bug>", "<!-- solo-bug -->\n", "<!-- /solo-bug -->\n",
                                     "## Descripción\n\n<texto literal>\n\n", "## Criterios de aceptación", "## Adjuntos"],
    "enrich-us/templates/bitacora.md": ["# Bitácora — <ID> <Título>", "**Generado con:**", "#[ID]",
                                        "docs/sdd/[ID]-[slug]/", "\n- AAAA-MM-DD · <persona> · "],
}

# Shared rule that must be word-for-word identical in every flow skill.
I18N_RULE = "- **User-visible texts (i18n):** this rule is about the product's texts"

errors: list[str] = []
warnings: list[str] = []


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line and not line.startswith((" ", "#")) and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


def check_skill(skill_dir: Path) -> None:
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{name}: missing SKILL.md")
        return
    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if not fm:
        errors.append(f"{name}: SKILL.md has no YAML frontmatter")
        return

    if fm.get("name") != name:
        errors.append(f"{name}: frontmatter name '{fm.get('name')}' must match the folder name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append(f"{name}: name must be lowercase letters, digits and hyphens (max 64)")
    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{name}: description is required")
    elif len(desc) > 1024:
        errors.append(f"{name}: description is {len(desc)} chars (max 1024)")

    for key in fm:
        if key in CLAUDE_ONLY_FIELDS:
            errors.append(f"{name}: field '{key}' in the canonical copy — {CLAUDE_ONLY_FIELDS[key]}. "
                          "Add it in scripts/sync-claude-skills.py instead")
        elif key == "disable-model-invocation":
            warnings.append(f"{name}: 'disable-model-invocation' can stop Visual Studio from ever "
                            "activating the skill (it activates skills automatically)")
        elif key not in PORTABLE_FIELDS:
            warnings.append(f"{name}: field '{key}' is not portable")

    lines = text.count("\n") + 1
    if lines > 500:
        warnings.append(f"{name}: SKILL.md has {lines} lines (recommended < 500)")

    # Claude-only syntax that would reach Copilot as literal text or fail silently.
    if re.search(r"!`[^`]+`", text):
        errors.append(f"{name}: uses !`command` injection (Claude Code only)")
    if re.search(r"(^|\s)@[\w*./-]+\.(json|csproj|md)", text):
        errors.append(f"{name}: uses @file references (not expanded inside skills)")
    if "$ARGUMENTS" in text and "placeholder that starts with a dollar" not in text:
        warnings.append(f"{name}: $ARGUMENTS without a fallback for tools that do not substitute it")
    if text.count("$ARGUMENTS") > 1:
        errors.append(f"{name}: $ARGUMENTS appears more than once; Claude Code substitutes every "
                      "occurrence, so explanatory text that mentions it becomes nonsense")
    if "Shared SDD conventions" not in text:
        errors.append(f"{name}: missing the 'Shared SDD conventions' section")
    elif name in FLOW and I18N_RULE not in text:
        errors.append(f"{name}: the shared i18n rule is missing or differs from the other skills")

    for link in re.findall(r"\]\(([^)#]+)\)", text):
        if not link.startswith(("http://", "https://")) and not (skill_dir / link).exists():
            errors.append(f"{name}: broken link -> {link}")

    for tpl in (skill_dir / "templates").rglob("*.md") if (skill_dir / "templates").exists() else []:
        if tpl.name in PERSON_TEMPLATES:
            continue
        if "**Generado con:**" not in tpl.read_text(encoding="utf-8"):
            errors.append(f"{name}: template {tpl.name} has no 'Generado con' traceability stamp")


def parse_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [v.strip() for v in value.split(",") if v.strip()]


def check_versions() -> None:
    """The version in '# Skill: <name> · vX' must match every stamp in that skill and its templates."""
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.exists():
            continue
        m = re.search(r"^# Skill: [\w-]+ · v([\d.]+)", md.read_text(encoding="utf-8"), re.M)
        if not m:
            continue
        version = m.group(1)
        files = [md] + sorted((skill_dir / "templates").rglob("*.md")) if (skill_dir / "templates").exists() else [md]
        for f in files:
            for found in re.findall(rf"{skill_dir.name} v([\d.]+)", f.read_text(encoding="utf-8")):
                if found != version:
                    errors.append(f"{skill_dir.name}: {f.name} stamps v{found}, skill is v{version}")


def check_agents() -> None:
    """Neutral agent definitions in core/agents (ADR-0011, ADR-0013)."""
    if not AGENTS_DIR.is_dir():
        errors.append("missing folder core/agents")
        return
    skills = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
    for md in sorted(AGENTS_DIR.glob("*.md")):
        if md.name == "README.md":
            continue
        fm = parse_frontmatter(md.read_text(encoding="utf-8"))
        name = md.stem
        if not fm:
            errors.append(f"agent {name}: no YAML frontmatter")
            continue
        if fm.get("name") != name:
            errors.append(f"agent {name}: frontmatter name '{fm.get('name')}' must match the file name")
        if not fm.get("description"):
            errors.append(f"agent {name}: description is required")
        perms = set(parse_list(fm.get("permissions", "")))
        if not perms or not perms <= AGENT_PERMISSIONS:
            errors.append(f"agent {name}: permissions must be a subset of {sorted(AGENT_PERMISSIONS)}")
        if fm.get("status") not in {"draft", "stable"}:
            errors.append(f"agent {name}: status must be draft or stable")
        elif fm.get("status") == "stable" and "Use " not in fm.get("description", ""):
            errors.append(f"agent {name}: a stable agent needs a description that says when to use it ('Use ...')")
        if fm.get("model_tier") not in MODEL_TIERS:
            errors.append(f"agent {name}: model_tier must be one of {sorted(MODEL_TIERS)}")
        for skill in parse_list(fm.get("skills", "")):
            if skill not in skills:
                warnings.append(f"agent {name}: skill '{skill}' is not in core/skills yet")


def check_base_rules() -> None:
    """core/AGENTS.base.md must stay short (ADR-0014)."""
    if not BASE_RULES.exists():
        errors.append("missing core/AGENTS.base.md")
        return
    lines = BASE_RULES.read_text(encoding="utf-8").count("\n") + 1
    if lines > BASE_RULES_MAX_LINES:
        errors.append(f"core/AGENTS.base.md has {lines} lines (max {BASE_RULES_MAX_LINES})")


def check_adrs() -> None:
    """Every ADR file is listed in docs/adr/README.md (ADR-0001)."""
    index = ADR_DIR / "README.md"
    if not index.exists():
        errors.append("missing docs/adr/README.md")
        return
    text = index.read_text(encoding="utf-8")
    for adr in sorted(ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")):
        if adr.name.startswith("0000-"):
            continue
        if f"({adr.name})" not in text:
            errors.append(f"docs/adr/README.md does not list {adr.name}")


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"Skills folder not found: {SKILLS_DIR}")
        return 1
    for skill in FLOW:
        if not (SKILLS_DIR / skill).is_dir():
            errors.append(f"flow skill missing: {skill}")
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        check_skill(skill_dir)
    rules = {}
    for skill in FLOW:
        md = SKILLS_DIR / skill / "SKILL.md"
        if md.exists():
            m = re.search(re.escape(I18N_RULE) + r".*?(?=\n- \*\*)", md.read_text(encoding="utf-8"), re.S)
            if m:
                rules[skill] = m.group(0)
    if len(set(rules.values())) > 1:
        errors.append("the shared i18n rule is not word-for-word identical in "
                      + ", ".join(sorted(rules)))
    shared = {}
    for skill in FLOW:
        md = SKILLS_DIR / skill / "SKILL.md"
        if md.exists():
            m = re.search(r"^## Shared SDD conventions\n.*?(?=^## )", md.read_text(encoding="utf-8"), re.S | re.M)
            if m:
                shared[skill] = m.group(0)
    if len(set(shared.values())) > 1:
        errors.append("the 'Shared SDD conventions' section is not identical in " + ", ".join(sorted(shared)))
    check_versions()
    for rel, anchors in REQUIRED_ANCHORS.items():
        path = SKILLS_DIR / rel
        if not path.exists():
            errors.append(f"missing template: {rel}")
            continue
        content = path.read_text(encoding="utf-8")
        for anchor in anchors:
            if f"<!-- {anchor} -->" not in content:
                errors.append(f"{rel}: missing anchor <!-- {anchor} -->")

    for prompt in sorted(PROMPTS_DIR.glob("*.prompt.md")):
        text = prompt.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)#]+)\)", text):
            if not link.startswith(("http://", "https://")) and not (prompt.parent / link).exists():
                errors.append(f"{prompt.name}: broken link -> {link}")
        stem = prompt.name.removesuffix(".prompt.md")
        if (SKILLS_DIR / stem).is_dir():
            errors.append(f"{prompt.name}: same name as the skill '{stem}' — the / menu would be ambiguous")

    for rel, needles in NEW_ITEM_STRINGS.items():
        path = SKILLS_DIR / rel
        if path.exists():
            content = path.read_text(encoding="utf-8")
            for needle in needles:
                if needle not in content:
                    errors.append(f"{rel}: missing «{needle.strip()}» (used by scripts/new-sdd-item.py)")

    check_agents()
    check_base_rules()
    check_adrs()

    checked = len([p for p in SKILLS_DIR.iterdir() if p.is_dir()])
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    agents = len([p for p in AGENTS_DIR.glob("*.md") if p.name != "README.md"])
    print(f"\n{checked} skills · {agents} agents checked · {len(errors)} errors · {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
