---
name: workflow-diseno-profundo
description: >
  Multi-model deep design workflow. Iterative refinement with external counselors
  (Opus 4.8, DeepSeek v4 Pro, Codex/ChatGPT) and independent adversarials.
  Minimum 3 full rounds before approval. Use for high-stakes designs where
  single-model blind spots are unacceptable: flagship products, public-facing
  systems, architectures that must survive external scrutiny.
metadata:
  version: "1.2"
  creation: "2026-06-29"
  author: "Prima + Hilo (flow) + Lienzo (escalation) + Eco (counselor voice)"
  base: "workflow-diseno v4.0"
invocation: "relay session (separate Claude Code instance)"
tags:
  - workflow/deep-design
  - agent/architect
  - agent/design_counsellor
  - agent/design_adversarial
  - proyecto/faro
  - estado/activo
---

# Workflow: Deep Design (v1.2 — Multi-Model Iterative)

Orchestrates an iterative design phase with external multi-model counsel and adversarial validation. Produces Brief + Spec + Plan that have survived minimum 3 rounds of external scrutiny across different AI models.

> **Guiding principle 1 — Do not improvise**: identical to workflow-design v4. Every step, prompt, path, and format must be explicit.
>
> **Guiding principle 2 — Three layers, not two**: this workflow separates internal design (Coordinator/Architect), external counsel (Counselors — improve), and adversarial attack (Adversarials — destroy). The Coordinator designs. The Counselors strengthen. The Adversarials break. Never confuse the three roles.
>
> **Guiding principle 3 — Escalation is structural, not emotional**: each round changes the LENS (what to examine), the THRESHOLD (minimum severity to report), and the TONE (how to communicate). The Counselor's personality does not change — the assignment does.
>
> **Guiding principle 4 — Quorum over perfection**: external models are unreliable. Minimum 2 of 3 counselors must respond to proceed. Design for partial input, not for perfect consensus.
>
> **Guiding principle 5 — No shortcuts in deep design**: adversarials must issue APPROVE (not APPROVE_WITH_DEBT) on the Brief before moving to Spec+Plan. On Spec+Plan, APPROVE_WITH_MINOR_DEBT is acceptable only for implementation-level items, never for design-level items.
>
> **Guiding principle 6 — Vision Keeper is optional**: if a `vision_<project>.md` document exists and a Vision_keeper session is available, the Coordinator sends the deliverable for review before each gate. If neither exists, the workflow proceeds without it — the user acts as vision keeper at the gates.

---

## When it activates

This workflow replaces workflow-design when:
1. The task is **high-stakes**: flagship product, public-facing system, architecture that must survive external scrutiny.
2. the user explicitly requests deep design.
3. Single-model blind spots are unacceptable (the whole point of multi-model counsel).

This workflow is **overkill** for:
- Standard refactors → use workflow-design v4
- Trivial tasks → direct to workflow-construction
- Tasks where speed matters more than depth → use workflow-design v4

---

## Three-layer architecture

```
LAYER 1 — INTERNAL (Coordinator/Architect)
├── Writes Brief, Spec, Plan
├── Incorporates counsel
├── Applies adversarial fixes
└── Owns the deliverables

LAYER 2 — EXTERNAL COUNSEL (Counselors — IMPROVE)
├── Opus 4.8 (Claude Code + EcoRelay)
├── DeepSeek v4 Pro (Claude Code + DeepSeek API + EcoRelay)
└── Codex/ChatGPT (ecorelay-codex.cmd + EcoRelay)

LAYER 3 — ADVERSARIAL (Adversarials — DESTROY)
├── DeepSeek Adversarial (Claude Code + DeepSeek API + EcoRelay)
└── Opus Adversarial (Claude Code + EcoRelay)
```

Counselors and Adversarials are INDEPENDENT of each other. A model that counsels in Layer 2 does NOT attack in Layer 3 (different session, different peer ID, different role).

---

## Round structure (minimum 3)

Each round follows: **Counselors → Coordinator incorporates → Adversarials attack → Coordinator corrects**

### Escalation model (Lienzo+Hilo fusion)

| Round | Lens | Tone | Threshold | Guiding question |
|-------|------|------|-----------|-----------------|
| 1 | **PREMISE** | Constructive | CRITICAL only | Is this the right problem? |
| 2 | **SOLUTION** | Demanding | CRITICAL + HIGH | Is this the right solution? |
| 3+ | **CRAFT** | Hostile-constructive | CRITICAL + HIGH + MEDIUM | Is this the best possible version? |

