---
name: workflow-diseno
description: |
  Multi-agent design workflow. Use it BEFORE any execution workflow (Construction, Evolution, Integration, Adaptation) when the task is non-trivial: refactor touching schema or data, integration with external systems, feature with non-obvious trade-offs, or a project where the Architect's training cutoff could be costly. Produces Brief + Spec + Plan ready for the Supervisor to execute.
metadata:
  version: "4.0"
  estreno_v1: 2026-04-17
  endurecido_v2: 2026-04-18
  agent_teams_v3: 2026-04-26
  relay_rewrite: 2026-05-22
  autor_v3: Prima
  hardening_reason: |
    Application of workflow-construction v3 methodology to workflow-design. v1 left too much inference to the orchestrator model: non-literal dispatch prompts, ambiguous physical artifact locations, unformalized Brief and Spec schemas, gates with non-explicit formats, no Gate 3 for scope changes, no formal Challenger authority over the Architect when conflicting with verified research, no referenced templates, no Faro retrospective at close.
invocation: relay session (separate Claude Code instance)
tags:
  - workflow/design
  - agent/investigator
  - agent/adversarial_design
  - agent/architect
  - agent/scribe
  - agent/challengerSpec
---

# Workflow: Design (v4 — Relay)

Orchestrates the design phase before execution. Produces documents (Brief, Spec, Plan) that eliminate ambiguity before anyone writes a line of code.

> **Guiding principle 1 — Do not improvise**: this workflow assumes that Faro and subagents **do not infer well**. Every step, prompt, path, and format must be explicit. If you read this skill and think "here I need to decide how to do X" — stop and consult the user (gate). Do not improvise.
>
> **Guiding principle 2 — Verified research is authority above the Architect**: if the Architect's Brief contradicts a verified finding with a cited source (either from a prior report of `workflow-investigation` or from the contingency Investigator), **research wins**. The Adversarial must detect that conflict and mark it as BLOCKER. The Architect cannot overwrite current external research with their training cutoff.
>
> **Guiding principle 3 — The Adversarial is not optional**: even if the user approves the Brief "by eye", the Adversarial is always launched. Its function is not ceremonial validation — it is to detect contradictions, implicit assumptions, and gaps that neither the user nor the Architect will see because both are too close to the problem.
>
> **Guiding principle 4 — Investigator is CONTINGENCY, not a mandatory phase** (added 2026-04-19): after the bifurcation of workflow-investigation into light/deep, external research must come FIRST from a prior report in `$FARO_ROOT/Informes/Investigacion/`. The Architect searches there before generating questions. The Investigator (mode 3, Haiku — validated 2026-04-21) is only launched as an explicit phase if: (a) there is no prior report covering the topic AND (b) the task is light (standard, not critical). For **critical tasks without a prior report**, Faro must **abort this workflow and launch `workflow-investigation` first** — critical design cannot start blind.

---

## When it activates

Faro launches this workflow when:
1. the user asks to design something before building it (see triggers in `description`).
2. And the task has been classified as **standard** or **critical** (see next section).
3. **Research precondition**: Faro checks whether there is a prior report in `$FARO_ROOT/Informes/Investigacion/` covering the topic (search by tags / date / name). If yes → proceed. If not:
   - **light standard** → proceed with contingency Investigator (Step 2 of the flow, mode 3 of Investigator/CLAUDE.md).
   - **critical** → **abort** and launch `workflow-investigation` first. Faro notifies the user: *"Critical task without prior report. Running workflow-investigation before returning to design."*

Faro **does not** launch this workflow for:
- Trivial tasks (<100 lines, <5 decisions, established pattern) → go directly to workflow-construction with simple Plan
- Specific bugs with known cause → direct fix
- Cosmetic or style changes → direct fix

---

## Complexity levels

The classification is decided by **the user directly or Faro upon receiving the task** (never the Architect — they are the designer, not the one who decides how much design is needed).

| Level | Objective criteria (one suffices) | Action |
|-------|----------------------------------|--------|
| **trivial** | <100 lines, <5 decisions, well-established pattern | DO NOT use this workflow |
| **standard** | Non-obvious trade-offs, integration with existing system, technology with relevant training cutoff | **Loop 1 only** (Brief) |
| **critical** | Touches SQL schema, multiple interdependent files, external API, data migration | **Loops 1 + 2** (Brief + Spec + Plan) |

If the classification is ambiguous → Faro asks the user before choosing the level.

---

## The 4 human gates (mandatory)

**Golden rule of gates**: options are always presented with **full literal text**, never with A/B/C labels. Alphabetic labels invite misinterpretation. Each option carries its action described literally, even if redundant.

### Gate B0 — Workflow load confirmation

**When**: right after Faro receives the task, before dispatching to the first agent.

**What Faro does**:

```
[GATE B0 — Load confirmation]
I have loaded workflow-design v4 (Relay).

Task received: <1-2 sentence summary>
Classified level: <standard | critical>
Project: <project path>
Loops to be executed: <Loop 1 only | Loops 1 + 2>

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>_design/
- Final deliverables will live in: <project path>/
  * refactor_v<N>_brief.md
  * refactor_v<N>_spec.md (critical only)
  * refactor_v<N>_plan.md (critical only)
  * verification_checkpoint.md (critical only)
- Agent reports: <project path>/.faro/reportes_diseno/
- Agents I will dispatch (in order):
    1. Architect — produces brief of questions
    2. Investigator — external research
    3. Architect — writes Brief
    4. Adversarial — adversarial attack on Brief
    5. Architect — closes Loop 1 (Brief v2)
    [IF critical:]
    6. Architect — writes verification_checkpoint.md
    7. Architect — writes Spec + Plan
    8. Adversarial — adversarial attack
    9. Architect — closes Loop 2 (Spec v2 + Plan v2)
    10. Scribe — final documentation + Faro retrospective

Subsequent gates I will trigger:
- B1: Brief v2 approval (always, when closing Loop 1)
- B2: if there are ESCALATED_TO_USER items in loop closures
- B3: if the user requests a scope change during design

Options:
- "Proceed" — I start with physical setup and Step 1.
- "Adjust X" — describe what you want to modify before proceeding.
- "Do not proceed" — I cancel without touching anything.

What should I do?
```

