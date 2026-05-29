---
name: workflow-construccion
description: |
  Orchestrated workflow to build new tools, systems or components from scratch. Use it when the user wants to create something that does not exist yet — a new MCP, a script, an automation system, a command, an integration, an agent, or any new piece of software. Also activates when the user says "I need a tool that does X", "can we build X?", "I want it to work like this: X". The difference from Evolution is that here there is no existing code to start from — the starting point is a need. For critical tasks, launch workflow-design first to produce the Spec and Plan before executing.
metadata:
  version: "5.2"
  estreno_v1: 2026-04-16
  endurecido_v2: 2026-04-18
  refinado_v3: 2026-04-18
  agent_teams_v4: 2026-04-26
  relay_rewrite: 2026-05-22
  autor_v4: Prima
  motivo_v3: |
    First end-to-end productive run (refactor eco_graph_mcp v2) revealed 7 specific improvements: (1) Faro can introduce typos in prompts that Supervisor does not detect — mandatory cross-validation Prompt↔Spec added. (2) Gates used A/B/C options that invite misinterpretation — now always use literal options. (3) The workflow did not account for external runtime configuration (claude_desktop_config.json, systemd, docker-compose) — now mandatory pre-flight check. (4) New Gate B3 for scope changes during execution. (5) New verdict APPROVE_WITH_DEBT to differentiate acceptable debt from a blocker. (6) New final retrospective step for Faro. (7) Spec is superior authority to Faro when they conflict — if Faro instructs something different from the Spec, the Supervisor fires a Gate instead of obeying.
invocation: relay session (separate Claude Code instance)
tags:
  - agent/supervisor
  - agent/executor
  - agent/verifier
  - agent/scribe
  - workflow/construccion
  - agent/code_adversarial
  - agent/security_adversarial
---

# Workflow: Construction (v5 — Relay)

Orchestrates the construction of new tools from scratch. The **Supervisor** coordinates execution task by task from an **approved Plan**. The Supervisor *supervises*, does not design — if the Plan is defective, it escalates; never improvises.

> **Guiding principle 1 — Do not improvise**: this workflow assumes that the model executing it (Faro and the subagents) **does not infer well**. Every step, prompt, path and format must be explicit. If you read this skill and think "here I need to decide how X is done" — stop and consult the user (gate). Do not improvise.
>
> **Guiding principle 2 — Spec is superior authority to Faro**: if Faro instructs something that contradicts the Spec (e.g. function names, signatures, structure), **the Spec wins**. The Supervisor detects the conflict and fires Gate B2 ("proposed modification of Plan/Prompt"), never obeys Faro against the Spec. This exists because Faro can introduce typos when assembling prompts, and the Executor would literally follow the wrong instruction. Lesson from the productive launch v2 → v3.

---

## When it activates

Faro launches this workflow when:
1. the user asks to build something that does not exist (see triggers in `description`).
2. And the task has been **previously classified** as trivial / standard / critical (see next section).

Faro **does not** launch this workflow for:
- Modifying existing code → workflow-evolucion
- Connecting two systems that already exist → workflow-integracion
- Adapting a system to a new environment → workflow-adaptacion
- Specific bugs with known cause → direct fix, no workflow

---

## Complexity levels (objective criteria)

The classification is decided by **one of these three sources, never the Supervisor**:
- prior workflow-design (already classified delivery)
- the user directly (in the assignment)
- Faro upon receiving the assignment if the user did not specify

| Level | Objective criteria (one is enough) | Action |
|-------|--------------------------------|--------|
| **trivial** | Single script <100 lines, no schema, no network, no persistent state, well-established pattern | Executor + quick verification (no formal Supervisor) |
| **standard** | Multiple files, integrates with existing system, no new schema, no migrations | Supervisor + Executor + Verifier |
| **critical** | Touches schema, data migration, external API/service, multiple interdependent tasks, deploy to production | **workflow-design first**, then this workflow with the resulting Plan |

If the classification is ambiguous → Faro asks the user before choosing a level. Does not assume.

---

## The 4 human gates (mandatory)

This workflow has **four points** where Faro **stops execution and explicitly consults the user**. They are not optional.

**Golden rule of gates** (added in v3): options are always presented with **full literal text**, never with A/B/C labels. Alphabetic labels invite misinterpretation — real example from the v2 launch: "C" offered by Faro as "abort" was understood as "continue". In v3, each option carries its action described literally, even if redundant. Do not use A/B/C or 1/2/3 as option identifiers in gates.

### Gate B0 — Workflow load confirmation

**When**: immediately after Faro receives the assignment and before dispatching the first agent.

**What Faro does**: presents the user a message with this literal structure:

```
[GATE B0 — Load confirmation]
I have loaded workflow-construccion v5.

Assignment received: <1-2 sentence summary>
Classified level: <trivial | standard | critical>
Plan origin: <prior workflow-design | Faro template | the user provided it>
Plan path: <absolute path>
Spec path: <absolute path or "not applicable for standard">

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>/
- Project folder (reports): <project path>/.faro/reportes/
- Agents I will launch (in order):
    1. Supervisor (always first)
    2. Executor (dispatched by Supervisor for each task)
    3. Verifier (dispatched by Supervisor after each Executor)
    4. Scribe (at the end)
- Parallel agents: none by default. If a task allows it, the Supervisor declares it and I consult again.
- Subsequent gates I will fire:
    - B1 before each destructive task
    - B2 if Supervisor proposes modification of Plan after 3 failed iterations, OR detects that Faro contradicts the Spec
    - B3 if the user requests a scope change during execution

Options (write the word; the label is secondary):
- "Proceed" — I start immediately with physical setup and dispatch to Supervisor.
- "Adjust X" — describe what you want to modify in the orchestration plan before proceeding.
- "Do not proceed" — I cancel the workflow without touching anything.

What do I do?
```

**Why it exists**: to validate that the SKILL has been loaded correctly, that the user's and Faro's context is synchronized, and that the user sees the orchestration plan before it starts.

### Gate B1 — Before any destructive task