Each round accepts what previous rounds validated and attacks deeper. The Counselor does not revisit settled decisions — they advance the lens.

### Round context block (injected in every counselor dispatch)

```
ROUND_CONTEXT:
  round: {N}/3+
  lens: {PREMISE | SOLUTION | CRAFT}
  tone: {constructive | demanding | hostile-constructive}
  threshold: {CRITICAL | CRITICAL+HIGH | CRITICAL+HIGH+MEDIUM}
  validated_assumptions: {list of what passed previous rounds}
  guiding_question: {the question for this round}
```

### Exit condition

- **Brief**: ALL adversarials issue `VERDICT: APPROVE` (no debt). Minimum 3 rounds.
- **Spec+Plan**: ALL adversarials issue `VERDICT: APPROVE` or `VERDICT: APPROVE_WITH_MINOR_DEBT` (implementation-level items only, no design-level debt). Minimum 2 rounds.
- **Plan execution-readiness (v1.2)**: additionally, EVERY Plan task must pass the 9-field execution schema (see Step 6 + the gate below). A Plan approved on design merit but lacking per-task execution fields does NOT exit — it is not construction-ready.

### Plan execution-readiness gate (v1.2 — MANDATORY, non-skippable)

**Origin**: KnowTwin (2026-06-30 deep design → 2026-07-01 construction). The Plan passed all adversarial rounds and both full-team sweeps, then arrived at workflow-construccion as a week-by-week roadmap table (ID / Task / Description / Dependencies / Effort / Verification) with NO per-task execution fields. Construction had to STOP and reconstruct the 9-field schema task-by-task with the build team before a line of code could be written. The adversarials reviewed design correctness — nobody owned "can construccion execute this Plan as-is?"

**The gate** fires after Spec+Plan adversarial APPROVE and the full-team sweep, BEFORE Gate B4. The Coordinator verifies, task by task, that the Plan conforms to the 9-field execution schema. For EVERY task:
- [ ] objetivo, archivos_a_tocar, accion, pre_condiciones, post_condiciones, tests, criterio_de_exito, rollback, depende_de — all present and non-empty
- [ ] archivos_a_tocar lists concrete paths (not "the relevant files")
- [ ] tests + criterio_de_exito are empirically verifiable (a machine could check them)
- [ ] no time/effort estimate is presented as a Plan input (banned as a scoping unit)

If ANY task fails, the Plan is NOT ready. The Coordinator expands the failing tasks — dispatching the build/execution team to read real source when the detail requires it — and re-runs the gate. Only a Plan where all tasks pass reaches Gate B4.

**Handoff assertion**: Gate B4 must state explicitly "Plan is construction-ready: N/N tasks conform to the 9-field execution schema." If it can't, it doesn't gate.

---

## System agents — Relay

### Team structure

```
join coordination room

PERSISTENT RELAY PEERS:
├── Coordinator/Architect (Opus) — designs, incorporates, corrects. Same agent, same session.
├── Design_Adversarial_Opus (Opus 4.8) — adversarial attack, persistent between rounds
├── Design_Adversarial_DeepSeek (DeepSeek v4 Pro) — adversarial attack, persistent between rounds
├── Design_Counsellor_Opus (Opus 4.8) — external counsel, persistent between rounds
├── Design_Counsellor_DeepSeek (DeepSeek v4 Pro) — external counsel, persistent between rounds
├── Design_Counsellor_Codex (ChatGPT via Codex) — external counsel, persistent between rounds
└── Vision_keeper (Sonnet) — OPTIONAL. Reviews against vision document if available.

ON-DEMAND:
├── Investigator (Haiku) — research service for any peer
└── Archivist (Haiku) — pre-flight / post-flight

ONE-SHOT:
└── Scribe (Sonnet) — archives at close
```

### Agent table

