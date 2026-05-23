---
name: workflow-integracion
description: |
  Orchestrated workflow for integrating new external technology into the system. Use it whenever the user asks to install, incorporate, add or test a tool, package, library, MCP, ComfyUI node, extension, or any technology that comes from outside and must be made to work inside the existing ecosystem. Also activates when something "is not installed" or "needs to be configured from scratch". Do not wait for the user to ask explicitly — if the request implies bringing something from outside and making it work, this is the correct workflow.
metadata:
  version: "4.0"
  relay_rewrite: 2026-05-22
  debut_v1: 2026-04-16
  hardened_v2: 2026-04-18
  agent_teams_v3: 2026-04-26
  author_v3: Prima
  invocation: relay session (separate Claude Code instance)
  motivation_hardening: |
    Application of the workflow-construction v3 methodology to workflow-integration. v1 had valuable knowledge base (ComfyUI/ElevenLabs/MCPs errors) but lacked all v2/v3 discipline: literal prompts, explicit human gates, minimum Install Blueprint schema, cross-validation between Designer assumptions and external system reality, physical location, retrospective.
tags:
  - workflow/integracion
  - agent/designer
  - agent/executor
  - agent/verifier
  - agent/scribe
---

# Workflow: Integration (v4 — Relay)

Orchestrates the installation and incorporation of external technology. The goal is not that something "gets installed" but that it **works verifiably**, and that the knowledge is documented to avoid repeating it.

> **Guiding principle 1 — Do not improvise**: Faro and subagents do not infer well. Every step, prompt, path and format explicit.
>
> **Guiding principle 2 — External system reality > Designer assumptions**: if the Designer assumes an API/library/service behaves a certain way but execution reveals it does not, **reality wins**. The Verifier validates against the real system, not the blueprint. A non-existent endpoint, a renamed package, an eliminated flag — all of these are BLOCKERS.
>
> **Guiding principle 3 — "Installed without errors" is NOT verification**: verification is functional. `pip install X` completing without error does not mean X works. The Verifier tests real usage.

---

## When it activates

Faro launches this workflow when:
1. the user asks to install/integrate something that comes from outside (PyPI package, MCP server, plugin, extension, library, external API, etc.).
2. And the task has been classified as trivial / standard / critical.

**Do NOT** use for:
- Modifying existing code → workflow-evolution
- Connecting two already-installed systems → workflow-adaptation
- Building something new from scratch → workflow-construction

---

## Complexity levels

| Level | Criteria | Action |
|---|---|---|
| **trivial** | `pip install X`, download <100MB, no cross-dependencies, no configuration | Executor + quick functional verification |
| **standard** | Multiple dependencies, necessary config, risk of conflict with other libs | Designer + Executor + Verifier |
| **critical** | Integration with ecosystem architecture, downloads >1GB, MCPs that touch EcoDB, services running in background | **workflow-design first** (if it touches architectural decisions) OR full cycle with Plan Reviewer |

---

## The 4 human gates

### Gate B0 — Load confirmation

```
[GATE B0 — Load confirmation]
I have loaded workflow-integration v3.

Brief received: <summary>
Technology to integrate: <name + version if specified>
Classified level: <trivial | standard | critical>

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones/<YYYY-MM-DD>_<tech>_integracion/
- Reports: <project path>/.faro/integration_reports/
- Agents:
    1. Designer (generic mode) — produces Install Blueprint
    2. Executor (after Gate B1 if download >500MB or touches sensitive configs)
    3. Functional Verifier (not declarative)
    4. Scribe (at the end + updates knowledge base)

Subsequent gates:
- B1 before downloads >500MB or installation of background services
- B2 if Blueprint requires revision after Executor failure
- B3 if the user changes scope during integration

Options:
- "Proceed"
- "Adjust X"
- "Do not proceed"

What do I do?
```

### Gate B1 — Before large downloads or persistent services

