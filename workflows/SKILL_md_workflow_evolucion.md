---
name: workflow-evolucion
description: |
  Orchestrated workflow for studying, improving, or refactoring tools and code that already exist in the system. Use it whenever the user asks to review, improve, optimize, refactor, audit, or analyze something already built — existing MCPs, scripts, configurations, current workflows. Also activates when the user says "this isn't working well", "it's slow", "it's messy", "needs cleanup", or "I want a second version of X". The difference from Construction is that here there is existing code to start from. The difference from Design is that here we go straight to modifying — if the task is critical, workflow-diseño is launched first to produce Brief+Spec+Plan.
metadata:
  version: "4.0"
  estreno_v1: 2026-04-16
  endurecido_v2: 2026-04-18
  agent_teams_v3: 2026-04-26
  autor_v3: Prima
  relay_rewrite: 2026-05-22
  invocation: relay session (separate Claude Code instance)
  motivo_endurecimiento: |
    Application of v3 workflow-construccion methodology to workflow-evolucion. v1 left too much inference to the model: no literal prompts, no explicit human gates, no minimum Audit Report schema, no cross-validation between current code and Auditor proposal, no physical artifact location, no retrospective.
tags:
  - agent/auditor
  - agent/executor
  - agent/verifier
  - agent/scribe
  - workflow/evolucion
---

# Workflow: Evolution (v4 — Relay)

Orchestrates improvement of existing systems. The starting point is always real code — analyze what exists, identify what to improve, and implement carefully to not break what works.

> **Guiding Principle 1 — No improvising**: Faro and sub-agents **do not infer well**. Every step, prompt, path, and format must be explicit. If when reading this skill you think "here I must decide how X is done" — stop and consult the user (gate).
>
> **Guiding Principle 2 — Verified behavior > Auditor proposal**: if the Auditor proposes changing something whose current behavior is correct and has users, **current behavior wins**. The Verifier detects regressions; a regression in a feature that worked is BLOCKER, not "evolution trade-off". Evolution improves specific things, does not reinvent what was already fine.
>
> **Guiding Principle 3 — Mandatory backup before any modification**: no change is made without backup of the current state. Not optional. The first task of any standard/critical evolution is always backup.

---

## When it activates

Faro launches this workflow when:
1. the user asks to modify/improve/audit code or configuration that already exists.
2. And the task has been classified as trivial / standard / critical.

Faro **does not** launch this workflow for:
- Building something that doesn't exist → workflow-construccion
- Connecting two existing systems → workflow-integracion
- Generating daily newspaper → workflow-periodico
- Bug with known cause and trivial fix → direct fix

---

## Complexity levels (objective criteria)

Classification is decided by **the user directly or Faro upon receiving the assignment** (never the Auditor — it is the one that sees problems, not the one that decides how much evolution is done).

| Level | Criteria (one suffices) | Action |
|-------|----------------------|--------|
| **trivial** | Isolated change <50 lines, no known side effects, single file | Light Auditor + Executor (no formal Verifier) |
| **standard** | Refactoring with regression tests needed, changes in multiple files but no schema | Auditor + Executor + Verifier |
| **critical** | Architectural change, touches schema, multiple interdependent files, system with real users | **workflow-diseño first**, then this workflow with resulting Plan |

If doubtful → Faro asks the user.

---

## The 4 human gates (mandatory)

**Golden rule**: options with complete literal text, never A/B/C.

### Gate B0 — Load confirmation

**When**: after receiving assignment, before dispatching to the first agent.

```
[GATE B0 — Load confirmation]
I have loaded workflow-evolucion v4.

Assignment received: <1-2 sentence summary>
System to evolve: <path/name>
Classified level: <trivial | standard | critical>

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones\<YYYY-MM-DD>_<project>_evolucion\
- Project folder (reports): <project path>\.faro\reportes_evolucion\
- Agents (in order):
    1. Auditor (Designer in Auditor mode) — reads current code and produces Audit Report
    2. Executor (after Gate B1 backup, and per proposed change)
    3. BLIND Verifier (after each change, standard/critical)
    4. Scribe (at the end)

Subsequent gates:
- B1 before any destructive change OR before starting modifications (mandatory backup)
- B2 if Auditor detects a problem requiring a more detailed Plan → escalate to workflow-diseño
- B3 if the user requests scope change during evolution

Options:
- "Proceed" — start with physical setup and Step 1 (audit).
- "Adjust X" — describe what to adjust before proceeding.
- "Do not proceed" — cancel without touching anything.

What do I do?
```