| Agent | Type | Model | CLAUDE.md | Launcher |
|-------|------|-------|-----------|----------|
| **Coordinator/Architect** | Lead + Relay peer | Opus | `Architect/CLAUDE.md` | (orchestrator session) |
| **Design_Counsellor_Opus** | Relay peer | Opus 4.8 | `Design_Counsellor/CLAUDE.md` | `Design_Counsellor/start_opus.bat` |
| **Design_Counsellor_DeepSeek** | Relay peer | DeepSeek v4 Pro | `Design_Counsellor/CLAUDE.md` | `Design_Counsellor/start_deepseek.bat` |
| **Design_Counsellor_Codex** | Relay peer | ChatGPT (Codex) | `Design_Counsellor/CLAUDE.md` | `ecorelay-codex.cmd` |
| **Design_Adversarial_Opus** | Relay peer | Opus 4.8 | `Design_Adversarial/CLAUDE.md` | `Design_Adversarial/start.bat` |
| **Design_Adversarial_DeepSeek** | Relay peer | DeepSeek v4 Pro | `Design_Adversarial/CLAUDE.md` | `Design_Adversarial/start_deepseek.bat` |
| **Vision_keeper** | Relay peer (optional) | Sonnet | `Vision_keeper/Claude.md` | — |
| **Investigator** | Relay peer (on-demand) | Haiku | `Investigator/CLAUDE.md` | — |
| **Archivist** | One-shot | Haiku | `Archivist/CLAUDE.md` | — |
| **Scribe** | One-shot | Sonnet | `Scribe/CLAUDE.md` | — |

### Counselor communication protocol

1. Coordinator dispatches to all 3 counselors in PARALLEL via peer dispatch
2. **Dispatch order**: Codex/ChatGPT FIRST (most likely to timeout), then DeepSeek, then Opus. All run concurrently — dispatch order is launch priority, not sequencing
3. Each counselor writes analysis to `<session>/consejeros/round_N/<peer_id>.md`
4. Each counselor replies via peer dispatch with a summary
5. **Timeout**: 10 minutes per counselor
6. **Quorum**: minimum 2 of 3 must respond to proceed
7. If only 1 responds → wait one more timeout cycle, then proceed with available + log gap
8. If 0 respond → Gate B2 (escalate to the user)
9. Coordinator documents which counselor was absent and why

### Adversarial communication protocol

1. Coordinator dispatches to both adversarials in PARALLEL via peer dispatch
2. Each adversarial writes report to `<session>/adversarial/round_N/<peer_id>.md`
3. Both adversarials must respond (no quorum — both are required)
4. If one adversarial times out → retry once, then escalate to the user

---

## The 5 human gates

### Gate B0 — Workflow load confirmation

```
[GATE B0 — Deep Design load confirmation]
I have loaded workflow-deep-design v1.0.

Task received: <1-2 sentence summary>
Project: <project path>

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>_deep_design/
- Final deliverables: <project path>/
- Agent reports: <session>/consejeros/ and <session>/adversarial/
- External models: Opus 4.8, DeepSeek v4 Pro, Codex/ChatGPT
- Minimum rounds: 3 (Brief) + 2 (Spec+Plan)
- Vision_keeper: <available | not available — the user acts as vision keeper>

Agents to launch:
  Counselors: 3 (Opus 4.8, DeepSeek v4 Pro, Codex)
  Adversarials: 2 (Opus 4.8, DeepSeek v4 Pro)
  Investigator: on standby
  Archivist: pre-flight then post-flight

Options:
- "Proceed" — I start with setup and Step 0.5 (Archivist pre-flight).
- "Adjust X" — describe modifications.
- "Do not proceed" — I cancel without touching anything.

What should I do?
```

### Gate B1 — Brief approval (after minimum 3 rounds)

```
[GATE B1 — Brief approval (Deep Design)]
Project: <name>
Brief final version: <path>
Rounds completed: <N>

Round history:
- Round 1 (PREMISE): <counselors responded> / <adversarial verdict>
- Round 2 (SOLUTION): <counselors responded> / <adversarial verdict>
- Round 3 (CRAFT): <counselors responded> / <adversarial verdict>
[- Round N: ...]

Final adversarial verdicts:
- Opus Adversarial: <APPROVE | REQUEST_CHANGES>
- DeepSeek Adversarial: <APPROVE | REQUEST_CHANGES>

Accumulated metrics:
- Total counselor recommendations: N (applied: X, deferred: Y)
- Total adversarial observations: N (applied: X, deferred: Y, escalated: Z)

Options:
- "I approve Brief — proceed with Spec+Plan"
- "More rounds before approving" — specify what needs more work
- "I approve Brief — close here" — stop at Brief without Spec+Plan
- "Reject — redesign from scratch"

What should I do?
```

### Gate B2 — Escalated items or infrastructure failure

Same format as workflow-design v4 Gate B2, extended with counselor failure reporting.