```
[GATE B1 — Destructive/voluminous installation imminent]
Step N of Install Blueprint: <title>
Action: <summary + exact command>
Estimated download size: <MB/GB>
Services that will start: <list or "none">
Config files that will be modified: <list or "none">
Rollback: <exact command>

Options:
- "Proceed"
- "Stop the workflow"
- "Review X first"

What do I do?
```

### Gate B2 — Blueprint requires revision

**When**: any of:
- Executor reports `STATUS: DISAGREEMENT_WITH_BLUEPRINT` (reality does not match blueprint)
- 3 Executor↔Verifier iterations fail
- Designer detects during blueprint that the technology requires more study (e.g. knowledge base has prior unresolved warnings)

```
[GATE B2 — Install Blueprint requires revision]
Technology: <name>
Reason: <"reality differs from blueprint" | "3 failed iterations" | "unresolved warnings in knowledge base">
Concrete conflict: <what the Blueprint says vs what the Executor/Verifier discovered>
Designer's proposal: <concrete change to Blueprint>

Options:
- "Apply the proposed change and resume"
- "Pause — I want to review the Blueprint manually"
- "Abort — this integration needs more research or a prior the user decision"

What do I do?
```

### Gate B3 — Scope change

```
[GATE B3 — Scope change]
the user's request: <description>
Current phase: <step N>
Impact: <what of the Blueprint remains valid>

Options:
- "Apply the change"
- "Defer it for later"
- "Cancel the request"

What do I do?
```

---

## System agents — Relay (v4.0, 2026-05-22)

```
join coordination room

RELAY PEERS (separate sessions):
├── Designer (OPUS) — central, produces Install Blueprint, coordinates
├── Executor (Sonnet) — applies blueprint steps, reports to designer
├── Verifier (Sonnet) — FUNCTIONAL beta tester (guiding principle 3: "installed" ≠ "works")
└── Investigator (Haiku) — standby to query docs, repos, issues of the technology

SUBAGENT:
└── Scribe (Sonnet) — close + updates error knowledge base

LEAD (Prima):
└── Gates, escalation to workflow-design if critical.
```

| Agent | Type | Model | CLAUDE.md | Mode |
|---|---|---|---|---|
| **Designer** | Relay peer | **Opus** | `Diseñador/CLAUDE.md` | Generic (installation) |
| **Executor** | Relay peer | Sonnet | `Ejecutor/CLAUDE.md` | — |
| **Verifier** | Relay peer | Sonnet | `Verificador/CLAUDE.md` | Functional beta tester |
| **Investigator** | Relay peer | Haiku | `Investigador/CLAUDE.md` | Standby |
| **Scribe** | Subagent | Sonnet | `Escribano/CLAUDE.md` | — |

### Direct communication

```
Designer produces blueprint → disk
Designer ──peer dispatch──→ Executor: "execute step N"
Executor ──peer dispatch──→ Designer: reports + problems
Executor/Designer ──peer dispatch──→ Investigator: "query docs for <tech>"
Designer ──peer dispatch──→ Verifier: "FUNCTIONALLY verify step N"
Verifier ──peer dispatch──→ Designer: functional report
Designer consolidates → peer dispatch to Prima
```

### Chain of command

- **the user**: gates, scope.
- **Prima**: final decisions, escalation to workflow-design.
- **Designer (Opus)**: coordinates integration, decides what works and what doesn't. Queries knowledge base.
- **Executor/Verifier**: execute and report.

### Relay peer state

| Phase | Designer | Executor | Verifier | Investigator |
|---|---|---|---|---|
| Blueprint | **working** | idle | idle | standby |
| Execution | supervising | **working** | idle | standby |
| Verification | coordinating | idle | **working** | standby |
| Fix (if it fails) | supervising | **working** | idle | standby |
| Close | shutdown | shutdown | shutdown | shutdown |

**Cost of idle relay peers**: zero tokens.

#### WARNING — Correct agent invocation rule (2026-04-28)

**ALL agents are launched as relay sessions with a clean context + peer name.**

```
dispatch task to <agent-name>
```