### Gate B1 — Before destructive modifications

**When**: before any task that modifies existing code, schema, production configuration, or files that cannot be trivially restored. Also fires before the first modification (ensure backup).

```
[GATE B1 — Imminent modification]
Change N: <change title>
Affected files: <list>
Backup done: <backup path | "pending — doing it now">
Rollback defined: <exact command>
Non-regression criteria: <what must keep working>
Verifier will validate: <concrete list>

Options:
- "Proceed" — apply the change now.
- "Stop the workflow" — stop here without touching anything else.
- "Review X first" — describe what to verify before proceeding.

What do I do?
```

### Gate B2 — Escalation to workflow-diseño or Audit Report modification

**When**: any of:
- Auditor detects that the real scope exceeds what a simple evolution can resolve (requires formal Brief + Spec + Plan)
- 3 Executor↔Verifier iterations fail for a change AND the Verifier identifies that the problem is with the Audit Report, not the Executor
- Conflict detected between "verified current behavior" and "Auditor proposal" (guiding principle 2)

```
[GATE B2 — Evolution needs more design OR Audit Report requires modification]
Reason: <"complexity detected during audit" | "3 failed iterations" | "conflict with verified behavior">
Change N: <title>
Diagnosis: <what Auditor/Verifier detected>
Proposal: <"launch workflow-diseño to produce Brief+Spec+Plan" | "modify Audit Report at X" | "accept current behavior and discard the change">
Impact on subsequent changes: <list or "none">

Options:
- "Launch workflow-diseño first" — pause this evolution, execute workflow-diseño, resume with resulting Plan.
- "Modify the Audit Report per proposal" — update the Report and resume.
- "Discard this change and continue with the others" — change stays as DEFERRED, not applied.
- "Abort the entire workflow" — stop and review manually.

What do I do?
```

### Gate B3 — Scope change during execution

**When**: the user decides during the workflow to add, remove, or modify the evolution scope.

```
[GATE B3 — Scope change detected]
the user's request: <literal description>
Completed changes: <list>
Impact on Audit Report: <"still valid" | "invalidates X" | "requires re-audit">

Options:
- "Apply the change" — Faro integrates the new scope into the Audit Report; if it invalidates, relaunches Step 1.
- "Defer it until after the current evolution" — stays as backlog.
- "Cancel the request" — continue with original scope.

What do I do?
```

---

## System agents — Relay (v4.0, 2026-05-22)

Each workflow uses **relay peers** (separate Claude Code sessions). The lead coordinates via peer dispatch.

### Team structure

```
join coordination room

RELAY PEERS (persistent, bidirectional via peer dispatch):
├── Auditor (OPUS) — reads existing code, identifies problems, proposes changes,
│                    coordinates the workflow. Is the lead here — knows the code.
├── Executor (Sonnet) — implements changes with backup, reports to Auditor
├── Code_Adversarial (Sonnet) — reviews quality of modified code post-changes
├── Verifier (Sonnet) — beta tester: regressions, functional, stress
└── Investigator (Haiku) — standby for on-demand research

EPHEMERAL:
└── Scribe (Sonnet) — archives at close

LEAD (Prima):
└── Gates, final decisions, escalation to workflow-diseño if critical.
```

### Agent table

| Agent | Type | Model | CLAUDE.md | Mode |
|--------|------|--------|-----------|------|
| **Auditor** | Relay peer | **Opus** | `Designer/CLAUDE.md` | Auditor |
| **Executor** | Relay peer | Sonnet | `Executor/CLAUDE.md` | — |
| **Code_Adversarial** | Relay peer | Sonnet | `Code_Adversarial/CLAUDE.md` | — |
| **Verifier** | Relay peer | Sonnet | `Verifier/CLAUDE.md` | Beta tester |
| **Investigator** | Relay peer | Haiku | `Investigator/CLAUDE.md` | Standby |
| **Scribe** | Ephemeral | Sonnet | `Scribe/CLAUDE.md` | — |

### Direct communication

```
AUDIT PHASE:
Auditor reads code → produces Audit Report → idle notification to Prima
dispatch task to Investigator  # if point research needed

CHANGES PHASE (per each change in Audit Report):
dispatch task to Executor
dispatch task to Auditor  # Executor reports back
Auditor: reviews change (has context of original code)

POST-CHANGE REVIEW PHASE:
dispatch task to Code_Adversarial
dispatch task to Auditor  # Code_Adversarial reports back

TEST PHASE:
dispatch task to Verifier
dispatch task to Auditor  # Verifier reports back
Auditor consolidates → peer dispatch to Prima with summary

DECIDE:
Auditor + Prima evaluate findings
Prima prevails → the user if unresolved
```

