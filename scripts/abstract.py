#!/usr/bin/env python3
"""
abstract.py — Generates public Faro repo from internal vault files.

Copies internal files → public/, applying abstraction rules:
1. MCP tool refs → generic descriptions
2. Relay-specific refs → "peer coordination" language
3. Concrete paths → relative/generic paths
4. Skill refs → removed
5. Named identities (Hilo/Prima/Eco/Lienzo) → generic role descriptions

Run from Hilo workspace:
    python scripts/abstract.py

Requires: internal vault files at VAULT_PATH (default: F:/obsidian/GuildWars/Eco_Consulting/Faro)
Produces: public/ directory ready for GitHub push.
"""

import os
import re
import shutil
from pathlib import Path

VAULT_PATH = Path(os.environ.get("FARO_VAULT_PATH", "F:/obsidian/GuildWars/Eco_Consulting/Faro"))
PUBLIC_PATH = Path(__file__).parent.parent

# Agent directories to include (24 active, skip 3 archived)
ACTIVE_AGENTS = [
    "Architect", "Investigator", "Challenger", "ChallengerSpec",
    "Supervisor", "Executor", "Verifier", "Scribe", "Designer",
    "Editor", "Source_Critic", "Analyst", "Layout_Designer",
    "News_Researcher", "Weaver",
    "Code_Adversarial", "Design_Adversarial", "Security_Adversarial",
    "Audit_Adversarial", "Visual_Adversarial",
    "Pioneer", "Guardian", "Pragmatist", "Archivist"
]

ARCHIVED_AGENTS = ["Data_Analyst", "Scraper", "Synthesizer"]

# Abstraction rules: (pattern, replacement)
ABSTRACTIONS = [
    # MCP tool calls → generic descriptions (preserve agent name)
    (r'`?relay_ask\(to="([^"]+)",\s*question="[^"]*"\)`?', r'dispatch task to \1'),
    (r'`?relay_ask\(to="([^"]+)",\s*question=<[^>]*>\)`?', r'dispatch task to \1'),
    (r'`?relay_reply\([^)]+\)`?', 'reply to requesting peer'),
    (r'`?relay_peers\(\)`?', 'discover available peer agents'),
    (r'`?relay_join\([^)]+\)`?', 'join coordination room'),
    (r'`?relay_room\([^)]+\)`?', 'broadcast to coordination room'),
    (r'`?relay_leave\([^)]+\)`?', 'leave coordination room'),
    (r'`relay_ask`', 'peer dispatch'),
    (r'`relay_reply`', 'peer reply'),
    (r'`relay_peers`', 'peer discovery'),
    (r'relay_ask\b', 'peer dispatch'),
    (r'relay_reply\b', 'peer reply'),
    (r'relay_peers\b', 'peer discovery'),

    # EcoDB tool calls → generic
    (r'`?search\(query_text="[^"]*"[^)]*\)`?', 'search shared memory'),
    (r'`?search_recent\([^)]*\)`?', 'search recent memories'),
    (r'`?save_memory\([^)]*\)`?', 'persist to shared memory'),
    (r'`?save_triple\([^)]*\)`?', 'save relationship to knowledge graph'),
    (r'`?neighbors\([^)]*\)`?', 'explore graph connections'),
    (r'`?search_nodes\([^)]*\)`?', 'search graph nodes'),
    (r'`?path_between\([^)]*\)`?', 'find path between graph nodes'),
    (r'`?load_identity\([^)]*\)`?', 'load agent identity'),
    (r'`?view_image\([^)]*\)`?', 'view stored image'),

    # Concrete paths → generic (multiple formats)
    (r'F:\\\\obsidian\\\\GuildWars\\\\Eco_Consulting[/\\\\]Faro[/\\\\]', '$FARO_ROOT/'),
    (r'F:/obsidian/GuildWars/Eco_Consulting/Faro/', '$FARO_ROOT/'),
    (r'F:\\obsidian\\GuildWars\\Eco_Consulting\\Faro\\', '$FARO_ROOT/'),
    (r'Eco_Consulting/Faro/', '$FARO_ROOT/'),
    (r'Eco_Consulting\\Faro\\', '$FARO_ROOT/'),
    (r'C:\\\\Users\\\\Admin\\\\AppData\\\\Roaming\\\\Claude\\\\', '$CLAUDE_CONFIG/'),
    (r'C:/Users/Admin/AppData/Roaming/Claude/', '$CLAUDE_CONFIG/'),
    (r'C:\\\\Users\\\\Admin\\\\Documents\\\\', '$WORKSPACE/'),
    (r'C:/Users/Admin/Documents/', '$WORKSPACE/'),
    (r'C:\\Users\\Admin\\Documents\\', '$WORKSPACE/'),
    (r'C:\\\\Users\\\\Admin\\\\', '$HOME/'),
    (r'C:/Users/Admin/', '$HOME/'),
    (r'C:\\Users\\Admin\\', '$HOME/'),
    (r'F:\\\\obsidian\\\\GuildWars\\\\', '$VAULT/'),
    (r'F:/obsidian/GuildWars/', '$VAULT/'),
    (r'F:\\obsidian\\GuildWars\\', '$VAULT/'),

    # Personal name → generic
    (r'\bPepe\b', 'the user'),

    # Spanish EcoDB schema values → EN for public readability
    (r'type="observacion"', 'type="observation"'),
    (r'tags=\["evaluacion"', 'tags=["evaluation"'),

    # Eco Relay specifics → generic coordination
    (r'Eco Relay', 'inter-session messaging system'),
    (r'eco-relay', 'relay-plugin'),
    (r'eco_brujula', 'utility-tools'),

    # Playwright MCP tool names → generic
    (r'mcp__playwright__browser_navigate', 'browser_navigate'),
    (r'mcp__playwright__browser_evaluate', 'browser_evaluate'),
    (r'mcp__playwright__browser_close', 'browser_close'),

    # Skill/plugin refs
    (r'\.claude/skills/[^\s]+', '.claude/skills/<workflow>/SKILL.md'),
    (r'superpowers:[a-z-]+', '<skill-name>'),

    # Named agent identities in frontmatter (optional — keep as system names)
    # (r'author: Hilo', 'author: orchestrator'),
    # (r'author: Prima', 'author: rd-lead'),
]