**NEVER pass the full lead context to a peer.** Peers only need their brief.

**Incident 2026-04-28:** 7 investigators launched without clean context = 700k tokens burned just on startup.

---

## Initial setup

```
$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<tech>_integracion/
  ├── ENVIRONMENT.md
  ├── CONTRACT.md
  ├── LESSONS.md
  └── orchestration.md

<path of project or system where integrated>/.faro/
  └── integration_reports/
        ├── install_blueprint.md
        ├── executor_step_<N>_iter_<M>.md
        ├── verifier_step_<N>_iter_<M>.md
        └── scribe_close.md
```

### Templates

- `$FARO_ROOT/Plantillas/INSTALL_BLUEPRINT_template.md` (new)
- `$FARO_ROOT/Plantillas/ENVIRONMENT_template.md` (shared)
- `$FARO_ROOT/Plantillas/CONTRACT_template.md` (shared)
- `$FARO_ROOT/Plantillas/LESSONS_template.md` (shared)

---

## Install Blueprint minimum schema

```
# Install Blueprint — <technology + version>

## Metadata
- Technology: <official name>
- Target version: <exact>
- Official documentation: <URL>
- Blueprint date: <YYYY-MM-DD>
- Designer: Generic Opus

## 1. Knowledge base query
- EcoDB queried with tags: <list>
- Relevant prior findings: <list or "none">
- Error knowledge base (section of this SKILL) reviewed: yes/no
- Unresolved prior warnings: <list or "none">

## 2. Dependencies
List with exact version and official source:
- <dep1>: <version> — <docs url>
- <dep2>: <version> — <docs url>

## 3. Installation plan (ordered steps)
Each step:
- P<N>: <action>
  - Exact command: `<cmd>`
  - Expected output: <literal or regex>
  - Alternative if it fails: <plan B with command>
  - Functional verification of step: <command that proves the step did what it should>

## 4. Functional success criteria (not declarative)
**Guiding principle 3**: "pip install OK" does NOT count. "tool.function(args) returns expected result" counts.
- [ ] <functional criterion> verifiable with `<command + expected output>`

## 5. Known warnings
- <warning> — origin: <knowledge base | official docs | inference>

## 6. Rollback
Exact command to completely uninstall and return to pre-integration state.
```

---

## Workflow flow (literal prompts)

### Step 0: Faro validates and prepares

1. Receives brief.
2. Determines level. If critical and touches architecture → launch workflow-design first.
3. Pre-flight checks:
   - Internet connection
   - Sufficient disk space (>2x estimated size)
   - Necessary permissions (local admin if touching services)
   - EcoDB accessible
4. Creates session folder and reports.
5. **Gate B0**.

### Step 1: Designer (Install Blueprint)

```
<Diseñador/CLAUDE.md>

---

[BRIEF FOR YOU — Designer (generic mode, integration)]

Workflow: integration v3
Technology: <name>
the user's brief (literal): <text>
Level: <trivial | standard | critical>

Your task:

1. **Query EcoDB** (`search` tool) with tags: "integracion", "<tech-name>", "<domain>", "error" — search for similar prior installations from any agent.

2. **Review the error knowledge base** of this SKILL (section "Knowledge base"). If there are specific warnings for this technology or related technologies, incorporate them into the Blueprint.

3. **Read updated official documentation** — not from your training cutoff. If unsure of current version, look it up.

4. **Identify dependencies** with exact version. If there are known incompatibilities (e.g. rustworkx requires numpy >=1.16), document them.

5. **Ordered installation plan** with:
   - Exact command per step (no pseudo-commands)
   - Literal expected output
   - Alternative if it fails (concrete plan B)
   - **Functional verification per step** (guiding principle 3 — NOT "if pip said OK")

6. **Functional success criteria** — NOT declarative. Examples:
   - Bad: "The package is installed"
   - Good: "`python -c 'import X; X.key_function()'` returns `<expected output>`"

7. Write Install Blueprint complying with minimum schema (6 sections):
   - Template: `$FARO_ROOT/Plantillas/INSTALL_BLUEPRINT_template.md`
   - Save it in `<path>/.faro/integration_reports/install_blueprint.md`

8. If you detect the integration requires architectural decisions (e.g. where the service lives, how it connects with EcoDB) → mark `requires_escalation_to_design: true` and do NOT specify those details here.

Return:
- Blueprint path
- Summary: N dependencies, M steps, flag `requires_escalation_to_design`
- Pre-commitment: "Blueprint delivered. I do not execute anything until Faro dispatches the Executor."
```