### Chain of command (non-negotiable)

- **the user**: product decisions (gates, scope).
- **Prima (lead)**: final technical decisions, escalation to workflow-diseño.
- **Auditor (Opus)**: coordinates the workflow, decides what to change and in what order. Knows the code — is the evolution team lead.
- **Executor/Code_Adversarial/Verifier**: execute and report. Do not decide scope.

### Relay peer state by phase

| Phase | Auditor | Executor | Code_Adversarial | Verifier | Investigator |
|---|---|---|---|---|---|
| Audit | **working** | idle | idle | idle | standby |
| Changes | supervising | **working** | idle | idle | standby |
| Code review | coordinating | idle | **working** | idle | standby |
| Regression test | coordinating | idle | idle | **working** | standby |
| Decide | **working** + Prima | idle | idle | idle | standby |
| Fix | supervising | **working** | idle | idle | standby |
| Close | leave | leave | leave | leave | leave |

**Cost of idle relay peers**: zero tokens.

**No Security_Adversarial**: evolution is tactical improvement, not building from scratch. If the evolution is critical (touches schema, architecture) → goes to workflow-diseño first, where there is a full adversarial.

---

## Initial setup — file structure

### 1. Session folder

```
$FARO_ROOT/Sesiones\<YYYY-MM-DD>_<project>_evolucion\
  ├── ENVIRONMENT.md     ← copied from Templates/ENVIRONMENT_template.md and filled in
  ├── CONTRACT.md        ← copied from Templates/CONTRACT_template.md
  ├── LESSONS.md         ← copied from Templates/LESSONS_template.md
  └── orchestration.md
```

### 2. Project folder (reports + backups)

```
<project>\
  ├── archive\                              ← pre-evolution backups
  │     └── <file>.pre_evolucion_<date>
  └── .faro\
        └── reportes_evolucion\
              ├── audit_report.md
              ├── ejecutor_cambio_<N>_iter_<M>.md
              ├── verificador_cambio_<N>_iter_<M>.md
              └── escribano_cierre.md
```

### 3. Referenced templates

- `$FARO_ROOT/Plantillas\AUDIT_REPORT_template.md` (new, evolution-specific)
- `$FARO_ROOT/Plantillas\ENVIRONMENT_template.md` (shared)
- `$FARO_ROOT/Plantillas\CONTRACT_template.md` (shared with construction, adapting "task" → "change")
- `$FARO_ROOT/Plantillas\LESSONS_template.md` (shared)
- `$FARO_ROOT/Plantillas\PLAN_template.md` (shared, if escalated to critical)

---

## Minimum Audit Report schema

Every Audit Report produced by the Auditor must have these sections:

```
# Audit Report — <system/project>

## Metadata
- Audited system: <path>
- Audit date: <YYYY-MM-DD>
- Current version read: <git hash / mtime / N lines>
- Auditor: Designer-Opus in Auditor mode

## 1. Verified current state
- What works (behavior that must NOT be lost): concrete list with command/test that validates it
- How it is used today: list of known integrations/users
- Current metrics (if applicable): performance, counters, etc.

## 2. Detected problems
Per problem:
- P<N>: <description>
  - Evidence: <command/observation that confirms it>
  - Severity: critical | medium | low
  - Impact if unresolved: <what happens>

## 3. Proposed changes
Per change:
- C<N>: <description>
  - Resolves: [P1, P2]
  - Files to touch: <list>
  - Type: refactor | optimization | cleanup | fix | feature
  - Risk: low | medium | high
  - Regression tests needed: <list>
  - Rollback: <command or "restore from archive/">

## 4. Suggested application order
[C3, C1, C2, ...] — with reason for order (dependencies).

## 5. What NOT to touch
Explicit list of code/files that must NOT be modified even if they look improvable — because they are in active use or have hidden dependencies.

## 6. Global success criteria
Verifiable bullets the Verifier will use at the end:
- [ ] <criterion> verifiable with <command>
```

If any of the 6 sections is missing, Faro returns the Audit Report to the Auditor before dispatching to the Executor.

---

## Workflow flow (step by step, literal prompts)