### Gate B1 — Brief v2 approval (always)

**When**: at the end of Loop 1, after the Architect delivers Brief v2.

**What Faro does**: presents the user with Brief v2 along with the Loop 1 report (APPLIED_FIXES, DEFERRED_AS_DEBT, Adversarial observations).

```
[GATE B1 — Brief v2 approval]
Project: <name>
Brief v2: <path>
Loop 1 report: <path>

Loop 1 summary:
- Investigator findings: N sources, X incorporated into Brief
- Adversarial observations: N total (X APPLIED / Y DEFERRED / Z ESCALATED)
- Explicit debt documented: <short list>

Options:
- "I approve Brief v2 — proceed with Loop 2" (only if critical)
- "I approve Brief v2 — close here" (if standard, or if critical but the user decides to stop)
- "Revise X before approving" — describe what you want adjusted; Faro re-dispatches to Architect from Step 3
- "Reject — relaunch the design" — the Brief is not usable, we go back to Step 1

What should I do?
```

### Gate B2 — ESCALATED_TO_USER in loop closures

**When**: if in Loop 1 or Loop 2 closure, the Architect marks items as `ESCALATED_TO_USER` (issues requiring the user's decision before continuing).

**What Faro does**: presents each escalated item with its context.

```
[GATE B2 — Decisions escalated by the Architect]
Loop: <1 | 2>
Escalated items (N):

Item 1:
  Adversarial issue: <text>
  Architect context: <text>
  Technical options the Architect sees: <A | B | C>
  Architect recommendation: <option + reason>

Item 2:
  [...]

the user's options per item:
- "For item N, I choose <specific option>"
- "For item N, leave it as DEFERRED_AS_DEBT"
- "For item N, abort the workflow — I need to think about it"

What do you decide?
```

### Gate B3 — Scope change during design (new in v2)

**When**: the user decides during the workflow to add, remove, or modify the design scope.

**What Faro does**:

```
[GATE B3 — Scope change detected]
the user's request: <literal description>
Current phase: <Step N of Loop M>
Deliverables already produced: <list>
Estimated impact:
  - Is the current Brief still valid? <yes | no | partial — which parts it invalidates>
  - Does the Investigator need to be re-launched? <yes | no>
  - Does the Adversarial need to be re-launched? <yes | no>

Options:
- "Apply the change" — Faro integrates the new scope: if it invalidates the Brief, re-launch from Step 3; if it only expands, add to Brief and resume where it left off.
- "Defer it until after the current design" — the scope change goes to the backlog; it will be designed in a future workflow execution.
- "Cancel the request" — I continue with the original scope.

What should I do?
```

---

## System agents — Relay (v4.0, 2026-05-22)

Each workflow uses relay peers. The orchestrator joins the room, dispatches peers via peer dispatch, and directs. Agents communicate directly with each other — the orchestrator does not relay.

**Important note**: this workflow does NOT use Designer or Supervisor. Those are roles for execution workflows. Here the Architect is the one who produces the deliverables.

### Team structure

```
join coordination room

RELAY PEERS (separate sessions, bidirectional via peer dispatch):
├── Architect (Opus) — central instance, EVERYTHING converges here: Brief, Spec, Plan
├── Design_Adversarial (Sonnet) — adversarial with memory, attacks Brief (Loop 1) and Spec+Plan (Loop 2)
│   (merges former Challenger + ChallengerSpec into a single persistent relay peer)
└── Investigator (Haiku) — 1 instance on standby, research service for the whole team

ONE-SHOT (ephemeral, one-shot):
├── Archivist (Haiku) — pre-flight (internal knowledge) + post-flight (metadata verification)
└── Scribe (Sonnet) — archives at team close

LEAD (orchestrator):
└── Gates, anti-stuck, investigator escalation decisions. Does NOT relay.
```

### Agent table

| Agent | Type | Model | Guaranteed tools | CLAUDE.md |
|--------|------|--------|-----------------|-----------|
| **Architect** | Relay peer | **Opus** | peer dispatch, Task*, Read, Write, Edit, Bash, MCPs | `$FARO_ROOT/Agentes/Arquitecto/CLAUDE.md` |
| **Design_Adversarial** | Relay peer | Sonnet | peer dispatch, Task*, Read, Write, WebFetch | `$FARO_ROOT/Agentes/Adversarial_Diseno/CLAUDE.md` |
| **Investigator** | Relay peer | Haiku | peer dispatch, Task*, Read, Write, WebSearch, WebFetch, YouTube | `$FARO_ROOT/Agentes/Investigador/CLAUDE.md` |
| **Archivist** | One-shot | Haiku | Read, MCPs (EcoDB, obsidian) | `$FARO_ROOT/Agentes/Archivista/CLAUDE.md` |
| **Scribe** | One-shot | Sonnet | Read, Write, MCPs (EcoDB, obsidian) | `$FARO_ROOT/Agentes/Escribano/CLAUDE.md` |

### Direct communication

```
STARTUP:
Orchestrator passes prior research report to Architect in peer dispatch (if it exists).
Investigator starts on standby — research service for any peer.

LOOP 1 (Brief):
Architect needs research → peer dispatch(to="Investigator") direct
Investigator → peer dispatch(to="Architect") result direct
Architect writes Brief → disk
Orchestrator ──peer dispatch──→ Design_Adversarial: "attack Brief at <path>"
Design_Adversarial ──peer dispatch──→ Architect (direct feedback)
Design_Adversarial ──peer dispatch──→ lead (verdict for gate)
Orchestrator authorizes → dispatch task to Architect

LOOP 2 (Spec + Plan, critical only):
Architect does verification_checkpoint (real commands, can request research)
Architect writes Spec + Plan → disk
Orchestrator ──peer dispatch──→ Design_Adversarial: "attack Spec+Plan, verify Loop 1 fixes"
Design_Adversarial REMEMBERS Brief → verifies Brief↔Spec coherence
Design_Adversarial ──peer dispatch──→ Architect + lead
Orchestrator authorizes → dispatch task to Architect

RESEARCH ON-DEMAND:
any peer ──peer dispatch──→ Investigator: "I need to know X"
Investigator → peer dispatch result to the requesting peer
If MORE investigators needed → peer asks orchestrator → orchestrator decides and joins more
```

### Chain of command (non-negotiable)

- **the user**: product decisions (gates, scope, budget).
- **Orchestrator (lead)**: technical and operational decisions. Authorizes fix integration. Decides investigator escalation. Evaluates verdicts.
- **Agents**: execute and advise. Do not decide. Direct communication = efficiency, not delegation.

### Peer state by phase

| Phase | Architect | Design_Adversarial | Investigator |
|---|---|---|---|
| Brief preparation | **working** (can request research) | idle | standby (available) |
| Brief attack | idle | **working** (reads disk) | standby |
| Loop 1 closure | **working** (integrates fixes) | idle | standby |
| Gate B1 | idle | idle | standby |
| verification_checkpoint | **working** (real commands) | idle | standby |
| Spec + Plan | **working** (can request research) | idle | standby |
| Spec+Plan attack | idle | **working** (remembers Loop 1) | standby |
| Loop 2 closure | **working** (integrates fixes) | idle | standby |
| Close | shutdown | shutdown | shutdown |

**Investigator as service**: starts on standby. Any peer sends peer dispatch with a concrete question → direct response to the requester. If a peer needs parallel investigation (multiple focuses), asks the orchestrator. Orchestrator decides whether to escalate by joining additional investigators as peers.

**Design_Adversarial (merger of Challenger + ChallengerSpec)**: a single peer with dual capability. Loop 1 attacks Brief. Loop 2 attacks Spec+Plan WITH MEMORY of what it attacked in Loop 1 — verifies that Brief fixes materialized in the Spec.

**Cost of idle peers**: zero tokens.

#### HARD RULE — Correct agent invocation (2026-04-28)

**ALL agents are dispatched via peer dispatch with an explicit peer name.** No exceptions.

```
dispatch task to Architect
dispatch task to Investigator
dispatch task to Design_Adversarial
```

**NEVER dispatch without a self-contained prompt.** The peer only needs its assignment — nothing from the lead context should bleed in.

**Incident 2026-04-28:** 7 investigators dispatched without clean context = 700k tokens burned on startup alone.

---

## Initial setup — file structure

Upon confirming Gate B0 with "Proceed", Faro executes this setup **before dispatching to the Architect**:

### 1. Session folder (coordination)

```
$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>_design/
  ├── CONTRACT.md             ← copied from Plantillas/CONTRACT_diseno_template.md
  ├── LESSONS.md              ← copied from Plantillas/LESSONS_template.md (empty)
  └── orchestration.md       ← Faro's append-only log
```

### 2. Project folder (final deliverables)

Design deliverables live in the project, not in Faro/Sesiones — because the execution workflow needs them afterward.

```
<project_path>/
  ├── refactor_v<N>_brief.md          ← produced in Step 3 (Loop 1)
  ├── refactor_v<N>_spec.md           ← produced in Step 7 (Loop 2, critical only)
  ├── refactor_v<N>_plan.md           ← produced in Step 7 (Loop 2, critical only)
  ├── verification_checkpoint.md      ← produced in Step 6 (Loop 2, critical only)
  └── .faro/
        └── reportes_diseno/
              ├── investigador_report.md
              ├── adversarial_report.md
              ├── adversarial_spec_report.md
              ├── arquitecto_cierre_loop1.md
              └── arquitecto_cierre_loop2.md (critical only)
```

### 3. Referenced templates

- `$FARO_ROOT/Plantillas/BRIEF_template.md`
- `$FARO_ROOT/Plantillas/SPEC_template.md`
- `$FARO_ROOT/Plantillas/PLAN_template.md` (shared with construction)
- `$FARO_ROOT/Plantillas/verification_checkpoint_template.md`
- `$FARO_ROOT/Plantillas/CONTRACT_diseno_template.md`
- `$FARO_ROOT/Plantillas/LESSONS_template.md`

---

## Mandatory minimum schemas

### Brief — minimum schema

Every Brief produced by the Architect must have these sections (the Adversarial rejects the Brief if any are missing):

```
# Brief — <Refactor/feature name>

## 1. Context and motivation
- What problem it solves
- Why now
- Affected users

## 2. Design decisions (with traceability)
Each decision cited with its origin:
- [research] — comes from the Investigator, with source URL
- [user-brief] — comes literally from the user
- [my-inference] — Architect's inference based on known context

Format per decision:
- **D<N>**: <decision>
  - Origin: [research | user-brief | my-inference]
  - Reason: <1-2 sentences>
  - Conscious trade-off: <what is sacrificed>
  - Discarded alternatives: <short list with reason for discarding>

## 3. Scope
- In: explicit list
- Out: explicit list (conscious debt)

## 4. Success criteria (verifiable)
Operational bullets, not "works well":
- <criterion with command/query that validates it>

## 5. Explicit debt
- What remains consciously unresolved and why

## 6. Questions the Adversarial should ask
The Architect anticipates their own weak points (without answering them — that is the Adversarial's turn).
```

### Spec — minimum schema (critical only)

```
# Spec — <Refactor/feature name>

## 1. Reference to Brief and verification_checkpoint
Links to both documents with date.

## 2. Schema / DDL (if applicable)
Literal, executable SQL.

## 3. Function/tool/endpoint signatures
Explicit types, not descriptions.

## 4. Real examples (no placeholders)
At least 3 real use cases with literal inputs/outputs.

## 5. External dependencies
Exact version of each. Link to official documentation.

## 6. Error handling
For each function/endpoint: what errors it returns, how.

## 7. Success criteria per component
Verifiable bullets that translate to tests in the Plan.
```

### Plan — minimum schema

Identical to the workflow-construction v3 schema. Each Plan task has:
- `objetivo`, `archivos_a_tocar`, `accion`, `pre_condiciones`, `post_condiciones`, `tests`, `criterio_de_exito`, `rollback`, `depende_de`

See template at `$FARO_ROOT/Plantillas/PLAN_template.md`.

### verification_checkpoint.md — minimum schema (critical only)

```
# verification_checkpoint — <date>

## Real system state (executed commands)
For each technical prerequisite: command + literal output.

## Real counters (DBs, configs)
Exact values at the time of verification (e.g. "triples: 2571 at 2026-04-18 11:22").

## Concrete findings that the Spec must cite
Each finding numbered and referencing the verified file/DB.
```

---

## Workflow flow (step by step, literal prompts)

### Step 0: Faro validates and prepares

1. Receives task from the user.
2. Determines level (standard/critical). If ambiguous → asks.
3. Pre-flight checks:
   - The project exists on disk (`<project_path>` is a valid directory)
   - EcoDB accessible (trivial query)
   - The 5 CLAUDE.md files exist in `$FARO_ROOT/Agentes/`
   - The 6 templates exist in `$FARO_ROOT/Plantillas/`
4. Creates session folder and `.faro/reportes_diseno/` in the project. Copies CONTRACT + LESSONS from templates.
5. **Gate B0** — waits for the user's confirmation.

---

### Step 0.5: Archivist pre-flight (MANDATORY)

Before joining the relay room and dispatching agents, launch the Archivist to search for internal knowledge about the task topic. This prevents the Investigator from going out to find what is already documented.

```
peer dispatch(to="Archivist", question="""<contents of Archivista/CLAUDE.md>

---

[ASSIGNMENT — Archivist Pre-flight]

Workflow topic: <the user's task>
Project: <path>

Execute Mode 1 (Pre-flight) from your CLAUDE.md.
Search EcoDB (search, neighbors, search_nodes) and the Obsidian vault for everything we already know about this topic.
Classify into DIRECT_ANSWERS / RELEVANT_CONTEXT / NOTHING_FOUND.
Deliver in ARCHIVISTA_PREFLIGHT format.""")
```

**The Archivist's result is passed to the Architect in Step 1** as "Prior internal knowledge". The Architect does not investigate what is already documented — they formulate questions about what is missing.

---

### Loop 1 — Brief

**Relay (v4.0, 2026-05-22):** The Architect is a **relay peer** that lives through the whole workflow. Communicate with them via `peer dispatch(to="Architect", ...)`. The Adversarial is another persistent peer that attacks Brief (Loop 1) and Spec+Plan (Loop 2) with memory between loops. The Investigator is a peer on standby available for on-demand research. See the "System agents" section for full details.

#### Step 1: Architect prepares brief of questions

Literal prompt that Faro sends to the Architect (injected after Architect/CLAUDE.md):

```
<contents of Arquitecto/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Architect, Step 1 of Loop 1]

Workflow: design v4
Project: <path>
Level: <standard | critical>
the user's task (literal): <text>

Your task NOW (only this, nothing else):
1. Search EcoDB with domain tags (`search` tool):
   - <suggested tags based on the task domain>
   Note relevant lessons.
2. Query EcoDB graph if the task touches already-mapped systems:
   - explore graph connections or search graph nodes
   Note known dependencies.
3. Identify 4-8 questions where your training cutoff or knowledge is biased and where the Investigator needs to provide current external sources. Examples of areas where you might be uncertain:
   - New libraries (<2 years) that may have changed their API
   - Best practices that may have evolved
   - Technologies whose documentation changes frequently (LLMs, vector databases, JS frameworks)
4. Mandatory delivery format:
   ```
   BRIEF_QUESTIONS:
   Q1: <concrete question, with technical context of the project>
   Q2: <...>
   ...
   Q6: <...>
   TECHNICAL_CONTEXT: <2-3 sentences so the Investigator understands why you are asking this>
   ECODB_RELEVANT_LESSONS: <list or "none">
   ECODB_DEPENDENCIES: <list or "none">
   ```

**DO NOT write the Brief yet.** This step is only to prepare the questions. The Brief comes in Step 3 after research.

Return your delivery in that format.
```

#### Step 2: Investigator

Literal prompt:

```
<contents of Investigador/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Investigator]

Project: <path>
Architect's questions: <literal BRIEF_QUESTIONS from Step 1>
Technical context: <literal TECHNICAL_CONTEXT>

Your task:
1. Research each question using current external sources (official docs, papers, repos with >1000 stars, changelogs from the last 12 months).
2. Discard sources without a verifiable date or older than 2 years if the technology changes quickly.
3. Triangulation: each finding must have at minimum 2 independent sources when controversial.
4. Mandatory format:
   ```
   INVESTIGATION_STATUS: OK | PARTIAL | BLOCKED
   KEY_FINDINGS:
     H1: <finding>
       Primary source: <URL + date>
       Confirmatory source: <URL + date, or "single source found">
       Applies to questions: [Q1, Q3]
     H2: <...>
   BLOCKING_QUESTIONS: [] | [concrete question for the user when it cannot be answered without human input]
   NEXT_ACTION: "The Architect has sufficient input to write the Brief."
   ```

Save your report at: `<project>/.faro/reportes_diseno/investigador_report.md`

Return the report.
```

Faro verifies: if `BLOCKING_QUESTIONS` is not empty → consult the user before continuing (this is not a formal gate — it is an agent protocol).

#### Step 3: Architect — writes the Brief

**peer dispatch (2026-04-23):** Do NOT dispatch a new agent. Faro sends peer dispatch to the Architect that is already alive from Step 1. The Architect remembers their own questions from Step 1.

Message that Faro sends via peer dispatch:

```
[CONTINUATION — Architect, Step 3 of Loop 1]

Investigator report: <report path or literal content>

Your task:
1. Read the Investigator report in full.
2. Write the Brief meeting the **mandatory minimum schema**:
   - Reference template: `$FARO_ROOT/Plantillas/BRIEF_template.md`
   - All 6 sections are mandatory: Context, Decisions with traceability, Scope, Verifiable success criteria, Explicit debt, Questions the Adversarial should ask
3. **Hard traceability rule**: each decision carries the label [research | user-brief | my-inference]. If you cannot label it, do not include it — it is a sign that you are making it up.
4. **DO NOT self-review** — the raw Brief goes directly to the Adversarial. If you include a section "I already reviewed and found X", Faro sends it back.
5. Target length: 800-1500 words. If you exceed 2000, you are including things that should be Spec.
6. Save the Brief at: `<project>/refactor_v<N>_brief.md` (where <N> is the next available version).
7. **Mandatory pre-commitment** (write this in your response before delivering): *"I have delivered the raw Brief. After receiving the Adversarial report, I will process in bulk immediately: APPLIED_FIXES / DEFERRED_AS_DEBT / ESCALATED_TO_USER. I will not self-review or consult Faro beforehand."*

Return: Brief path + pre-commitment + confirmation that all 6 sections are present.
```

#### Step 4: Adversarial attacks Brief

Literal prompt:

```
<contents of Adversarial_Diseno/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Design_Adversarial, Loop 1 (Brief)]

Project: <path>
Brief to attack: <path>
Investigator report (reference for traceability validation): <path>

Your attitude: you are the most skeptical member of the team. You want to see the Brief collapse now, not 3 weeks from now when it is half implemented. Adversarial but loyal — you look for defects to protect the project, not to sabotage it.

**CRITICAL — cross-validation against research** (guiding principle 2):
If the Brief makes a technical claim that contradicts a verified finding from the Investigator (with source), mark it as BLOCKER. Research with a current external source has authority above the Architect's training cutoff. The Architect CANNOT overwrite research with their inference.

YOU DO NOT HAVE ACCESS to the process that led to the Brief. Only the Brief, the Investigator report, and your judgment.

Your work:
1. Read the Brief in full.
2. Detect 4 types of defects:
   - **DIRECT_ATTACKS**: technical claims you believe are incorrect. Justify each one.
   - **CONTRADICTIONS**: parts of the Brief that contradict each other, or that contradict verified research.
   - **IMPLICIT_ASSUMPTIONS**: things the Brief assumes without stating (e.g. "assumes the DB can scale to 10x", "assumes Ollama will always be available").
   - **GAPS**: decisions the Brief does not make that will be blocking during execution.
3. Mandatory format (dual markdown-INI + JSON):

Markdown-INI:
```
REVIEW_SUMMARY: <1-2 sentence verdict>
VERDICT: APPROVE | REQUEST_CHANGES | NEEDS_REDESIGN

DIRECT_ATTACKS:
  A1 [critical|medium|low] <Brief section> — <attack>
    Justification: <...>

CONTRADICTIONS:
  C1 [critical|medium|low] <...>

IMPLICIT_ASSUMPTIONS:
  S1 [medium|low] <...>

GAPS:
  L1 [critical|medium|low] <...>

CROSS_REF_RESEARCH:
  - [Brief §X.Y claims Z] vs [Investigator H3 says W] → CONFLICT, research wins (BLOCKER)
  - [list or "no conflicts"]

REQUIRED_CLARIFICATIONS: [ids of items the Architect MUST resolve]
SOFT_OBJECTIONS: [ids of items the Architect can leave as justified debt]
```

JSON:
```json
{
  "verdict": "APPROVE | REQUEST_CHANGES | NEEDS_REDESIGN",
  "summary": "...",
  "required_clarifications": ["A1", "C1", "L1"],
  "soft_objections": ["S1", "A2"],
  "cross_ref_research_conflicts": [
    {"brief_claim": "...", "research_finding": "...", "severity": "BLOCKER"}
  ]
}
```

Consistency rules:
- `required_clarifications` empty AND `soft_objections` empty → `verdict = APPROVE`.
- `cross_ref_research_conflicts` with any item of severity BLOCKER → `verdict = NEEDS_REDESIGN` automatic (non-negotiable).

Save the report at: `<project>/.faro/reportes_diseno/adversarial_report.md`

Return the full report.
```

#### Step 5: Architect — Loop 1 closure

**peer dispatch (2026-04-23):** Faro sends peer dispatch to the live Architect. The Architect remembers their Brief v1 from Step 3.

Message via peer dispatch:

```
[CONTINUATION — Architect, Loop 1 closure]

Adversarial report: <literal content or path>

Your pre-commitment from Step 3: "I will process in bulk immediately". Fulfill it NOW.

Process each item in the Adversarial report and classify it:
- **APPLIED_FIXES**: items you incorporate into Brief v2 with concrete changes.
- **DEFERRED_AS_DEBT**: items you accept as conscious debt, with justification of why it is being deferred.
- **ESCALATED_TO_USER**: items that require the user's decision before continuing (you cannot decide them alone because they affect scope or imply trade-offs that belong to the user).

**CRITICAL**: items with `cross_ref_research_conflicts` of severity BLOCKER go MANDATORILY to APPLIED_FIXES. You cannot leave a conflict with verified research as debt.

Write Brief v2 with the APPLIED_FIXES incorporated. Save it as: `<project>/refactor_v<N>_brief.md` (overwrites v1 — v1 remains in git history).

Closure format:
```
LOOP1_CLOSURE:
APPLIED_FIXES:
  - [A1] <what I changed in Brief v2>
  - [C1] <...>
DEFERRED_AS_DEBT:
  - [S1] <what I accept as debt> — justification: <why not now>
ESCALATED_TO_USER:
  - [L1] <what I need the user to decide>
    Context: <...>
    Options I see: <A | B | C>
    My recommendation: <option + reason>

LOOP1_METRICS:
  total_observations: N
  applied_fixes: N
  deferred_as_debt: N
  escalated_to_user: N

BRIEF_V2_PATH: <path>
```

Save this report at: `<project>/.faro/reportes_diseno/arquitecto_cierre_loop1.md`

Return the report.
```

**Gate B1** is triggered here (Brief v2 approval by the user). If there are ESCALATED_TO_USER items → **Gate B2** first.

---

### Loop 2 — Spec + Plan (critical only)

#### Step 6: Architect — verification_checkpoint

**peer dispatch (2026-04-23):** Faro sends peer dispatch to the live Architect. The Architect remembers their Brief v2 from Step 5.

Message via peer dispatch:

```
[CONTINUATION — Architect, Step 6 of Loop 2]

Brief v2 approved by the user.

Your task BEFORE writing Spec + Plan:
Get out of your head and touch reality. The Brief is theory. verification_checkpoint is facts.

1. Read the actual existing code/system (not what you remember, the one today).
2. Verify each technical prerequisite with real commands and capture literal output.
3. Query real data if applicable:
   - Current DB counters (e.g. "SELECT COUNT(*) FROM triples")
   - Installed library versions (pip list, etc.)
   - Config files that the Spec/Plan will touch
4. Write `verification_checkpoint.md` at `<project>/verification_checkpoint.md` meeting the minimum schema:
   - Template: `$FARO_ROOT/Plantillas/verification_checkpoint_template.md`
   - 3 sections: real system state, real counters, findings that the Spec must cite

The Spec and the Plan will CITE this file. If there is drift between verification_checkpoint and Brief, escalate to Faro (do not improvise).

Return: verification_checkpoint path + findings summary.
```

#### Step 7: Architect — Spec + Plan

**peer dispatch (2026-04-23):** Faro sends peer dispatch to the live Architect. The Architect remembers Brief v2 and verification_checkpoint from Step 6.

Message via peer dispatch:

```
[CONTINUATION — Architect, Step 7 of Loop 2]

Your task:
1. Write the **Spec** meeting the minimum schema:
   - Template: `$FARO_ROOT/Plantillas/SPEC_template.md`
   - 7 mandatory sections: reference to Brief+verification, DDL, signatures with types, real examples, dependencies with versions, error handling, success criteria per component
   - Spec cites `verification_checkpoint.md` where applicable
2. Write the **Plan** meeting the minimum schema shared with workflow-construction v3:
   - Template: `$FARO_ROOT/Plantillas/PLAN_template.md`
   - Each task with 9 mandatory fields: objetivo, archivos_a_tocar, accion, pre_condiciones, post_condiciones, tests, criterio_de_exito, rollback, depende_de
   - If a task is not destructive, `rollback: "no_destructiva"` literal
   - Tests must be executable commands as-is (absolute paths, no unresolved variables)
3. Save:
   - Spec at: `<project>/refactor_v<N>_spec.md`
   - Plan at: `<project>/refactor_v<N>_plan.md`
4. **DO NOT self-review**. Deliver raw to the Adversarial.
5. **Mandatory pre-commitment**: write in your response *"I have delivered raw Spec + Plan. After receiving the Adversarial report, I will process in bulk immediately."*

Return: paths + pre-commitment + confirmation that the minimum schemas are met.
```

#### Step 8: Adversarial attack

Literal prompt:

```
<contents of Adversarial_Diseno/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Design_Adversarial, Loop 2 (Spec + Plan)]

Project: <path>
Brief v2: <path>
Spec: <path>
Plan: <path>
verification_checkpoint: <path>

Your attitude: more skeptical than in Loop 1 because now there is concrete code. Lies hide in the detail. You want to see the system BURN in design, not in production.

YOU DO NOT HAVE ACCESS to the process. Only the 4 documents above and your judgment.

Your work: detect 4 types of defects:

1. **GAPS_BRIEF_SPEC**: things the Brief decided but the Spec does not implement, or vice versa.
2. **SPEC_DEFECTS**: DDLs that do not parse, signatures with incorrect types, examples that would not work, dependencies with incompatible versions, incomplete error handling.
3. **PLAN_DEFECTS**: tasks with missing fields from the minimum schema, non-executable tests, incorrect rollbacks, broken dependencies between tasks, non-verifiable success criteria.
4. **COHERENCE**: the Spec and Plan do not cite verification_checkpoint where they should; Brief says X but verification_checkpoint shows Y (contradiction with reality).

Mandatory dual format (same as Loop 1 + additional fields):

Markdown-INI:
```
REVIEW_SUMMARY: <1-2 sentences>
VERDICT: APPROVE | REQUEST_CHANGES | NEEDS_REDESIGN

GAPS_BRIEF_SPEC:
  G1 [critical|medium|low] <...>

SPEC_DEFECTS:
  SD1 [critical|medium|low] <Spec §X.Y> — <defect>

PLAN_DEFECTS:
  PD1 [critical|medium|low] <Plan Task N> — <defect>

COHERENCE:
  CO1 [critical|medium|low] <contradiction>

CROSS_REF_REALITY:
  - [Spec/Plan claims Z] vs [verification_checkpoint says W] → CONFLICT, reality wins (BLOCKER)

REQUIRED_CLARIFICATIONS: [ids]
SOFT_OBJECTIONS: [ids]
```

JSON: equivalent structure.

Consistency rules: same as Loop 1.

Save report at: `<project>/.faro/reportes_diseno/adversarial_spec_report.md`

Return the report.
```

#### Step 8b: Double blind validation (critical fixes only)

When any finding is classified as "critical" severity, the fix must be validated independently by TWO agents before the Architect applies it. This prevents false critical findings from distorting the Spec/Plan.

Process: dispatch ChallengerSpec + one other independent reviewer (Design_Adversarial if available, otherwise Investigator) to validate the critical fix independently. Both must agree before fix is applied. If they disagree, escalate to Gate B2.

This pattern was validated empirically (2026-04-26): Prima + CuestionadorSpec independently validated a SCD2 critical fix and found 2 additional edge cases.

#### Step 9: Architect — Loop 2 closure

**peer dispatch:** Faro sends peer dispatch to the live Architect. The Architect remembers Spec+Plan from Step 7.

Prompt analogous to Step 5 but for Spec + Plan. Updates versions: Spec v2, Plan v2. Classifies items in APPLIED / DEFERRED / ESCALATED.

If there are ESCALATED_TO_USER items → **Gate B2**.

Report format identical to Step 5 but with Loop 2 metrics.

---

### Final step: Scribe + Faro Retrospective

#### Scribe (always)

Literal prompt:

```
<contents of Escribano/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Scribe (workflow-design closure)]

Project: <path>
Final state: <"Loop 1 closed, standard" | "Loops 1+2 closed, critical" | "Aborted at <phase>">

Read ALL workflow artifacts:
- Brief v2
- Spec v2 (if critical)
- Plan v2 (if critical)
- verification_checkpoint.md (if critical)
- Investigator, Adversarial reports (Loop 1 + Loop 2)
- Architect closure reports (Loop 1 + Loop 2)
- Accumulated LESSONS.md

Document in these 3 places (all mandatory):

1. Obsidian: `$FARO_ROOT/Informes/Diseno/<Project>_<YYYY-MM-DD>.md`
   Minimum content:
   - What was designed
   - Decisions made and their origin (research / user-brief / my-inference)
   - Decisions NOT made and why (what the Adversarial rejected and why it was accepted/rejected)
   - APPLIED_FIXES from both loops with justification
   - DEFERRED_AS_DEBT with justification
   - Bugs found only in Loop 2 that Loop 1 could not see (if applicable)
   - Metrics from both loops
   - Gates triggered and the user's decisions

2. EcoDB (`save_memory` tool, author: "Scribe"):
   - One memory with tags = [project, domain, "design", key_technologies]
   - Content < 500 words (embedding limit)
   - Summary: what was designed, what debt remained

3. EcoDB graph (`save_triples_batch` tool): minimum triples
   - `<project design v<N>>` is_a `design`
   - `<project design v<N>>` precedes `<project construction v<N>>` (if critical)
   - `<project>` has_debt `<DEFERRED_AS_DEBT item>` (for each one)
   - With `origin="Design_<Project>_<date>"` and `author="Scribe"`

Report to Faro with SCRIBE_REPORT confirming the 3 places updated.
```

#### Archivist post-flight (after the Scribe)

Last agent before the retrospective. Verifies that the Scribe left everything in place.

```
peer dispatch(to="Archivist", question="""<contents of Archivista/CLAUDE.md>

---

[ASSIGNMENT — Archivist Post-flight]

Session: <session name>
Project: <path>
Scribe's final report: <Obsidian path>

Execute Mode 2 (Post-flight) from your CLAUDE.md.
Verify: complete YAML frontmatter, ASCII-only tags, traceability with valid wiki-links,
Scribe's EcoDB memory without duplicates and with correct author, EcoDB graph with correct origin.
Report issues — DO NOT fix anything, the lead decides.
Deliver in ARCHIVISTA_POSTFLIGHT format.""")
```

If the Archivist reports REQUIRES_CORRECTION, the lead (orchestrator) decides whether to correct before closing or leave it as documented debt.

#### Faro Retrospective (new in v2)

After the Scribe, Faro writes (without launching an agent) a retrospective at:
`$FARO_ROOT/Sesiones/<date>_<project>_design/retrospective.md`

Format:
```markdown
# Retrospective workflow-design — <project> — <date>

## What worked
- <bullets of what the SKILL allowed to do well>

## What did not work / where I improvised
- <any point where Faro had to decide something the SKILL did not cover>
- <typos Faro introduced, if any>
- <gates I triggered that were not in the SKILL>

## Real metrics
- Loop 1 duration: X min
- Loop 2 duration: Y min (if applicable)
- Adversarial observations: N (loop 1) + M (loop 2)
- Applied/Deferred/Escalated ratios
- Approx tokens: ~N

## For v<N+1>
- <1-3 concrete changes that would improve the SKILL>
```

This retrospective is input for the next iteration of the SKILL.

---

## Cost and performance (reference)

| Complexity | Estimated duration | Estimated tokens | Time/avoided problem ratio |
|---|---|---|---|
| standard (1 loop) | ~45-60 min | ~150-250k | ~2 min/problem |
| critical (2 loops) | ~90-120 min | ~300-500k | ~1.5 min/problem |

---

## Healthy metrics per loop

| Ratio | Loop 1 (Brief) | Loop 2 (Spec+Plan) |
|---|---|---|
| Investigator findings incorporated | >70% | — |
| Applied fixes / Adversarial observations | 50-70% | 25-45% |
| Required_clarifications resolved without human | >80% | >80% |
| Documented debt / total observations | 20-40% | 55-75% |
| Conflicts with verified research (BLOCKER) | 0 expected | — |
| Conflicts with verification_checkpoint (BLOCKER) | — | 0 expected |

---

## Anti-stuck protocols

### Anti-stuck — Architect

If after receiving the Adversarial report, the Architect does not emit the APPLIED/DEFERRED/ESCALATED contract in their next turn, Faro injects via peer dispatch:

> *"YOU ARE STUCK. Process in bulk now: 1) REQUIRED_CLARIFICATIONS first, 2) APPLIED_FIXES / DEFERRED_AS_DEBT / ESCALATED_TO_USER. Only escalate what requires the user's decision."*

### Anti-stuck — Investigator (new in v2)

If the Investigator reports `STATUS: PARTIAL` without concrete BLOCKING_QUESTIONS, or extends >3 attempts asking for "more context" without converging, Faro injects via peer dispatch:

> *"Conclude with what you have. Mark findings with low confidence as 'single source, low confidence' and continue. The Architect decides what to do with incomplete research — not you."*

### Anti-stuck — Adversarial

If the Adversarial returns a report with `verdict: APPROVE` and 0 observations (no attacks, contradictions, assumptions, or gaps), the orchestrator injects via peer dispatch:

> *"A perfect Brief does not exist. If you genuinely see NOTHING, change approach: look for implicit assumptions that seem obvious to the Architect. Return at least 3 SOFT_OBJECTIONS or mark the verdict as 'APPROVE_WITH_OBSERVATIONS' with justification for why you find no blockers."*

### Anti-stuck — Faro itself

When Faro receives a report with VERDICT/STATUS, the action is deterministic:

| Report | Faro action |
|---------|------------|
| `VERDICT: APPROVE` (Adversarial) | peer dispatch to Architect for loop closure |
| `VERDICT: REQUEST_CHANGES` (Adversarial) | peer dispatch to Architect for loop closure (process items) |
| `VERDICT: NEEDS_REDESIGN` (Adversarial) | Gate B1 with literal verdict to the user — possible re-launch of Step 3 |
| `cross_ref_research_conflicts` with BLOCKER | Force Architect to APPLIED_FIXES (non-negotiable) |
| `STATUS: BLOCKING_QUESTIONS` (Investigator) | Consult the user before continuing |
| `ESCALATED_TO_USER` non-empty in closures | Gate B2 |
| User scope change request | Gate B3 |

---

## Agent loading protocol

Before dispatching any agent, Faro reads the corresponding CLAUDE.md and injects its contents into the peer's peer dispatch prompt:

| Agent | CLAUDE.md path |
|--------|---------------|
| Archivist | `$FARO_ROOT/Agentes/Archivista/CLAUDE.md` |
| Architect | `$FARO_ROOT/Agentes/Arquitecto/CLAUDE.md` |
| Investigator | `$FARO_ROOT/Agentes/Investigador/CLAUDE.md` |
| Design_Adversarial | `$FARO_ROOT/Agentes/Adversarial_Diseno/CLAUDE.md` |
| Scribe | `$FARO_ROOT/Agentes/Escribano/CLAUDE.md` |

---

## Input and output dependencies (information routing between workflows)

### Expected inputs (what this workflow consumes)

**Prior research report** at `$FARO_ROOT/Informes/Investigacion/<YYYY-MM-DD>_<project>.md`. Search by project name or related tags.

**Research precondition** (guiding principle 4):
- If prior report exists → the Architect reads it in their Step 1 and cites it with [research] traceability in the Brief. Can skip Step 2 (Investigator) if the report covers the questions.
- If it does NOT exist AND the task is **light standard** → launch contingency Investigator (Step 2, mode 3 of Investigador/CLAUDE.md, Haiku — validated 2026-04-21).
- If it does NOT exist AND the task is **critical** → Faro ABORTS this workflow and launches `workflow-investigation` first. Critical design without prior research is not permitted.

### Output — final report archived by the Scribe

- **Target Obsidian folder**: `$FARO_ROOT/Informes/Diseno/`
- **File name**: `<YYYY-MM-DD>_<project_slug>.md`
- **Mandatory YAML frontmatter** — schema in `Escribano/CLAUDE.md`. For design:
  ```yaml
  workflow: design
  version_workflow: "2.1"
  date: YYYY-MM-DD
  project: <human name>
  project_slug: <slug>
  faro_session: $FARO_ROOT/Sesiones/<session>/
  prior_report_consumed: "[[Investigacion/YYYY-MM-DD_project]]"  # or null if contingency Investigator was used
  contingency_investigator_used: true | false
  next_workflow_suggested: construction | evolution | integration | adaptation
  level: standard | critical
  faro_artifacts:
    brief: <project_path>/refactor_v<N>_brief.md
    spec: <project_path>/refactor_v<N>_spec.md  # critical only
    plan: <project_path>/refactor_v<N>_plan.md  # critical only
    verification_checkpoint: <project_path>/verification_checkpoint.md  # critical only
    retrospective: <faro_session_path>/retrospective.md
  ecodb_memory_ids: [<ids>]
  ecodb_graph_origin: Design_<project>_<date>
  tags: [workflow/design, status/closed, project/<slug>, level/<n>]
  ```
- **Mandatory "Traceability" section** at the end: `[[]]` links to the prior research report, to Brief/Spec/Plan in the project, to the Faro session, and to EcoDB.

### Typical next workflow

- **workflow-construction** if the design is for something new from scratch.
- **workflow-evolution** if the design is for modifying existing code.
- **workflow-integration** if the design is for bringing in external technology.
- **workflow-adaptation** if the design is for connecting something external with internal identities.

The Scribe marks `next_workflow_suggested` in the frontmatter. Faro chains it without improvising: upon receiving "build X according to design Y", reads the design report and uses the field to classify the next workflow.

---

## Version history

- **v1.0 (2026-04-17)**: first version — production debut with eco_graph_mcp v2 refactor. Metrics: Loop 1 (6 questions, 28 sources, 41 Challenger observations, 26 applied / 15 deferred); Loop 2 (55 Adversarial observations, 17 applied / 38 deferred, 9 blockers resolved). Key finding: 73% of Loop 2 observations were impossible to detect without concrete code.

- **v2.0 (2026-04-18)**: hardening by applying workflow-construction v3 methodology to workflow-design. Changes:
  1. **3 explicit guiding principles** (do not improvise, research > Architect, Challenger is not optional).
  2. **4 human gates** with literal options (B0 load, B1 Brief approval, B2 ESCALATED_TO_USER, B3 scope change — new).
  3. **Explicit physical artifact location**: deliverables in `<project>/`, coordination in `$FARO_ROOT/Sesiones/`, reports in `<project>/.faro/reportes_diseno/`.
  4. **Formalized minimum schemas** for Brief (6 sections), Spec (7 sections), verification_checkpoint (3 sections). Plan was already aligned with construction v3.
  5. **Literal prompts** for each dispatch (9 steps × agent).
  6. **Pre-flight checks** before Step 1.
  7. **6 referenced templates**: BRIEF, SPEC, PLAN, verification_checkpoint, CONTRACT_design, LESSONS.
  8. **Expanded anti-stuck**: Architect, Investigator, Challenger, Faro.
  9. **Mandatory cross-validation** by the Challenger against the Investigator's research (verified research has authority above the Architect, analogous to "Spec > Faro" in construction v3).
  10. **Faro retrospective** at closure (10-15 lines, input for v+1).
  11. **Dual markdown-INI + JSON format** formalized for Challenger reports.
  12. **Plan alignment with workflow-construction v3**: same 9 fields per task, same referenced template.

- **v3.0 (2026-04-26)**: migration to Agent Teams by Prima. Changes:
  1. Architect Opus as **persistent relay peer** — lives through the whole workflow, remembers everything.
  2. **Merger of Challenger + ChallengerSpec** into a single persistent **Design_Adversarial** Sonnet peer — attacks Brief in Loop 1, Spec+Plan in Loop 2 with memory of previous attacks.
  3. **Investigator Haiku on standby** — on-demand research service for any peer. If more are needed, orchestrator decides and escalates.
  4. Scribe continues as ephemeral one-shot at closure.
  5. Direct communication between peers (Investigator→Architect, Adversarial→Architect) without relay through the orchestrator.
  6. Explicit chain of command: the user (product), orchestrator (technical), agents (execute).
  7. State table per phase for each peer.
  8. Motivation: first real workflow-design (SocialIntel, Apr-26) demonstrated inefficiency of forks (~750k tokens in 3 Architect relaunches) and fragility (recurring SendMessage vs Agent error). Relay peers empirically validated the same day.

- **v4.0 (2026-05-22)**: relay rewrite. Agent Teams replaced by relay peers (separate Claude Code instances). All SendMessage/TeamCreate/TeamDelete calls replaced with peer dispatch/relay_join/relay_leave. Python Agent spawn blocks removed. Fully translated to English.