### Step 2: Executor (for each Blueprint step, in order)

**Step 2.0** — If download >500MB or service installation → **Gate B1**.

**Step 2.1** — Executor:

```
<Ejecutor/CLAUDE.md>

---

[BRIEF FOR YOU — Executor, Step <N> iter <M> of Install Blueprint]

Before touching anything:
1. Read ENVIRONMENT.md, LESSONS.md, CONTRACT.md
2. Verify current system state (what is installed, what versions)

Step to execute (literal from Blueprint):
<block P<N>>

Execute ONLY this step. Do NOT take advantage to install additional things even if they seem related.

When done:
1. Verify output against Blueprint "expected output".
2. **Run the functional verification of the step** — if the Blueprint includes it (it should).
3. Generate EXECUTOR_REPORT in `<path>/.faro/integration_reports/executor_step_<N>_iter_<M>.md`.

If reality does not match the Blueprint (renamed package, changed endpoint, different output):
- STATUS = DISAGREEMENT_WITH_BLUEPRINT
- Document the exact discrepancy. Do NOT improvise the fix.

If the step has `alternative_if_fails`, try it BEFORE marking DISAGREEMENT — it's what the Designer foresaw.
```

**Step 2.2** — BLIND Verifier:

```
<Verificador/CLAUDE.md>

---

[BRIEF FOR YOU — Functional Verifier (guiding principle 3)]

Your job: verify the integration WORKS, not that "it was installed".

YOU DO NOT HAVE ACCESS to the Executor's report. Only:
- ENVIRONMENT.md
- Functional success criteria from Blueprint (Section 4)
- Access to the real system

Your job:
1. For each functional criterion: run the command, verify real output against expected output.
2. Adversarial: test edge cases — what happens if the credential is missing?, if the external service doesn't respond?, if you pass empty input?
3. Verify you have NOT broken other existing integrations (if applicable, ecosystem test pool).

HARD INVARIANT: "installed without errors" does NOT count as verification. If a criterion is "X was installed" without functional proof, mark as FRAGILE_ASSERT and add your own functional test.

Dual report format (markdown-INI + JSON, with APPROVE_WITH_DEBT available).
Save it in `<path>/.faro/integration_reports/verifier_step_<N>_iter_<M>.md`.
```

### Step 3: Scribe + Retrospective + knowledge base update

When all steps are APPROVE:

**Scribe** (literal brief analogous to other workflows) with addition:

```
...(rest of Scribe brief)...

**KNOWLEDGE BASE UPDATE** (specific to integration):
If during the integration new undocumented errors appeared, or were resolved differently from what was documented, **update the "Knowledge base" section of the SKILL workflow-integration** with the new finding. This base grows with each integration and is input for the next.

Entry format:
- [technology] [version]: [error/gotcha description] → [solution]
```

**Faro Retrospective** (analogous).

---

## Knowledge base (updated after each integration)

### ComfyUI / FLUX
- VAE `ae.safetensors`: repo `black-forest-labs` gated → use `camenduru/flux1-dev`
- IP-Adapter FLUX: `x-flux-comfyui` broken in 0.19.x → use Shakker-Labs + InstantX
- `end_percent` Shakker: maximum 0.75
- MCP package: `comfyui-mcp` (not `comfyui-mcp-server`)

### ElevenLabs
- Without `voices_read`: bypass with direct curl to REST API