### Gate B3 — Scope change during design

Same as workflow-design v4 Gate B3.

### Gate B4 — Spec+Plan approval (after minimum 2 rounds)

```
[GATE B4 — Spec+Plan approval (Deep Design)]
Project: <name>
Spec final version: <path>
Plan final version: <path>
Rounds completed: <N>
Plan execution-readiness: <N/N tasks conform to 9-field execution schema | NOT READY — cannot gate>

Final adversarial verdicts:
- Opus Adversarial: <APPROVE | APPROVE_WITH_MINOR_DEBT>
- DeepSeek Adversarial: <APPROVE | APPROVE_WITH_MINOR_DEBT>

Minor debt (if any):
<list of implementation-level items deferred>

Options:
- "I approve Spec+Plan — proceed to execution workflow"
- "More rounds"
- "Reject — redesign Spec+Plan from Brief"

What should I do?
```

---

## Initial setup — file structure

### Session folder

```
$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>_deep_design/
  ├── CONTRACT.md
  ├── LESSONS.md
  ├── orchestration.md
  ├── consejeros/
  │     ├── round_1/
  │     │     ├── opus_48.md
  │     │     ├── deepseek.md
  │     │     └── chatgpt.md
  │     ├── round_2/
  │     └── round_3/
  └── adversarial/
        ├── round_1/
        │     ├── opus_adv.md
        │     └── deepseek_adv.md
        ├── round_2/
        └── round_3/
```

### Project folder (final deliverables)

```
<project_path>/
  ├── deep_design_v<N>_brief.md
  ├── deep_design_v<N>_spec.md
  ├── deep_design_v<N>_plan.md
  ├── verification_checkpoint.md
  └── .faro/
        └── reportes_diseno_profundo/
              ├── investigador_report.md
              ├── consejero_consolidado_round_N.md
              └── adversarial_consolidado_round_N.md
```

---

## Workflow flow (step by step)

### Step 0: Coordinator validates and prepares

Identical to workflow-design v4 Step 0 + creates `consejeros/` and `adversarial/` subfolders.

### Step 0.5: Archivist pre-flight (MANDATORY)

Identical to workflow-design v4. Search EcoDB for prior knowledge before external research.

### Phase 1 — Brief (minimum 3 rounds)

#### Step 1: Coordinator prepares brief of questions

Identical to workflow-design v4 Step 1. Coordinator searches EcoDB, identifies 4-8 questions for the Investigator.

#### Step 2: Investigator

Identical to workflow-design v4 Step 2. External research on the Coordinator's questions.

#### Step 3: Coordinator writes Brief v1

Coordinator writes Brief following the mandatory minimum schema from workflow-design v4 (6 sections). This is the RAW brief before any external counsel.

Save at: `<project>/deep_design_v<N>_brief.md`

#### Step 4: Counselor Round (repeated N times, minimum 3)

**4a. Dispatch to Counselors (PARALLEL)**

Dispatch Codex FIRST, then DeepSeek, then Opus. Each gets:

```
<contents of Design_Counsellor/CLAUDE.md>

---

[ASSIGNMENT — Design Counsellor, Round {N}]

Project: <path>
Document to review: <brief path>
Investigator report: <path>
{If round > 1: Previous round counselor reports: <paths>}
{If round > 1: Previous round adversarial reports: <paths>}

ROUND_CONTEXT:
  round: {N}/3+
  lens: {PREMISE | SOLUTION | CRAFT}
  tone: {constructive | demanding | hostile-constructive}
  threshold: {CRITICAL | CRITICAL+HIGH | CRITICAL+HIGH+MEDIUM}
  validated_assumptions: {list from previous rounds}
  guiding_question: {question for this round}

Your task:
1. Read the Brief in full.
2. Apply your lens: {lens-specific instructions}.
3. Write your analysis following the COUNSELLOR_REPORT format from your CLAUDE.md.
4. Save at: <session>/consejeros/round_{N}/<your_peer_id>.md
5. Reply via peer dispatch with a summary (max 500 words).

Return your analysis.
```

Wait for quorum (2/3, timeout 10 min per counselor).

**4b. Coordinator incorporates counsel**

Coordinator reads all available counselor reports. For each recommendation:
- **INCORPORATED**: applied to next Brief version with change description
- **NOTED_NOT_APPLIED**: acknowledged but not applied, with justification
- **CONTRADICTS_OTHER_COUNSELOR**: two counselors disagree — Coordinator decides and documents