**When**: immediately before dispatching to the Executor a task marked in the Plan with any of:
- `rollback` is not `"no_destructiva"`
- touches production (real DB, deploy, file deletion, schema migration)
- writes to systems the user cannot trivially revert

**What Faro does**: presents the user:

```
[GATE B1 — Imminent destructive task]
Task N: <title>
Action: <1-2 sentence summary of what it will do>
Files/systems affected: <list>
Rollback defined in the Plan: <exact rollback command>
Verifier will validate: <task success criteria>

Options:
- "Proceed" — I execute the destructive task now.
- "Stop the workflow" — I stop here without touching anything (previous tasks remain completed).
- "Review X first" — describe what you want me to verify or adjust before proceeding.

What do I do?
```

### Gate B2 — Proposed modification of Plan or Prompt

**When**: either of the two cases:
- (a) the **3 iterations** Executor↔Verifier for a task have been exhausted without `APPROVE` AND the Verifier has identified that the blocker is a Plan defect, not an Executor error.
- (b) **New in v3**: the Supervisor has detected that a prompt generated by Faro contradicts the Spec (e.g. different function names), before dispatching to the Executor. This branch does not wait for 3 iterations — it is preventive.

**What the Supervisor does**: does NOT modify the Plan or the prompt. Generates a proposal report and delivers it to Faro.

**What Faro does**: presents the user:

```
[GATE B2 — Proposed modification of Plan/Prompt]
Task N: <title>
Reason: <"3 iterations exhausted" | "Prompt↔Spec conflict detected by Supervisor pre-dispatch">
Diagnosis: <defect summary — what the Plan/Prompt says vs what the Spec or reality says>
Supervisor's proposal: <description of suggested change, with literal reference to Spec when applicable>
Estimated impact on subsequent tasks: <list or "none">

Options:
- "Apply the proposed change and resume" — Faro edits Plan/Prompt per proposal and continues.
- "Pause the workflow for me to review" — I stop and wait for specific instructions.
- "Abort and relaunch workflow-design" — the defect is structural, not isolated.

What do I do?
```

### Gate B3 — Scope change during execution (new in v3)

**When**: the user decides, during workflow execution, to expand or modify the scope of the work (add new tools, change behaviors, include unplanned features).

**Why it exists**: in the productive v2 launch, the user asked to expand from 17 to 19 tools mid-execution. Faro processed it by improvising — it worked but broke the discipline of the "approved Plan". In v3 this has a formal channel.

**What Faro does** upon receiving a scope change request:

```
[GATE B3 — Scope change detected]
the user's request: <literal description of the expansion>
Task in progress when the request arrived: <N>
Tasks completed so far: <list>
Estimated impact on the Plan:
  - New tasks to add: <list>
  - Existing tasks to modify: <list or "none">
  - New tests mandatory before deployment: <list>
  - Documentation (Spec) to update: <yes/no>

Options:
- "Apply the change" — Faro pauses execution, formally updates Plan + Spec (not on the fly),
  adds new tasks at the end of the list, resumes from where it left off.
  MANDATORY NOTE: tests for the new scope are a deployment requirement, not optional.
- "Defer until after the current workflow" — I complete what was already planned,
  the scope change remains as backlog for a future workflow.
- "Cancel the request" — I do not modify anything, I continue with the original Plan.

What do I do?
```