### MCPs
- Test with `uvx [package] --help` before configuring
- If the MCP code reads credentials from a file AND we migrate to env var: ALWAYS update **BOTH** MCP configs adding the env var to the server's `env` block:
  - `$HOME/AppData\Roaming\Claude\claude_desktop_config.json` — used by Claude Desktop (the user + Faro)
  - `$HOME/.claude.json` — used by Claude Code CLI (Eco, Prima, other agents instantiated as CLI)
  If one of the two is forgotten, the MCP works in some agents but not others. (Lesson from the eco_graph_mcp v2 refactor, 2026-04-18 — happened twice the same day.)

### Python / pip on Windows
- Encoding: always `PYTHONIOENCODING=utf-8`
- Paths with backslash on native Windows, `/` in Git Bash
- Without direct access → generate downloadable `.bat`
- Wheels `cp39-abi3-win_amd64` work for Python 3.14 (e.g. rustworkx 0.17.1)

### PostgreSQL
- `psql` is usually not in Git Bash PATH → use absolute path `/c/Program Files/PostgreSQL/17/bin/psql.exe`
- Migrations with literal `BEGIN/COMMIT` break with psycopg2 → use `psql -f script.sql -v ON_ERROR_STOP=1`

### VibeVoice
- Flash Attention 2 does NOT work on Windows or Turing (sm_75) → automatic fallback to SDPA
- Python 3.14 + numba/llvmlite: compatible (verified 2026-04-24, risk not materialized)
- transformers must be ==4.51.3 (pinned by extra streamingtts)
- RTF ~1.5x free GPU, ~17x occupied GPU — do not use during gaming/rendering
- Texts <3 words unstable
- Spanish voices are experimental: sp-Spk{0,2,4}_woman.pt, sp-Spk{3,5}_man.pt

---

## Anti-stuck protocols

### Anti-stuck — Designer

If the Designer delivers Blueprint without "functional verification per step" or with declarative success criteria ("it is installed"), Faro returns:

> *"Guiding principle 3 is non-negotiable: FUNCTIONAL verification, not declarative. Rewrite Section 3 (step.functional_verification) and Section 4 (success criteria) with commands that test real usage, not just existence."*

### Anti-stuck — Executor

If Executor improvises a fix not listed as a Blueprint alternative:

> *"If reality differs from the Blueprint, mark DISAGREEMENT_WITH_BLUEPRINT. Do not improvise the fix — the Designer must update the Blueprint (Gate B2) because that discrepancy probably affects future steps."*

### Anti-stuck — Verifier

If the Verifier returns APPROVE with purely declarative criteria:

> *"'Installed without errors' does not count. For each Blueprint criterion, did you run a functional command? If not — go back and do it."*

### Anti-stuck — Faro

| Report | Action |
|---|---|
| Executor OK + Verifier APPROVE | Next step |
| APPROVE_WITH_DEBT | Register debt, next step |
| REQUEST_CHANGES M<3 | Re-dispatch Executor |
| REQUEST_CHANGES M=3 OR DISAGREEMENT_WITH_BLUEPRINT | **Gate B2** |
| REJECT | Escalate to the user |
| `requires_escalation_to_design: true` | **Gate B2** with proposal to launch workflow-design |
| Scope change | **Gate B3** |

---

## Healthy metrics

| Ratio | Target |
|---|---|
| Steps APPROVE in iter 1 | >70% |
| DISAGREEMENT_WITH_BLUEPRINT / total steps | 5-15% (if 0 → Designer too generic; if >25% → Designer did not read current docs) |
| Gate B2 triggered / integration | <20% |
| Verifiers with purely declarative criterion | 0% (non-negotiable) |

---

## Cost and performance

| Level | Duration | Tokens |
|---|---|---|
| trivial | <15 min | <30k |
| standard | 30-60 min | 80-200k |
| critical | 60-120 min | 200-400k |

---

## Input and output dependencies (information routing between workflows)

### Expected inputs (what this workflow consumes)