Write consolidated report at: `<session>/consejeros/round_{N}/consolidado.md`

Update Brief → save as same file (git tracks versions).

**4c. Dispatch to Adversarials (PARALLEL)**

Both adversarials get the updated Brief + all counselor reports from this round:

```
<contents of Design_Adversarial/CLAUDE.md>

---

[ASSIGNMENT — Design Adversarial, Round {N}]

Project: <path>
Brief to attack: <path>
Counselor reports this round: <paths>
Investigator report: <path>
{If round > 1: Your previous adversarial report: <path>}

Your task: attack the Brief following your CLAUDE.md.
Additional instruction: verify that counselor recommendations were properly incorporated.
{If round > 1: Verify that your previous round's REQUIRED_CLARIFICATIONS were resolved.}

Save at: <session>/adversarial/round_{N}/<your_peer_id>.md
Return the full report.
```

**4d. Coordinator corrects**

Coordinator processes adversarial reports. For each item:
- **APPLIED_FIXES**: incorporated into next Brief version
- **DEFERRED_AS_DEBT**: NOT ALLOWED in deep design Brief phase — if Coordinator wants to defer, must justify why it's not a design-level issue
- **ESCALATED_TO_USER**: requires the user's decision

Write consolidated adversarial report at: `<session>/adversarial/round_{N}/consolidado.md`

**4e. Round exit check**

If round >= 3 AND both adversarials issued `VERDICT: APPROVE`:
→ Proceed to Gate B1

If round >= 3 AND any adversarial issued `REQUEST_CHANGES`:
→ Start round N+1 (back to 4a with CRAFT lens)

If round < 3:
→ Start round N+1 regardless of verdict

**Maximum rounds**: 6. If after 6 rounds adversarials still don't approve → Gate B2 (escalate to the user with full history).

---

### Phase 2 — Spec + Plan (minimum 2 rounds)

#### Step 5: Coordinator — verification_checkpoint

Identical to workflow-design v4 Step 6. Touch reality before writing Spec.

#### Step 6: Coordinator writes Spec + Plan v1

Identical to workflow-design v4 Step 7. Spec (7 sections) + Plan.

**Plan format is a HARD CONTRACT, not a roadmap (v1.2).** The Plan is the artifact workflow-construccion consumes directly — it MUST be construction-ready. Every task carries the full 9-field execution schema, identical to the one workflow-construccion validates at input:

```
Task N: <short title, imperative>
- objetivo: <1-2 sentences — what is achieved on completion>
- archivos_a_tocar: [<absolute paths>]
- accion: <literal code/SQL/command, or precise pseudocode>
- pre_condiciones: <verifiable system state before>
- post_condiciones: <verifiable system state after>
- tests: [<exact commands + expected output>]
- criterio_de_exito: <verifiable bullets — not "works", yes "test_X 12/12 PASS">
- rollback: <exact command, or "no_destructiva">
- depende_de: [<prior tasks>] or "ninguna"
```

A week/phase roadmap table (ID / Task / Description / Dependencies / Effort / Verification) is NOT a valid Plan — it is a pre-Plan. If the design's natural output is a roadmap, the Coordinator MUST expand every roadmap row into the 9-field schema before the Plan can exit. Effort/time columns are dropped — they don't survive contact with execution and are not consumed downstream.

Save at: `<project>/deep_design_v<N>_spec.md` and `<project>/deep_design_v<N>_plan.md`

#### Step 7: Counselor + Adversarial rounds on Spec+Plan

Same structure as Step 4 but applied to Spec+Plan:

- Counselors review Spec+Plan with the same lens escalation (start at SOLUTION for Spec+Plan, not PREMISE — the premise was settled in Brief phase)
- Adversarials attack Spec+Plan following Loop 2 format from Design_Adversarial/CLAUDE.md
- Minimum 2 rounds
- Exit: both adversarials APPROVE or APPROVE_WITH_MINOR_DEBT (implementation-level only)
- Maximum 4 rounds

#### Step 7 — Spec+Plan round lens escalation

| Round | Lens | Tone | Threshold |
|-------|------|------|-----------|
| 1 | **SOLUTION** | Demanding | CRITICAL + HIGH |
| 2+ | **CRAFT** | Hostile-constructive | CRITICAL + HIGH + MEDIUM |

(No PREMISE round for Spec+Plan — premise was validated in Brief phase)