> Outside these four gates, the workflow runs autonomously. Faro **does not** consult the user for internal technical decisions. It does consult if an agent returns non-empty `BLOCKING_QUESTIONS` (that is the agents' contract, not a workflow gate).

---

## System agents — Relay (v5.0, 2026-05-22)

Each workflow involves a set of **relay peers** (separate Claude Code sessions). The orchestrator dispatches via peer dispatch and directs. Agents communicate directly — the orchestrator does not relay reports.

### Team structure

```
join coordination room

RELAY PEERS (persistent, bidirectional via peer dispatch):
├── supervisor (OPUS) — department head: coordinates, code review, unifies criteria,
│                       certifies production readiness. Brain of the team.
├── executor-1 (Sonnet) — main builder, persists through the whole workflow
├── executor-N (Sonnet) — additional builders if Supervisor requests parallel (on demand)
├── security-adversarial (Sonnet) — hacker: exploits, leaks, injection, auth bypass
├── code-adversarial (Sonnet) — senior dev: bugs, dead code, UX, patterns, performance
├── verifier (Sonnet) — beta tester: functional, stress, regressions, user impressions
└── investigator (Haiku) — standby for on-demand research from any peer

EPHEMERAL (dispatched once at close):
└── scribe (Sonnet) — archives at session close

ORCHESTRATOR (Faro):
└── Gates, launching additional Executors, invoking workflow-integracion/adaptacion,
    final decisions with Supervisor. Does NOT relay reports between agents.
```

### Agent table

| Agent | Type | Model | Key tools | CLAUDE.md |
|--------|------|--------|--------------------|-----------|
| **Supervisor** | Relay peer | **Opus** | peer dispatch, Task*, Read, Write, Edit, Bash, MCPs | `Supervisor/CLAUDE.md` |
| **Executor(s)** | Relay peers | Sonnet | peer dispatch, Task*, Read, Write, Edit, Bash, MCPs | `Executor/CLAUDE.md` |
| **Security_Adversarial** | Relay peer | Sonnet | peer dispatch, Task*, Read, WebFetch | `Security_Adversarial/CLAUDE.md` |
| **Code_Adversarial** | Relay peer | Sonnet | peer dispatch, Task*, Read | `Code_Adversarial/CLAUDE.md` |
| **Verifier** | Relay peer | Sonnet | peer dispatch, Task*, Read, Write, Bash | `Verifier/CLAUDE.md` |
| **Investigator** | Relay peer | Haiku | peer dispatch, Task*, Read, Write, WebSearch, WebFetch | `Investigator/CLAUDE.md` |
| **Scribe** | Ephemeral | Sonnet | Read, Write, MCPs (EcoDB, obsidian) | `Scribe/CLAUDE.md` |

### Direct communication

```
BUILD PHASE:
supervisor ──dispatch──→ executor-1: "implement tasks 1-3"
supervisor ──dispatch──→ executor-2: "implement tasks 4-5" (if parallel)
executor-1 ──dispatch──→ supervisor: regular reports (naming, decisions)
executor-2 ──dispatch──→ supervisor: regular reports
executor-X ──dispatch──→ investigator: "I need to know X" (direct research)
supervisor: code review + post-build unification

ATTACK PHASE (both in PARALLEL):
supervisor ──dispatch──→ security-adversarial: "attack version at <path>"
supervisor ──dispatch──→ code-adversarial: "review version at <path>"
security-adversarial ──dispatch──→ supervisor: security report
code-adversarial ──dispatch──→ supervisor: code report

TEST PHASE:
supervisor ──dispatch──→ verifier: "test version at <path>"
verifier ──dispatch──→ supervisor: beta test report

DECIDE PHASE:
supervisor consolidates findings → peer dispatch to orchestrator (Faro)
supervisor + Faro evaluate → Faro prevails → the user if unresolved

FIX PHASE:
supervisor ──dispatch──→ executor(s): consolidated findings to implement

WORKFLOW ESCALATION:
supervisor ──dispatch──→ orchestrator: "I need workflow-integracion for <X>"
Faro presents Gate to the user → approves → Faro pauses and launches auxiliary workflow
```

### Chain of command (non-negotiable)

- **the user**: product decisions (gates, scope, budget).
- **Faro (orchestrator)**: final technical decisions, launching/stopping Executors, invoking auxiliary workflows. Prevails over Supervisor in conflict.
- **Supervisor (Opus)**: implementation decisions, code review, unification, production readiness. Prevails over Executors.
- **Executors/Adversarials/Verifier**: execute and report. Do not decide scope or architecture.

### Incremental dispatch — ZERO IDLE PEERS (v5.2, lessons 2026-05-24 + 2026-05-27)

**Adversarials and Verifier do NOT wait for the full Build phase to finish.** As soon as a task is completed by an Executor, the Supervisor dispatches Adversarials to review that task immediately — while the Executor continues building the next task. The Verifier enters as soon as Adversarials deliver their report on a task.

This is a hard rule, not a suggestion. Every minute an Adversarial or Verifier sits idle while completed code exists unreviewed is wasted. The phases below overlap — they are NOT sequential gates.

```
Task 0 completed ──→ Adversarials attack Task 0 ──→ Verifier tests Task 0
Task 1 completed ──→ Adversarials attack Task 1 ──→ Verifier tests Task 1
  (Executor building Task 2 in parallel with above)
Task 2 completed ──→ Adversarials attack Task 2 ──→ ...
```

#### POST-TASK ATOMIC DISPATCH (v5.2, lesson 2026-05-27 — non-negotiable)

After the Supervisor code-reviews task N, the **NEXT action is ONE batch of peer dispatch calls** — all four in the same turn, no exceptions:

```
# ALL FOUR IN THE SAME TURN — atomic, not sequential
peer dispatch → adv-code:     review task N code
peer dispatch → adv-seg:      review task N security
peer dispatch → verificador:  test task N
peer dispatch → code:          build task N+1
```

**There is no valid reason to dispatch only the Executor and defer the others.** If you catch yourself writing peer dispatch to code without simultaneously writing peer dispatch to adv-code + adv-seg + verificador for the completed task, you are violating ZERO IDLE PEERS.

**Mandatory checklist in orchestration log** after each task completion:

```
Task N COMPLETED — POST-TASK DISPATCH:
  [x] Supervisor code review done
  [x] adv-code dispatched on task N
  [x] adv-seg dispatched on task N
  [x] verificador dispatched on task N
  [x] code dispatched on task N+1
  All 4 in same message batch? YES/NO
```

If any checkbox is empty, the Supervisor does NOT advance to the next task. The checklist is the enforcement mechanism — fill it before moving on.

**Origin**: Echo v0.1.0 Gate 1, 2026-05-27. Supervisor completed code review of T1+T2 (scaffolding + protocol models), dispatched Executor on T3+T4, but left adv-code, adv-seg, and verificador idle. Rationalized as "not enough attack surface in scaffolding." the user caught it. The rationalization was the bug, not the scaffolding.

### Relay peer state (realistic — overlapping phases)

| What's happening | Supervisor | Executor(s) | Sec.Adversarial | Code Adversarial | Verifier | Investigator |
|---|---|---|---|---|---|---|
| Kickoff | **working** | idle | idle | idle | idle | standby |
| Build task N | supervising | **working** | reviewing task N-1 | reviewing task N-1 | testing task N-2 | standby |
| All tasks built | code review | standby fix | **attacking** last batch | **attacking** last batch | testing prev batch | standby |
| Fix phase | supervising | **working** | idle | idle | idle | standby |
| Final loop | coordinating | standby | **attacking** fixes | **attacking** fixes | **testing** fixes | standby |
| Close | **production check** | shutdown | shutdown | shutdown | shutdown | shutdown |

**Minimum 2 complete attack+test passes over the FULL codebase** (not per-task — the second pass reviews everything including fixes from the first pass).

**Anti-patterns to avoid** (all four are the SAME mistake — waiting when you should dispatch):
1. "I'll dispatch adversarials when the build is complete." NO. Dispatch on the FIRST completed task.
2. "I'll dispatch the verifier when the adversarials finish ALL tasks." NO. Dispatch verifier on the first task the adversarials finish reviewing.
3. "Adversarials finished Task 0 review but I'll wait for Task 1 review before sending verifier." NO. Verifier starts on Task 0 NOW.
4. **"This task is just scaffolding / boilerplate / not enough to review."** NO. If code exists and was approved, it gets reviewed. Period. The Supervisor does not evaluate whether a task "deserves" review — the pipeline is mechanical. Completed → reviewed. No judgment call. This rationalization is the #1 way ZERO IDLE PEERS gets violated in practice.

If you catch yourself with ANY idle peer and completed unreviewed/untested work, you are doing it wrong. The pipeline is: Executor completes → Adversarials attack → Verifier tests. Each step flows IMMEDIATELY to the next, per task, not per phase.

**Additional Executors**: Supervisor requests from Faro via peer dispatch. Faro decides and dispatches.

**Escalation to other workflows**: Supervisor detects critical dependency → asks Faro → Gate with the user → Faro invokes workflow-integracion or workflow-adaptacion → returns to construction on close.

**Cost of idle peers**: zero tokens.

---

## Initial setup — file structure (created by the workflow, not by Faro)

Upon confirming Gate B0 with `yes`, Faro executes this setup **before dispatching to the Supervisor**:

### 1. Session folder (coordination artifacts)

```
$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>/
  ├── ENVIRONMENT.md          ← copied from Plantillas/ENVIRONMENT_template.md and filled in
  ├── CONTRACT.md             ← copied from Plantillas/CONTRACT_template.md and filled in
  ├── LESSONS.md              ← copied from Plantillas/LESSONS_template.md (empty)
  └── orchestration.md       ← append-only Faro log
```

### 2. Project folder (technical reports)

```
<project_path>/.faro/
  └── reportes/
        ├── supervisor_kickoff.md
        ├── executor_task_<N>_iter_<M>.md
        ├── verifier_task_<N>_iter_<M>.md
        └── scribe_close.md
```

**Rule**: coordination artifacts (CONTRACT, LESSONS, ENVIRONMENT, log) live in `$FARO_ROOT/Sesiones/`. Implementation-specific reports live in the project under `.faro/reportes/`. The **Plan and Spec** already live in the project folder (produced by workflow-design or created by Faro from template).

### 3. Task list (visible progress tracking)

Immediately after Gate B0 approval, Faro creates a task list using `TaskCreate` — one task per Plan task plus adversarial review, verification, and deployment. Each task includes:
- **subject**: `Task N: <title>` (matches Plan)
- **description**: 1-2 sentence summary of deliverable
- **activeForm**: present continuous for spinner display

Set up dependencies with `TaskUpdate.addBlockedBy` reflecting the Plan's `depende_de` graph. Mark tasks `in_progress` when dispatched to an executor, `completed` when verified. This gives the user real-time visibility into workflow progress.

### 4. Referenced templates

- `$FARO_ROOT/Plantillas/PLAN_template.md`
- `$FARO_ROOT/Plantillas/CONTRACT_template.md`
- `$FARO_ROOT/Plantillas/LESSONS_template.md`
- `$FARO_ROOT/Plantillas/ENVIRONMENT_template.md`

---

## Minimum Plan schema (input validation)

Before dispatching to the Supervisor, **Faro validates** that the Plan has the minimum structure. If any field is missing from any task, Faro **stops and reports to the user** — does not improvise the field.

Each task in the Plan must have:

```
Task N: <short title, imperative>
- objetivo: <1-2 sentences — what is achieved upon completion>
- archivos_a_tocar: [<absolute paths>]
- accion: <literal code, SQL, command, or pseudocode if implementation admits variants>
- pre_condiciones: <system state before — verifiable>
- post_condiciones: <system state after — verifiable>
- tests: [<exact commands the Verifier will run + what they must return>]
- criterio_de_exito: <verifiable bullet list — not "works correctly", yes "test_X.py 12/12 PASS">
- rollback: <exact command if destructive, or literal "no_destructiva">
- depende_de: [<prior tasks that must be OK>] or "ninguna"
```

If the Plan comes from **workflow-design**, it should comply (see SKILL_md_workflow_diseno.md, step 7). If it comes from **the user** or **Faro template**, Faro validates field by field and does not proceed if anything is missing.

---

## Workflow flow (step by step, literal prompts)

### Step 0: Faro validates and prepares

1. Receives assignment from the user.
2. Determines level (trivial/standard/critical) by objective criteria. If uncertain → asks.
3. If critical and no workflow-design Plan exists → **launches workflow-design first**. Returns here when done.
4. Locates Plan + Spec (absolute paths). Validates minimum schema (previous section).
5. Creates session folder and `.faro/reportes/` in the project. Copies templates and fills them in.
6. **Gate B0** — waits for the user's confirmation.
7. Reads `Supervisor/CLAUDE.md` to inject into the prompt.

### Step 1: Join room and dispatch relay peers

```
# Orchestrator joins the relay room
join coordination room

# Dispatch Supervisor (Opus) — department head, persists through the whole workflow
dispatch task to Supervisor

# Dispatch main Executor — persistent builder
dispatch task to Executor-1

# Dispatch Adversarials — await their turn
dispatch task to Security_Adversarial
dispatch task to Code_Adversarial

# Dispatch Verifier — beta tester, awaits its turn
dispatch task to Verifier

# Dispatch Investigator — standby for on-demand research
dispatch task to Investigator
```

### Step 2: Supervisor — kickoff

The Supervisor (already live as a relay peer) receives its assignment via the dispatch prompt. It does:

```
<Supervisor/CLAUDE.md content injected at start>

---

[ASSIGNMENT FOR YOU — Supervisor]

Workflow: construction v5
Session: <session folder path>
Project: <project folder path>
Level: <standard | critical>

Available artifacts (read before starting):
- Plan: <absolute path>
- Spec: <absolute path or "not applicable">
- ENVIRONMENT.md: <absolute path>
- CONTRACT.md: <absolute path>
- LESSONS.md: <absolute path>

Your kickoff (deliver before dispatching the first task):
1. Confirm the Plan meets the minimum schema. If anything is missing, REPORT and stop.
2. Search EcoDB with domain tags and `autor="*"` (minimum: project name, key technologies). Do not filter by author — any agent may have left relevant lessons. Note findings in LESSONS.md.
3. Query EcoDB (neighbors, search_nodes) if the tool interacts with already mapped systems. Note dependencies.
4. Pre-flight checks (run the commands and report the result of each):
   - Active Python venv: `python --version` must match ENVIRONMENT.md
   - Declared dependencies: `pip list` must contain key libraries
   - Required services up: <list from Plan or "none">
   - Declared paths exist: every path in `archivos_a_tocar` of every task
   - **External runtime config** (new in v3): does this refactor touch credentials, environment variables, or the process invocation format? If yes, identify and verify the runtime configuration files that will need synchronized updates. Examples:
     - `claude_desktop_config.json` (MCP servers)
     - Systemd unit files or `docker-compose.yml` (services)
     - `launchd` plists (macOS)
     - Startup scripts in `crontab` or equivalent
     If any needs updating, add it as an implicit sub-task in the Plan — the Supervisor must raise the observation before marking the kickoff as OK.
5. **Cross-validation Prompt↔Spec** (new in v3, critical): for each task in the Plan, verify that cited function names, signatures and structures match Spec §5 (or equivalent). If you detect a conflict between Plan and Spec — the Spec wins. Report the conflict as `BLOCKING_QUESTIONS` in the KICKOFF_REPORT. This also applies to prompts Faro passes you: if Faro instructs something that contradicts the Spec, do NOT dispatch to the Executor — escalate with Gate B2.
6. Identify destructive tasks (rollback != "no_destructiva"). List their numbers — Faro will fire Gate B1 before each one.
7. Report to Faro with the KICKOFF_REPORT format (see CONTRACT.md).

Hard rules:
- You do NOT modify the Plan. If you believe it is defective, you escalate via Gate B2 (after 3 failed iterations on a task).
- You do NOT improvise tasks. You only execute those in the Plan in order, respecting dependencies.
- You do NOT allow the Executor to change scope. If the Executor reports DISAGREEMENT_WITH_PLAN, investigate and decide whether to reformulate its prompt or escalate.
- Executor↔Verifier loop: maximum 3 iterations per task. On the 3rd failure → Gate B2.
```

Supervisor responds with KICKOFF_REPORT. Faro validates it is complete.

### Step 3: Main loop — BUILD → ATTACK → TEST → DECIDE → FIX (minimum 2 loops)

#### BUILD PHASE

The Supervisor assigns tasks from the Plan to Executor(s):
- Independent tasks → can request additional Executors from Faro in parallel
- Destructive tasks → **Gate B1** before each one
- Executors report regularly to Supervisor (naming, library decisions, patterns)
- Supervisor unifies criteria if there are inconsistencies between Executors

When Executors deliver, the Supervisor does a **code review + unification pass** before advancing.

#### 2.2. Supervisor dispatches to Executor

**Literal** prompt that the Supervisor sends to the Executor (via peer dispatch, injected after Executor/CLAUDE.md):

```
<Executor/CLAUDE.md content>

---

[ASSIGNMENT FOR YOU — Executor]

Session: <path>
Iteration: <M> of maximum 3 for this task

Before touching anything:
1. Read ENVIRONMENT.md: <path>
2. Read LESSONS.md: <path> — look for lessons tagged with this technology
3. Read CONTRACT.md section "Executor"
4. **Search EcoDB for prior knowledge** (mandatory):
   search shared memory
   Look for: solved problems, known gotchas, patterns that worked/failed. Do NOT filter by agent_identifier — any agent may have left the solution.

Task to execute:
<literal YAML/markdown block of the task as it appears in the Plan>

Implement ONLY this task. Do NOT touch files outside `archivos_a_tocar`. Do NOT execute actions outside `accion`.

When done:
1. Run the `tests` commands and capture the literal output.
2. Verify `post_condiciones` with concrete commands.
3. Generate EXECUTOR_REPORT (format in CONTRACT.md) and save it at:
   <project>/.faro/reportes/executor_task_<N>_iter_<M>.md
4. Return the report as response.

If tests or post_condiciones fail:
- STATUS = NEEDS_VERIFIER (let the Verifier diagnose)
- Document the failure literally, without interpreting it.
- **If you solve the failure**: save the problem+solution to EcoDB immediately:
  persist to shared memory
  Do NOT wait until session close — save as soon as you solve it.

If you believe the Plan task is poorly defined:
- STATUS = DISAGREEMENT_WITH_PLAN
- Describe the conflict in the DISAGREEMENT field of the report.
- Do NOT modify the task on your own. Only report.
```

#### 2.3. Supervisor dispatches to Verifier (BLIND)

After the Executor, the Verifier **always** enters. It is **blind**: it does not receive the Executor's report, does not receive the iteration history, does not receive the full Plan.

What it **does** receive (Faro prepares it):
- Verifier/CLAUDE.md (injected)
- Only `task_n` from the Plan (extracted) — specifically: `objetivo`, `post_condiciones`, `tests`, `criterio_de_exito`, `archivos_a_tocar`
- ENVIRONMENT.md
- Access to the resulting code (the modified files)

What it does **NOT** receive:
- EXECUTOR_REPORT
- Reports from previous iterations
- Rest of the Plan's tasks
- LESSONS.md (not biased)

**Literal** prompt:

```
<Verifier/CLAUDE.md content>

---

[ASSIGNMENT FOR YOU — Verifier]

Session: <path>
Your attitude: you want to see the system burn, precisely so it does not burn later. You are adversarial but loyal — you look for defects to protect it, not to sabotage it.

You receive only:
- ENVIRONMENT.md: <path>
- Task claimed to have been completed:
    objetivo: <...>
    post_condiciones: <...>
    tests: <...>
    criterio_de_exito: <...>
    archivos_a_tocar: <...>
- Access to the current state of the code in those files.

Your work:
1. Verify `post_condiciones` with concrete commands (do not trust they are met).
2. Run the listed `tests`. Capture literal output.
3. Verify each bullet of `criterio_de_exito` — one by one, with evidence.
4. Actively detect:
   - Coverage gaps: what inputs are not tested?
   - Fragile asserts: what assert would pass even if the code were broken?
   - Unconsidered edge cases: empty, None, unicode, concurrency, limits.
   - Spec drift: does the code do something different from `objetivo`?
5. Apply depth according to complexity:
   - trivial: quick skim
   - standard: full coverage
   - critical: maximum depth (read new functions line by line)

Generate VERIFIER_REPORT (dual markdown-INI + JSON format, see CONTRACT.md) and save it at:
<project>/.faro/reportes/verifier_task_<N>_iter_<M>.md

HARD INVARIANT: if `required_fixes` is empty → `verdict` must be APPROVE. No other combination is possible.
```

#### 2.4. Supervisor processes the VERIFIER_REPORT

Deterministic decision:

| Verifier `verdict` | Supervisor action |
|---------------------------|------------------------|
| `APPROVE` | Marks task_n as completed. Moves to the next one. |
| `APPROVE_WITH_DEBT` (new v3) | Marks task_n as completed. Debt observations (`debt_items` in the report JSON) are logged in `<project>/.faro/debt_backlog.md` with reference to the task. Moves to the next. Debt does NOT block deployment but is traced for future iterations. |
| `REQUEST_CHANGES` with `required_fixes: [B1, B2, ...]` | If iteration M < 3 → re-dispatches Executor with re-iteration prompt (next sub-step). If M == 3 → **Gate B2**. |
| `REJECT` | Stops. Reports to Faro. Faro escalates to the user (not a standard gate — severity escalation). |

#### 2.5. Executor re-iteration (when there is REQUEST_CHANGES and M < 3)

**Literal** prompt for the next iteration:

```
<Executor/CLAUDE.md content>

---

[ASSIGNMENT FOR YOU — Executor, iteration <M+1>]

Previous iteration: REQUEST_CHANGES
Blockers to resolve (ONLY these — do not touch anything else):

<for each id in required_fixes:>
  - <id>: <severity> at <location> — <message>

Rest of state: the current code already has your previous attempt. Modify it to resolve ONLY the listed blockers.

You do NOT receive:
- The full Verifier report (warnings, nits)
- Decisions from previous iterations

When done, same EXECUTOR_REPORT format, saved at:
<project>/.faro/reportes/executor_task_<N>_iter_<M+1>.md
```

> This restriction (only `required_fixes`, not warnings/nits) is designed to prevent scope creep between iterations. Warnings and nits accumulate in LESSONS.md for the next session, but do not enter the active loop.

#### 2.6. After the 3rd failed iteration → **Gate B2**

Supervisor generates proposal report. Faro presents it to the user (format in the "Gates" section).

#### ATTACK PHASE (after Supervisor code review) — NON-SKIPPABLE

The Supervisor dispatches the two Adversarials **in parallel**. This phase is NON-SKIPPABLE alongside Verifier — adv-code catches 6-12 real bugs per session (95% hit rate).

**Adversarial dispatch rules:**
- Security review: max 1 file per peer dispatch with specific concern.
- Code review: max 2 related files per peer dispatch. Otherwise split.
- Max 1 architectural question per peer dispatch.

```
dispatch task to Security_Adversarial
dispatch task to Code_Adversarial
```

Both work simultaneously on the same version. They are independent — they do not coordinate with each other. Both report to the Supervisor when done.

In loop 2+, Adversarials verify that fixes from the previous loop were applied correctly (CROSS_REF_PREVIOUS_LOOP in their reports).

#### TEST PHASE (after Adversarials)

The Supervisor dispatches to the Verifier. **Verificador dispatch rules:**
- Max 5 binary checks per peer dispatch (checkbox + file path + expected behavior).
- Max 1 file per smoke test. No open-ended "review everything" asks.
- If timeout → split ask in half + retry. Never bypass.

```
dispatch task to Verifier
```

The Verifier does beta testing: functional, stress, regressions, user impressions. Reports to Supervisor.

In loop 2+, the Verifier re-runs ALL tests from previous loops (regressions).

#### DECIDE PHASE

The Supervisor consolidates findings from Adversarials + Verifier and reports to Faro:

```
peer dispatch(to="Faro", question="""
CONSOLIDATED_LOOP_N:
  security_adversarial: N vulnerabilities (C critical, H high, M medium)
  code_adversarial: N findings (B bugs, D dead code, U usability)
  verifier: N tests (P pass, F fail, R regressions)
  
  REQUIRED_FIXES_CONSOLIDATED: [unified list]
  ACCEPTABLE_DEBT: [list with justification]
  
  SUPERVISOR_RECOMMENDATION: <implement fixes and do loop N+1 | close with documented debt>
""")
```

Faro + Supervisor decide:
- Which findings are implemented? (REQUIRED_FIXES always, ACCEPTABLE_DEBT per criteria)
- Is another loop needed? (minimum 2 mandatory)
- Is escalation to workflow-integracion/adaptacion needed?
- Faro prevails in conflict → the user if unresolved

#### FIX PHASE (if applicable)

The Supervisor sends consolidated findings to the Executors:

```
dispatch task to Executor-1
```

Back to BUILD PHASE → ATTACK → TEST. Minimum 2 complete loops.

#### CLOSE PHASE — Production Readiness + Scribe

When Supervisor + Faro agree that the version is ready:

1. **Supervisor executes Production Readiness Check** (full checklist in Supervisor/CLAUDE.md)
2. If NOT_READY → fix + re-check (do not close)
3. If READY:

```
# Step 3.5: Knowledge capture — MANDATORY before shutdown (v5.1, lesson 2026-05-24)
# Each peer saves their learnings to EcoDB + reusable scripts to their project dir.
# Do NOT send shutdown_request until all peers confirm knowledge saved.
# Literal prompt for each peer:

dispatch task to Executor-1
dispatch task to Security_Adversarial
dispatch task to Code_Adversarial
dispatch task to Verifier
dispatch task to Investigator

# Wait for ALL confirmations before proceeding to shutdown
# Then shut down peers

dispatch task to Executor-1
dispatch task to Security_Adversarial
dispatch task to Code_Adversarial
dispatch task to Verifier
dispatch task to Investigator
dispatch task to Supervisor

# Dispatch Scribe (ephemeral relay session)
dispatch task to Scribe

# Leave relay room
leave coordination room

# Retrospective (Faro writes directly)
```

### Step 4: Close — Scribe + Faro Retrospective

**New in v3**: before declaring the workflow closed, Faro produces an internal retrospective. It is short (10-15 lines) and lives at `$FARO_ROOT/Sesiones/<date>_<project>/retrospective.md`. Format:

```markdown
# Retrospective workflow-construccion — <project> — <date>

## What worked
- <3-5 bullets of what the SKILL enabled to do well>

## What did not work / where I improvised
- <any point where Faro had to decide something the SKILL did not cover>
- <any gate missing from the SKILL>
- <any typo I (Faro) introduced that was caught or not caught>

## Pain metrics
- Extra iterations due to bugs: N
- Gates fired: [list]
- Bugs detected by Verifier: N
- Approximate token cost: N

## For v<N+1>
- <1-3 concrete changes that would improve the SKILL>
```

This retrospective does not require launching an agent — Faro writes it directly as part of the close. It is input for the next SKILL iteration.

---

When all tasks are in `APPROVE` (or the workflow has been closed by the user's decision at a gate), Faro dispatches the Scribe.

**Literal** prompt:

```
<Scribe/CLAUDE.md content>

---

[ASSIGNMENT FOR YOU — Scribe]

Session: <path>
Project: <path>
Final status: <COMPLETED | ABORTED_AT_TASK_N | MODIFIED_AFTER_GATE_B2>

Document in these locations (all mandatory):

1. Obsidian: $FARO_ROOT/Informes/Construcción/<Name>_<YYYY-MM-DD>.md
   Minimum content:
   - What the tool does (1 paragraph)
   - How to invoke it (exact command)
   - Where it lives (absolute path)
   - Which systems it touches
   - Tasks completed / total
   - Bugs detected by Verifier (summary by severity)
   - Executor DISAGREEMENTS and how they were resolved
   - Gates fired and the user's decisions at each one
   - Telemetry: duration, total iterations, estimated tokens

2. EcoDB — save_memory (agent_identifier: "Scribe"):
   - One memory with tags = [project, key technologies, "construccion"]
   - Summary: what was built, what debt remained

3. EcoDB — save_triples_batch: minimum triples
   - <tool> is_a <type>
   - <tool> lives_at <path>
   - <tool> depends_on <library> (for each key dependency)
   - <tool> interacts_with <system> (for each integration)

Report to Faro with SCRIBE_REPORT confirming all 3 locations updated.
```

---

## Anti-stuck protocols

### Anti-stuck — Supervisor

If the Supervisor does not produce the next dispatch within its turn after receiving a VERIFIER_REPORT, Faro injects:

> *"YOU ARE STUCK. Read the VERIFIER_REPORT. If verdict == APPROVE → dispatch next task. If REQUEST_CHANGES with M<3 → re-dispatch Executor with required_fixes. If M==3 → generate proposal for Gate B2. No other options. Decide now."*

### Anti-stuck — Executor

If the Executor responds without a structured report (free-form, "I think it's fine", etc.), Faro injects:

> *"Your report does not meet EXECUTOR_REPORT (see CONTRACT.md). Generate the report with ALL mandatory fields and save it at the indicated path. No approval without a structured report."*

### Anti-stuck — Adversarials

If an Adversarial returns a report with 0 findings:
> *"New code always has things to find. Change angle. Security_Adversarial tests Unicode, concurrency, race conditions. Code_Adversarial looks for systemic patterns, not just individual bugs. Return at least 3 findings."*

### Anti-stuck — Verifier

If the Verifier approves without invented additional tests:
> *"You are a beta tester, not an automated test runner. Invent at least 3 scenarios the Plan did not contemplate. What would a real user who has not read the documentation do?"*

### Anti-stuck — Faro (orchestrator)

Deterministic action table:

| Signal | Faro action |
|-------|----------------|
| Supervisor requests additional Executor | Evaluate justification → approve or deny |
| Supervisor requests workflow-integracion/adaptacion | Gate with the user → pause/launch if approved |
| Supervisor reports Prompt↔Spec conflict | Gate B2 |
| Supervisor + Faro in disagreement | Faro prevails (document in log) |
| Supervisor + Faro do not resolve | Escalate to the user |
| Supervisor reports CONSOLIDATED_LOOP with ≥1 CRITICAL | Mandatory fix + additional loop |
| Supervisor reports Production Readiness NOT_READY | Mandatory fix + re-check |
| `BLOCKING_QUESTIONS` from any relay peer | Consult the user |
| Scope change from the user | Gate B3 |

---

## Cost and performance (reference)

| Level | Estimated duration | Estimated tokens |
|-------|-------------------|------------------|
| trivial | <15 min | <30k |
| standard | 30-60 min | 80-150k |
| critical (with prior workflow-design) | 90-180 min execution + prior design | 200-500k execution |

---

## Healthy metrics

| Ratio | Target |
|-------|----------|
| Tasks passing on iteration 1 | >60% |
| Tasks requiring iteration 2 | 20-30% |
| Tasks reaching iteration 3 | <15% |
| Gate B2 fired / total tasks | <5% (if it rises, the Plan arrives poorly — review workflow-design) |
| Bugs detected by Verifier / total tasks | 0.3-1.0 (if below 0.3 suspect a lax Verifier) |

---

## When NOT to use this workflow

- Modification of existing code → workflow-evolucion
- Connection between existing systems → workflow-integracion
- Adaptation of system to a new environment → workflow-adaptacion
- Isolated bug with known cause → direct fix
- Cosmetic change (rename, format) → direct fix

---

## Input and output dependencies (information routing between workflows)

### Expected inputs (what this workflow consumes)

For **critical** construction (with prior design):
- **Consolidated design report** at `$FARO_ROOT/Informes/Diseño/<YYYY-MM-DD>_<project>.md`.
- **Raw design artifacts** living in the project itself: `<project_path>/refactor_v<N>_brief.md`, `refactor_v<N>_spec.md`, `refactor_v<N>_plan.md`, `verification_checkpoint.md`. The Supervisor reads them before dispatching to the Executor — especially the Plan (base for tasks) and the Spec (superior authority to Faro, guiding principle 2).

For **standard** construction (without prior design):
- The simple Plan is generated by Faro at startup. No prior design report. It is assumed the scope is clear enough not to require a formal Spec.

**Precondition**: if the task is critical and there is NO design report → Faro aborts this workflow and launches `workflow-diseño` first. Nothing critical is built without Spec+Plan.

### Output — final report archived by the Scribe

- **Obsidian destination folder**: `$FARO_ROOT/Informes/Construcción/`
- **File name**: `<YYYY-MM-DD>_<project_slug>.md`
- **Mandatory YAML frontmatter** — schema in `Scribe/CLAUDE.md`. For construction:
  ```yaml
  workflow: construccion
  version_workflow: "5.0"
  date: YYYY-MM-DD
  project: <human name>
  project_slug: <slug>
  faro_session: $FARO_ROOT/Sesiones/<session>/
  prior_report_consumed: "[[Diseno/YYYY-MM-DD_project]]"  # or null in standard without design
  level: standard | critical
  tasks_completed: N/M
  tasks_approved: N
  tasks_approved_with_debt: N
  tasks_rejected: 0
  next_workflow_suggested: evolucion | none
  faro_artifacts:
    code_deployed: <project_path>
    tests_passing: <list>
    debt_backlog: <faro_session_path>/debt_backlog.md
    retrospective: <faro_session_path>/retrospective.md
  ecodb_memory_ids: [<ids>]
  ecodb_graph_origin: Construccion_<project>_<date>
  tags: [workflow/construccion, status/deployed, project/<slug>]
  ```
- **Mandatory "Traceability" section** at the end: `[[]]` links to prior design (if it exists), to Brief/Spec/Plan used, to tests, to Faro session, EcoDB memories, EcoDB graph.

### Typical next workflow

- **workflow-evolucion** if there is usage feedback that motivates improvements.
- **none** if the product is deployed and stable.

---

## Version history

- **v1.0 (2026-04-16)**: first version, based on EcoDB v2 and utility-tools v2.
- **v2.0 (2026-04-18)**: hardening. Explicit human gates (3), minimum Plan schema formalized, literal prompts for each dispatch, referenced templates, physical artifact locations defined, anti-stuck protocols per agent. Motivated by adherence tests with Opus 4.7 that showed v1 left too much inference to the orchestrator model.
- **v3.0 (2026-04-18, same afternoon)**: refinement post first productive run (refactor eco_graph_mcp v2, 17 tasks, 19 tools deployed). Concrete changes:
  1. **Guiding principle 2**: Spec is superior authority to Faro when they conflict. Supervisor must detect Prompt↔Spec conflicts and fire Gate B2 instead of obeying Faro. Reason: Faro can introduce typos when assembling prompts (happened in Task 10 of the refactor — "estado_grafo" vs "canonizar_predicados").
  2. **Gates with literal options** mandatory. Using A/B/C or 1/2/3 as labels is prohibited. Reason: in the v2 launch, "C" offered as "abort" was understood as "continue". Twice.
  3. **New Gate B3** for scope changes during execution. Reason: in the v2 launch, expanding from 17→19 tools mid-execution was processed by improvising. Now it has a formal channel with mandatory tests.
  4. **External runtime config pre-flight check**: review `claude_desktop_config.json`, systemd units, docker-compose, launchd plists when the refactor touches credentials/env vars/invocation. Reason: in Task 14 `eco_pass_key.txt` was deleted without updating `claude_desktop_config.json`, causing MCP crash on startup due to missing env var.
  5. **New `APPROVE_WITH_DEBT` verdict** from the Verifier to differentiate acceptable debt from a real blocker. Debt is logged in `<project>/.faro/debt_backlog.md` with reference to the task. Reason: in Task 9 the Executor reported technical debt (harness duplicates inline migration) that did not block but deserved traceability.
  6. **Faro retrospective final step**: before closing, Faro writes 10-15 lines about what worked / what did not / what goes into v+1. Lives at `$FARO_ROOT/Sesiones/.../retrospective.md`. Reason: without this step, the workflow is declared "success" and Faro does not evaluate its own failures.
  7. **Expanded Faro anti-stuck table** with the new verdict, Gate B3 and Prompt↔Spec conflict detection.

  What did NOT change from v2: minimum Plan schema (9 fields), literal prompts for each dispatch, templates, physical artifact locations, parallelization of independent tasks. These proved to work well in the launch.

- **v4.0 (2026-04-26)**: migration to Agent Teams + team redesign by Prima. Changes:
  1. **Supervisor upgraded to Opus** — from site foreman to department head. Code review, unification of criteria across Executors, production readiness checklist.
  2. **Executors as parallel teammates** — Supervisor can request more from Prima. Executors report regularly to Supervisor. Persist through the whole workflow.
  3. **Two new Adversarials** (Security_Adversarial + Code_Adversarial) replace the Verifier as "attacker". Run in parallel. Security thinks like a hacker, Code thinks like a senior dev.
  4. **Verifier becomes beta tester** — functional, stress, regressions, user impressions. No longer a blind adversarial.
  5. **Minimum 2 loops** BUILD→ATTACK→TEST→FIX→ATTACK→TEST mandatory.
  6. **Workflow escalation** — Supervisor can request workflow-integracion or workflow-adaptacion for critical dependencies.
  7. **Production Readiness Check** — formal checklist before close.
  8. **Explicit chain of command**: the user (product) > Prima (final technical) > Supervisor (implementation) > Executors (execution).
  9. Direct communication via Agent Teams. Prima does not relay reports.
  10. Motivation: this workflow is going to build EcoDB and serious tools. Vibe coding with production quality control.

- **v5.0 (2026-05-22)**: relay rewrite. Agent Teams replaced by relay peers (separate Claude Code sessions). All TeamCreate/Agent/SendMessage/TeamDelete API calls replaced with relay_join/peer dispatch/relay_leave. Agent names translated to English. All gates, workflow terms, paths and memory references updated. Full document translated to English.

- **v5.2 (2026-05-27)**: ZERO IDLE PEERS enforcement. Three changes from Echo v0.1.0 Gate 1 session:
  1. **POST-TASK ATOMIC DISPATCH**: after Supervisor code-reviews task N, ALL FOUR peer dispatch calls (adv-code + adv-seg + verificador + code) must happen in the same turn. No sequential dispatch, no deferral.
  2. **Anti-pattern #4**: "This task is just scaffolding / not enough to review" added as explicit violation. The pipeline is mechanical — completed = reviewed. No judgment call.
  3. **Mandatory checklist** in orchestration log after each task completion. 5 checkboxes, all must be filled before advancing. Enforcement mechanism, not documentation.