**Optional but very useful input**:
- **Investigation report** in `$FARO_ROOT/Informes/Investigacion/<YYYY-MM-DD>_<technology>.md` if the external technology was researched previously. Provides known antipatterns, problematic versions, hidden dependencies.
- **Prior integration reports** in `$FARO_ROOT/Informes/Integración/` for the same technology — to reuse the Install Blueprint if applicable.

For **critical** integration (with prior design): report in `$FARO_ROOT/Informes/Diseño/`.

**Precondition**: if integration is critical AND there is no design report → Faro launches `workflow-design` first. If there are only doubts about the technology and it is not critical, prior investigation can be omitted but the Designer will use their internal knowledge base.

### Output — final report archived by the Scribe

- **Obsidian destination folder**: `$FARO_ROOT/Informes/Integración/`
- **File name**: `<YYYY-MM-DD>_<technology_slug>.md`
- **Mandatory YAML frontmatter** — schema in `Escribano/CLAUDE.md`. For integration:
  ```yaml
  workflow: integracion
  version_workflow: "3.0"
  fecha: YYYY-MM-DD
  tecnologia: <human name>
  tecnologia_slug: <slug>
  version_tecnologia: <installed version>
  sesion_faro: $FARO_ROOT/Sesiones/<session>/
  informe_previo_consumido: "[[Investigación/YYYY-MM-DD_tecnología]]"  # or null
  nivel: standard | critical
  install_blueprint: <faro_session_path>/install_blueprint.md
  verificacion_funcional: PASS | PARTIAL | FAIL
  siguiente_workflow_sugerido: adaptacion | ninguno
  artefactos_faro:
    install_blueprint: <path>
    retrospectiva: <path>
  eco_memory_ids: [<ids>]
  eco_graph_origen: Integracion_<technology>_<date>
  tags: [workflow/integracion, estado/instalado, tecnologia/<slug>]
  ```
- **Mandatory "Traceability" section**: links to prior investigation (if any), to Install Blueprint, to Faro session, EcoDB, EcoDB graph.

### Typical next workflow

- **workflow-adaptation** if what was integrated needs to be customized for internal identities (Eco, Prima, Hilo, specific project) or active session.
- **none** if the integration is sufficient as-is and does not require adaptation to internal context.

---

## Version history

- **v4.0 (2026-05-22)**: relay rewrite. Migrated from Agent Teams to Relay. TeamCreate/SendMessage/TeamDelete → relay_join/peer dispatch/relay_leave. Python spawn code blocks removed. All Spanish text translated. Paths updated to $FARO_ROOT/ pattern. Agent names translated to English. EcoDB references updated.
- **v1.0**: first version with generic Designer, error knowledge base (ComfyUI/ElevenLabs/MCPs), Executor↔Verifier loop up to 3 iterations.
- **v2.0 (2026-04-18)**: hardening applying construction v3 methodology. Changes:
  1. **3 guiding principles** (do not improvise, external reality > Designer assumptions, "installed without errors" is NOT verification).
  2. **4 human gates** with literal options.
  3. **Install Blueprint minimum schema** (6 sections) with emphasis on FUNCTIONAL verification per step.
  4. **Physical artifact location** explicit.
  5. **Literal prompts** per step.
  6. **Pre-flight checks**.
  7. **Referenced templates** (INSTALL_BLUEPRINT new; ENV/CONTRACT/LESSONS shared).
  8. **Anti-stuck** per agent.
  9. **APPROVE_WITH_DEBT** from the Verifier.
  10. **Expanded knowledge base** with lessons from the 2026-04-18 session (eco_graph v2 → `claude_desktop_config.json`, pgvector, PyDiGraph, cp39-abi3 wheels).
  11. **Cross-validation** analogous to construction v3: "external system reality > Designer blueprint" — discrepancies are automatic BLOCKER.
  12. **Faro retrospective** at close.
- **v3.0 (2026-04-26)**: migration to Agent Teams. Teammates, SendMessage communication, explicit state table.