→ Gate B4 when exit condition met.

---

### Final step: Scribe + Retrospective

Identical to workflow-design v4 with additional metadata:

```yaml
workflow: deep-design
version_workflow: "1.0"
rounds_brief: N
rounds_spec: M
counselors_used: [opus_48, deepseek_v4_pro, codex_chatgpt]
adversarials_used: [opus_48, deepseek_v4_pro]
counselor_quorum_failures: N  # times a counselor didn't respond
```

---

## Anti-stuck protocols

### Anti-stuck — Counselor timeout

If a counselor does not respond within 10 minutes:
1. Log the timeout in orchestration.md
2. Check quorum (2/3)
3. If quorum met → proceed with available reports
4. If quorum not met → wait one more timeout cycle (10 min)
5. If still not met → Gate B2

### Anti-stuck — Adversarial disagreement

If one adversarial says APPROVE and the other says REQUEST_CHANGES after round 3+:
1. The Coordinator addresses ONLY the REQUEST_CHANGES items
2. Re-dispatch to the dissenting adversarial only
3. If after 2 re-dispatches the adversarial still doesn't approve → Gate B2

### Anti-stuck — Infinite loop

Maximum rounds: 6 for Brief, 4 for Spec+Plan. After max rounds without approval → Gate B2 with full history.

### Anti-stuck — Coordinator

Identical to workflow-design v4. If Coordinator doesn't process adversarial feedback in bulk → inject reminder.

---

## Counselor CLAUDE.md

Located at: `$FARO_ROOT/Agentes/Design_Counsellor/CLAUDE.md`

Generic prompt designed to work identically in Opus, ChatGPT, and DeepSeek. See the agent file for full contents.

---

## Launcher files

### Design_Counsellor/start_opus.bat

```bat
@echo off
title Consejero_diseno_Opus
cd /d "$FARO_ROOT/Agentes\Design_Counsellor"
set RELAY_PEER_ID=cons-dise-opus
claude --dangerously-skip-permissions --model "claude-opus-4-8" --dangerously-load-development-channels plugin:relay@relay-plugin
```

### Design_Counsellor/start_deepseek.bat

```bat
@echo off
title Consejero_diseno_DeepSeek
cd /d "$FARO_ROOT/Agentes\Design_Counsellor"
set ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
set ANTHROPIC_AUTH_TOKEN=<DEEPSEEK_API_KEY>
set ANTHROPIC_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-pro[1m]
set CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-pro[1m]
set CLAUDE_CODE_EFFORT_LEVEL=max
set RELAY_PEER_ID=cons-dise-deepseek
claude --dangerously-skip-permissions --dangerously-load-development-channels plugin:relay@relay-plugin
```

### Codex counselor launch

Use existing `ecorelay-codex.cmd` with CLAUDE.md contents as initial prompt. Peer ID managed by ecorelay-codex system.

---

## Cost and performance (estimated)

| Phase | Estimated duration | Estimated tokens (coordinator) | External model calls |
|-------|-------------------|-------------------------------|---------------------|
| Brief (3 rounds) | ~120-180 min | ~300-500k | 9 counselor + 6 adversarial |
| Spec+Plan (2 rounds) | ~90-120 min | ~200-400k | 6 counselor + 4 adversarial |
| **Total** | ~210-300 min | ~500-900k | ~25 external dispatches |

---

## Full-team consistency sweep (v1.1 — added 2026-06-30 post first execution)

**Origin**: first real execution of this workflow (KnowTwin, 2026-06-30). After adversarials APPROVED, two full-team sweeps found ~60 cross-document inconsistencies, stale text from earlier versions, and propagation failures that survived all regular rounds. The recurring failure mode: a fix applied in one document/section but not its mirror in another document/section. Five individual passes (3 counselors + 2 adversarials) working in their own lanes didn't catch cross-document drift. The full-team sweep — all 5 reading ALL documents simultaneously — did.

**When it triggers**: AFTER adversarials issue APPROVE (or APPROVE_WITH_MINOR_DEBT) on either Brief or Spec+Plan, BEFORE presenting the gate to the user.

### Sweep protocol (2 rounds)

**Sweep 1 — Hunt**