### Step 0: Faro validates and prepares

1. Receives assignment.
2. Determines level. If critical → launches workflow-diseño first; this workflow resumes with resulting Plan.
3. Pre-flight checks:
   - Project exists on disk
   - Space available for backups (>10x project size)
   - Git or equivalent available to revert
   - EcoDB accessible (to query prior patterns via `search` tool)
4. Creates session folder and `.faro/reportes_evolucion/` + `archive/` in the project.
5. **Gate B0**.

### Step 1: Auditor

Literal prompt (after injecting Designer's CLAUDE.md):

```
<Designer/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Auditor (Designer in Auditor mode)]

Workflow: evolucion v4
System to audit: <path>
the user's assignment (literal): <text>
Level: <trivial | standard | critical>

Your task (only this, nothing else):

1. **Query EcoDB** (`search` tool) with domain tags (author='*'):
   - <suggested tags>
   Note prior lessons about this system or similar systems.

2. **Read the current code in its entirety** — not what you remember, today's. Do not move to proposing changes before reading. If the system is large (>1000 lines), read critical sections first and make clear what you did NOT read.

3. **Document the verified current state**:
   - Run commands/tests that confirm what works today.
   - Identify integrations (imports, calls, known consumers).
   - If there are existing tests, run them and capture literal output.

4. **Identify problems** with concrete evidence — not impressions ("this could be better"). Each problem with command/observation that confirms it.

5. **Propose concrete changes** with evaluated risk. For each change, include what regression tests are needed (guiding principle 2: current working behavior must NOT be broken).

6. **Identify what NOT to touch**: code with hidden dependencies or active users that must not be modified even if they look improvable.

7. **Write the Audit Report** meeting the minimum schema (6 sections):
   - Template: `$FARO_ROOT/Plantillas\AUDIT_REPORT_template.md`
   - Save it at: `<project>\.faro\reportes_evolucion\audit_report.md`

8. **If you detect that the real scope exceeds a standard evolution** (requires new schema, major architectural change, or formal Spec) → mark `requiere_escalacion_a_diseño: true` in the Audit Report and do NOT propose architectural changes here. Faro will fire Gate B2.

Return to me:
- Audit Report path
- Summary: N problems detected, M changes proposed, flag `requiere_escalacion_a_diseño`
- Pre-commitment: "I have delivered the Audit Report. I will not make modifications until Faro dispatches the Executor with specific changes."
```

### Step 2: Executor (per each change in Audit Report, in order)

For each change `C<N>`:

**Step 2.0** — If the change is destructive or is the first in the workflow → **Gate B1** (confirmation + backup).

**Step 2.1** — Executor receives literal prompt:

```
<Executor/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Executor, Change <N> iter <M>]

Session: <path>
Iteration: <M> of maximum 3

Before touching anything:
1. Read ENVIRONMENT.md, LESSONS.md, CONTRACT.md
2. Confirm there is a backup in `<project>\archive\` (if not, do backup now — guiding principle 3 is non-negotiable)

Change to apply (literal from Audit Report):
<C<N> block from Audit Report>

Implement ONLY this change. Do NOT touch files outside the list. Do NOT take the opportunity to "also clean up this other thing" — any additional change must be in the Audit Report as a separate change.

When done:
1. Run the regression tests specified in the change.
2. Generate EXECUTOR_REPORT (format in CONTRACT.md) and save it at:
   `<project>\.faro\reportes_evolucion\ejecutor_cambio_<N>_iter_<M>.md`

If you detect that the Audit Report change has a defect (e.g. the file/function it asks to touch doesn't exist):
- STATUS = DISAGREEMENT_WITH_AUDIT_REPORT
- Describe the conflict, do NOT modify anything on your own.
```

**Step 2.2** — BLIND Verifier (standard and critical):

```
<Verifier/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Verifier (Change <N>, iter <M>)]

Your attitude: you want to see the system burn. Adversarial but loyal.

YOU DO NOT HAVE ACCESS to the Executor's report. You only receive:
- ENVIRONMENT.md
- The change from the Audit Report (objective, affected files, regression tests, success criteria)
- Access to the current code state

**Your main job (guiding principle 2)**:
1. **Detect regressions**: does what worked before still work? Run the Audit Report's regression tests. Also actively search for collateral behaviors the Audit Report might not have listed but that you'd expect as a user.
2. **Verify the original problem is resolved**: does the change do what it said it would?
3. **Detect new bugs**: the change might introduce problems that didn't exist before.

Generate VERIFIER_REPORT (dual markdown-INI + JSON format, includes `APPROVE_WITH_DEBT` when applicable) at:
`<project>\.faro\reportes_evolucion\verificador_cambio_<N>_iter_<M>.md`

HARD INVARIANT: if you detect regression in behavior that worked before → verdict = REQUEST_CHANGES or REJECT (non-negotiable; guiding principle 2 says verified behavior beats proposal).
```

**Step 2.3** — Supervisor (implicit: Faro in this workflow has no separate Supervisor) processes verdict:

| verdict | action |
|---|---|
| APPROVE | Mark change completed, move to next Audit Report change |
| APPROVE_WITH_DEBT | Same + record debt_items in `<project>\.faro\debt_backlog.md` |
| REQUEST_CHANGES M<3 | Re-dispatch Executor with required_fixes |
| REQUEST_CHANGES M=3 | **Gate B2** |
| REJECT | Escalate to the user |

### Step 3: Scribe + Faro Retrospective

When all changes are in APPROVE or the workflow has been closed:

**Scribe** (literal prompt analogous to construction v3):
- Obsidian: `$FARO_ROOT/Informes\Evolución\<Name>_v<N>_<YYYY-MM-DD>.md`
- Minimum content: before/after, applied changes, detected and resolved regressions, Auditor decisions, fired gates, metrics
- EcoDB (`save_memory` tool, author: "Scribe"): 1-2 memories <500 words each
- EcoDB graph (`save_triples_batch` tool): triples `<system> evolved_to <version>`, `<change N> resolved <problem N>`, etc.

**Faro Retrospective** (no agent): 10-15 lines in `$FARO_ROOT/Sesiones\...\retrospective.md` with what worked, what was improvised, real metrics, changes for v+1.

---

## Anti-stuck protocols

### Anti-stuck — Auditor (new in v2)

If the Auditor returns an Audit Report without the "what NOT to touch" section or with 0 detected problems, Faro injects:

> *"The Audit Report is incomplete. A system that genuinely has nothing to improve is rare — if you truly see nothing, put that as a finding and explain why. And the 'what not to touch' section is mandatory: if you don't identify untouchable zones, the Executor might take the opportunity to 'clean up' something with active users."*

### Anti-stuck — Verifier

If the Verifier returns APPROVE with 0 blockers/warnings/nits for a critical-level change, Faro injects:

> *"A critical change without observations is suspicious. Check specifically: (1) did you run the Audit Report's regression tests?, (2) did you test edge cases?, (3) did you look for collateral behaviors not listed in the Audit Report? If after that review you're still at clean APPROVE, justify it in REVIEW_SUMMARY."*

### Anti-stuck — Executor

If the Executor applies a change not listed in the Audit Report, Faro detects it and returns:

> *"You have modified files outside the scope of Change <N>. Revert the extra changes or escalate them as DISAGREEMENT_WITH_AUDIT_REPORT. We do not accept scope creep in the Executor."*

### Anti-stuck — Faro itself

| Report | Action |
|---|---|
| `VERDICT: APPROVE` | Move to next Audit Report change |
| `VERDICT: APPROVE_WITH_DEBT` | Record debt, next change |
| `VERDICT: REQUEST_CHANGES` M<3 | Re-dispatch Executor with fixes |
| `VERDICT: REQUEST_CHANGES` M=3 | **Gate B2** |
| `VERDICT: REJECT` | Escalate to the user |
| `STATUS: DISAGREEMENT_WITH_AUDIT_REPORT` | Investigate; if confirms defect → **Gate B2** |
| `requiere_escalacion_a_diseño: true` in Audit Report | **Gate B2** with proposal to launch workflow-diseño |
| User scope change request | **Gate B3** |

---

## Healthy metrics

| Ratio | Target |
|---|---|
| Changes in iter 1 APPROVE | >60% |
| Regressions detected by Verifier | 0.1-0.3 per change (if 0 always → lax Verifier; if >0.5 → Audit Report was incomplete) |
| Changes escalated to Gate B2 | <15% |
| DISAGREEMENT_WITH_AUDIT_REPORT / total changes | 0-10% (if >10% → Auditor is not reading real code) |

---

## Cost and performance

| Level | Duration | Tokens |
|-------|----------|--------|
| trivial | <15 min | <30k |
| standard | 45-90 min | 120-250k |
| critical | workflow-diseño first + execution — varies by complexity |

---

## Input and output dependencies (information routing between workflows)

### Expected inputs (what this workflow consumes)

**Mandatory input**: the existing code to be evolved (starting point, workflow principle).

**Optional useful input**:
- **Prior construction report** at `$FARO_ROOT/Informes\Construcción\<YYYY-MM-DD>_<project>.md` — to understand code origin, decisions made, accepted debt.
- **Prior evolution reports** for the same project at `$FARO_ROOT/Informes\Evolución\` — to avoid repeating already done refactors or breaking invariants assumed in prior iterations.
- **Investigation report** at `$FARO_ROOT/Informes\Investigacion\` if evolution requires external research on alternatives.

For **critical** evolution (with prior design): same contract as critical construction — Brief+Spec+Plan from workflow-diseño at `$FARO_ROOT/Informes\Diseño\` + raw artifacts in the project.

**Precondition**: if the task is critical and there is NO prior design report → Faro launches `workflow-diseño` first.

### Output — final report archived by Scribe

- **Obsidian destination folder**: `$FARO_ROOT/Informes\Evolución\`
- **File name**: `<YYYY-MM-DD>_<project_slug>.md`
- **Mandatory YAML frontmatter** — schema in `Scribe/CLAUDE.md`. For evolution:
  ```yaml
  workflow: evolucion
  version_workflow: "4.0"
  fecha: YYYY-MM-DD
  proyecto: <human name>
  proyecto_slug: <slug>
  sesion_faro: $FARO_ROOT/Sesiones\<session>\
  informe_previo_consumido: "[[Construcción/YYYY-MM-DD_proyecto]]"  # or [[Evolución/...]] if prior iterations, or null
  nivel: standard | critical
  cambios_aplicados: N
  regresiones_detectadas: 0  # MUST be 0 per guiding principle 2
  siguiente_workflow_sugerido: evolucion | ninguno  # if evolucion, for next iteration
  artefactos_faro:
    audit_report: <project_path>/audit_report_v<N>.md
    backup: <project_path>/archive/<timestamp>/
    retrospectiva: <faro_session_path>/retrospective.md
  eco_memory_ids: [<ids>]
  eco_graph_origen: Evolucion_<project>_<date>
  tags: [workflow/evolucion, estado/cerrado, proyecto/<slug>]
  ```
- **Mandatory "Traceability" section**: links to prior construction/evolution report, Audit Report, backup, Faro session, EcoDB, EcoDB graph.

### Typical next workflow

- **workflow-evolucion** (subsequent iteration) if new needs arise.
- **none** if the evolution covers the stated scope.

---

## Version history

- **v1.0**: first version with Designer-Auditor, JSON blueprint, Executor↔Verifier loop, Plan Reviewer in critical. Expected intensive use for existing MCPs.
- **v2.0 (2026-04-18)**: hardening applying v3 construction methodology. Changes:
  1. **3 explicit guiding principles** (no improvising, verified behavior > Auditor proposal, mandatory backup).
  2. **4 human gates** with literal options (B0 load, B1 destructive modification, B2 escalation to design or Audit Report modification, B3 scope change).
  3. **Minimum Audit Report schema** formalized (6 mandatory sections).
  4. **Explicit physical artifact location**.
  5. **Literal prompts** for each dispatch.
  6. **Pre-flight checks** before Step 1.
  7. **Referenced templates** (new AUDIT_REPORT; shared ENVIRONMENT/CONTRACT/LESSONS/PLAN).
  8. **Anti-stuck** per agent (Auditor, Executor, Verifier, Faro).
  9. **APPROVE_WITH_DEBT** in Verifier verdicts.
  10. **Cross-validation** analogous to construction v3: "verified behavior > Auditor proposal" — regressions are automatic BLOCKER, non-negotiable.
  11. **Faro Retrospective** at close.
  12. **Explicit escalation to workflow-diseño** when Auditor detects that complexity exceeds a simple evolution.
- **v3.0 (2026-04-26)**: migration to Agent Teams by Prima. Auditor Opus, Executor Sonnet, Verifier Sonnet as persistent teammates. Haiku Investigator on standby. Direct communication. Explicit chain of command. Escalation to workflow-construccion for bridges.
- **v4.0 (2026-05-22)**: relay rewrite. Agent Teams → Relay. bisagra → gate. eco_memory/eco_graph → EcoDB. Agent name translations applied. Python spawn blocks removed. All content translated to English.