def abstract_content(content: str) -> str:
    """Apply abstraction rules to file content."""
    result = content
    for pattern, replacement in ABSTRACTIONS:
        result = re.sub(pattern, replacement, result)
    return result

def copy_and_abstract(src: Path, dst: Path):
    """Copy file, applying abstraction if .md."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix == '.md':
        content = src.read_text(encoding='utf-8')
        abstracted = abstract_content(content)
        dst.write_text(abstracted, encoding='utf-8')
    else:
        shutil.copy2(src, dst)

def main():
    public = PUBLIC_PATH

    # Clean public dir (except scripts/ and .git/)
    for item in ['agents', 'workflows', 'templates', 'docs']:
        target = public / item
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)

    # Agents
    for agent in ACTIVE_AGENTS:
        src = VAULT_PATH / "Agentes" / agent / "CLAUDE.md"
        if src.exists():
            copy_and_abstract(src, public / "agents" / agent / "CLAUDE.md")

    # Workflows (SKILLs)
    for skill_file in (VAULT_PATH / "Skills").glob("SKILL_md_workflow_*.md"):
        copy_and_abstract(skill_file, public / "workflows" / skill_file.name)

    # Templates
    for template in (VAULT_PATH / "Plantillas").iterdir():
        if template.is_file():
            copy_and_abstract(template, public / "templates" / template.name)

    # Core docs
    for doc_name in ["FARO_ESTADO.md", "GLOSARIO.md", "ORCHESTRATOR_PREAMBLE.md", "GLOSSARY_ES_EN.md"]:
        src = VAULT_PATH / "Documentacion" / doc_name
        if src.exists():
            copy_and_abstract(src, public / "docs" / doc_name)

    print(f"Public variant generated at: {public}")
    print(f"  Agents: {len(list((public / 'agents').rglob('CLAUDE.md')))}")
    print(f"  Workflows: {len(list((public / 'workflows').glob('*.md')))}")
    print(f"  Templates: {len(list((public / 'templates').iterdir()))}")
    print(f"  Docs: {len(list((public / 'docs').glob('*.md')))}")

if __name__ == "__main__":
    main()