1. Coordinator dispatches ALL 5 peers (3 counselors + 2 adversarials) simultaneously with the same mission:
   - Read ALL deliverable documents end-to-end (Brief + Spec + Plan for Spec+Plan phase; Brief alone for Brief phase)
   - Cross-reference: Brief promises vs Spec delivery vs Plan tasks
   - Find EVERYTHING: missing items, cross-document inconsistencies, dead references, stale text from earlier versions, formulas that differ between documents, version stamp mismatches
   - **Plan consumability**: verify every Plan task carries the full 9-field execution schema (objetivo/archivos_a_tocar/accion/pre/post/tests/criterio/rollback/depende_de). A roadmap table (ID/Task/Description/Deps/Effort/Verification) is a finding, not a Plan.
   - ALL severity levels (no threshold — this is a dragnet)
2. Wait for all 5 responses (no quorum — this is the last pass, everyone participates)
3. Coordinator synthesizes ALL findings into a convergence matrix and applies fixes in ONE pass across all documents

**Sweep 2 — Verify**

1. Coordinator dispatches ALL 5 peers again with updated documents
2. Mission: verify YOUR findings from Sweep 1 were fixed. Find anything remaining.
3. Wait for all 5 responses
4. Coordinator applies final fixes

**Final adversarial round**

After Sweep 2 fixes, dispatch ONLY the 2 adversarials for a definitive verdict:
- Must issue APPROVE or APPROVE_WITH_MINOR_DEBT
- If REQUEST_CHANGES on remaining items → fix and re-dispatch (max 1 re-dispatch)
- If still REQUEST_CHANGES after re-dispatch → Gate B2 (escalate to the user)

**Then** → present Gate (B1 for Brief, B4 for Spec+Plan)

### Impact on exit conditions

The exit conditions in §4e and §Step 7 are modified:

- **Brief phase**: when adversarials APPROVE after round 3+ → Full-team sweep (2 rounds) → final adversarial → Gate B1
- **Spec+Plan phase**: when adversarials APPROVE after round 2+ → Full-team sweep (2 rounds) → final adversarial → Gate B4

### Session folder additions

```
<session>/
  ├── consejeros/
  │     ├── ...regular rounds...
  │     ├── sweep_1/          # Sweep 1 reports (all 5 peers)
  │     └── sweep_2/          # Sweep 2 verification (all 5 peers)
  ├── adversarial/
  │     ├── ...regular rounds...
  │     ├── sweep_1/          # Adversarial sweep reports
  │     ├── sweep_2/          # Adversarial sweep verification
  │     └── final/            # Definitive adversarial verdict
```

### Cost impact

| Phase | Additional duration | Additional dispatches |
|-------|--------------------|-----------------------|
| Brief sweeps | ~30-45 min | 10 (sweep 1) + 10 (sweep 2) + 2 (final adv) = 22 |
| Spec+Plan sweeps | ~30-45 min | 22 |
| **Total added** | ~60-90 min | ~44 dispatches |

Updated total estimate: ~270-390 min (was 210-300 min).

### Why this is worth the cost

The regular rounds (counselors → adversarials) work in lanes: each peer reads ONE document through ONE lens. Cross-document inconsistencies accumulate invisibly. The sweep forces ALL peers to read ALL documents simultaneously. In the first execution, Sweep 1 found 100+ items that survived 5 regular rounds. Sweep 2 found ~20 remaining after fixes. The final adversarial found 3 cosmetic items. Without the sweeps, the Spec would have shipped with formulas that disagreed between Brief and Spec, version stamps that lied, and SQL that didn't compile.

---

## Version history

- **v1.2 (2026-07-01)**: Plan execution-readiness gate. The Plan is now an enforced 9-field-per-task execution contract (identical to workflow-construccion input), not a roadmap. Added: explicit schema in Step 6, a non-skippable readiness gate before Gate B4, a Plan-consumability check in the full-team sweep, and a construction-ready assertion in the Gate B4 block. Time/effort columns banned as a scoping unit. Learned from KnowTwin: the v3 Plan shipped as a week roadmap and construction had to reconstruct the 9-field schema task-by-task before building.
- **v1.1 (2026-06-30)**: added full-team consistency sweep (2 rounds + final adversarial) between adversarial APPROVE and gate. Learned from first real execution on KnowTwin. Adds ~60-90 min and ~44 dispatches but catches cross-document drift that regular rounds miss.
- **v1.0 (2026-06-29)**: first version. Designed by Prima with Hilo (flow architecture, quorum, failure handling), Lienzo (escalation by lens/tone/threshold), and Eco (counselor voice). Based on workflow-design v4.0 with multi-model iterative refinement.
