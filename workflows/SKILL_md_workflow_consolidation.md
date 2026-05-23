---
name: workflow-consolidation
description: |
  Orchestrated workflow for periodic system audit against real usage. Mines session artifacts,
  classifies divergences between documented methodology and actual practice, updates core
  documentation, and validates changes. Use when: preparing for release, after N=15 sessions,
  after major pivot, or when documentation feels stale. Today's prototype (2026-05-22) is v0.
metadata:
  version: "1.0"
  creation: 2026-05-22
  author: Hilo
  design_doc: "$FARO_ROOT/Informes/Diseño/2026-05-22_faro_consolidation_github_release.md"
tags:
  - agent/investigator
  - agent/weaver
  - agent/challenger
  - agent/visual_adversarial
  - agent/verifier
  - agent/scribe
  - agent/archivist
  - workflow/consolidation
---

# Workflow: Consolidation (v1 — Relay)

Audits the Faro system against real usage. Mines session logs, retrospectives, and EcoDB memories to find divergences between what's documented and what actually happens, then updates core documentation.

> **Governing principle 1 — Do not improvise**: every finding must cite its source file and line. Classification requires evidence.
>
> **Governing principle 2 — Session artifacts > orchestrator memory**: what the logs say overrides what the orchestrator remembers. If FARO_ESTADO says X but 5 retrospectives show Y, the documentation is wrong.

---

## Trigger

**Dual trigger** — whichever fires first:
- **Periodic**: every N=15 sessions since last consolidation
- **Event-driven**: release preparation, major pivot, stack change, when the user says "update the system"

Phase 0 defines which trigger activated and adjusts scope accordingly.

---

## The 4 gates (mandatory)

| Gate | When | What orchestrator presents |
|---|---|---|
| **B0** | After loading workflow, before dispatching first agent | "Loaded workflow-consolidation. Trigger: [periodic/event]. Scope: [sessions X to Y / full audit]. Proceed?" |
| **B1** | After Phase 1 (findings collected, both L1+L2 passes) | "Investigators found N findings across L layers. [Summary]. Review before classification?" |
| **B1.5** | After Phases 2.5+2.75 (plan attacked + verified) | "Action plan: N bugs to fix, N evolutions, N lessons. Challenger found [issues]. Verifier confirms [coverage]. Approve plan before executing changes?" |
| **B2** | After Phase 3.5 (executed changes verified) | "Core docs updated. Verifier confirms [status]. Approve before final adversarial attack?" |
| **B3** | If scope changes during execution | "Scope change detected: [what changed]. Adjust scope or continue?" |

**Always literal options at gates.** Never A/B/C.

---

## Agent composition (7 relay peers)

| Agent | Model | Role in this workflow |
|---|---|---|
| **Investigator** (mode 4: archaeology) | Haiku | Mines session artifacts for divergences, patterns, failures |
| **Weaver** | Sonnet | Classifies findings, produces consolidated analysis |
| **Challenger** | Sonnet | Attacks updates — missed items? Evolution disguised as drift? |
| **Visual Adversarial** | Sonnet | Attacks visual quality of updated documentation |
| **Verifier** | Sonnet | Verifies updates match findings (NON-SKIPPABLE) |
| **Scribe** | Sonnet | Archives to vault + EcoDB + graph |
| **Archivist** (pre-flight) | Haiku | Checks what's already been consolidated |

---

## Phases

### Phase 0 — Scope definition
**Owner**: Orchestrator

1. Determine trigger type (periodic or event-driven).
2. Define session range: from last consolidation to now.
3. If event-driven (release): scope = full audit of ALL documentation.
4. If periodic: scope = delta only (sessions since last consolidation).
5. **Archivist pre-flight**: search EcoDB for previous consolidation memories (`type="observation"`, `tags=["consolidation"]`). What was last consolidated and when?
6. Present scope at **Gate B0**.

### Phase 1 — Collection + archaeology
**Owner**: Investigator (mode 4: archaeology, Haiku)

Dispatch via dispatch task to Investigador. Max 2 tasks per ask.

Task: mine all session folders in scope range. THREE source layers per session:

**Layer 1 — Written artifacts** (orchestrator self-report):
- `orchestration.md` — decision log
- `retrospective.md` — session reflection
- `debt_backlog.md` — technical debt

**Layer 2 — Claude Code session logs** (ground truth):
- Raw JSONL session transcripts from `~/.claude/projects/*/` (one .jsonl per session)
- Contains: every tool call, every relay message, every error, every agent dispatch
- **Extraction**: Investigators use the `session-log-archaeology` skill (installed at `Investigator/.claude/skills/<workflow>/SKILL.md The skill runs `extract.py` which parses ALL JSONL files across ALL projects and produces per-project markdown reports with: tool usage counts, skill invocations, repeated file edits, error patterns, relay call stats, agent dispatches.
- **Analysis targets**: (a) REPEATED WORK — files edited 10+ times across sessions (same bug re-fixed?), (b) ERROR CLUSTERS — same error 3+ times (solution saved to EcoDB?), (c) SKILL GAPS — available skills never invoked, (d) TOOL ANOMALIES — high Edit/low Read = editing blind, (e) BEHAVIORAL SIGNALS — peer dispatch without reply, Agent re-dispatches, low save_memory relative to session count.
- **Execution**: Phase 1 runs in TWO passes. Pass 1 = Layer 1 (vault artifacts). Orchestrator reviews findings at interim checkpoint. Pass 2 = Layer 2 (session logs via extraction script). Investigators get `/clear` or restart between passes to free context. Both passes feed into Gate B1.
- This is where you find what ACTUALLY happened vs what the orchestrator CHOSE to document

**Layer 3 — EcoDB memories** (cross-agent perspective):
- search shared memory — any agent may have recorded something the orchestrator missed
- search recent memories — all memories from that day

**Why all three layers matter**: Layer 1 is filtered by the orchestrator's judgment. Layer 2 is unfiltered ground truth. Layer 3 captures what other agents noticed. Divergences BETWEEN layers are findings themselves — if the retrospective says "smooth session" but the logs show 4 retries and 2 errors, that's a finding.

Produce structured findings using this schema:

```
FINDING_ID: C-NNN
TYPE: DIVERGENCE | RECURRING_FAILURE | UNDOCUMENTED_LESSON | EMERGENT_PRACTICE
SEVERITY: BLOCKER | IMPORTANT | MINOR
SOURCE: <session folder>/<file>
DESCRIPTION: <what was found>
EVIDENCE: <quote or reference>
RECOMMENDATION: ACCEPT_AS_EVOLUTION | FIX | DOCUMENT | ARCHIVE
```

Also collect quantitative metrics (if available from retrospectives):
- Total sessions in range
- Adversarial findings per session (approximate)
- Recurring patterns (3+ occurrences)

**If structured evaluations exist** (`type="observation"`, `tags=["evaluation"]`): consume them as additional input alongside session mining.

Present findings at **Gate B1**.

### Phase 2 — Classification
**Owner**: Orchestrator (as Weaver)

Dispatch via dispatch task to Tejedor.

Orchestrator classifies each finding into:

| Category | Action |
|---|---|
| **EVOLUTION_TO_ACCEPT** | Document as canonical. Update FARO_ESTADO + relevant docs. |
| **BUG_TO_FIX** | Something is wrong and needs correction. |
| **UNDOCUMENTED_LESSON** | Real lesson not captured in §11 or CLAUDE.md. Document it. |
| **EMERGENT_PRACTICE** | Team does X consistently but no doc describes it. Formalize or reject. |

**Every finding MUST include all 6 fields below. Incomplete entries are rejected by Challenger/Verifier.**

```
ID: B/E/L/P-xx
CATEGORY: BUG_TO_FIX | EVOLUTION_TO_ACCEPT | UNDOCUMENTED_LESSON | EMERGENT_PRACTICE
RAW SOURCES: which investigator findings feed this item (traceability)

CONTEXT:
  What: [what is happening]
  Impact: [quantitative — how often, how much waste, what breaks]
  Why it matters: [consequence if not addressed]

SOLUTION:
  Problem in plain language: [1-2 sentences — what goes wrong, why, in terms anyone can understand]
  Why this fix solves it: [the logic — WHY this action addresses the root cause, not just what to do]
  Action: [concrete — exact document, exact section, exact text to add/change]
  Who: [orchestrator | code peer | specific agent]
  Dependencies: [which other items must complete first]

SUCCESS CRITERIA:
  Short term (this session): [verifiable check — e.g., "rule text exists in Preamble §X"]
  Medium term (5 sessions): [behavioral check — e.g., "zero session-close attempts in 5 consecutive sessions"]
  Long term (15 sessions): [metric target — e.g., "save_memory compliance >80% across all agents"]
```

**HISTORICAL items** (cannot recur due to system changes) must be explicitly listed with justification for why they're closed.

**Deduplication mapping**: for every raw finding NOT appearing as its own consolidated item, state which consolidated item absorbs it. No silent drops.

Orchestrator produces TWO separate documents at different stages:

**1. Technical classification** (Phase 2 output → agents consume):
Full schema with all fields, dedup mapping, dependency order. This is the attack surface for Challenger and Verifier. The user does NOT read this document.

Goes to Challenger (Phase 2.5) and Verifier (Phase 2.75) for attack and validation. Loops until both approve.

**2. Decision report** (post-approval → user consumes at Gate B1.5):
Written by the orchestrator AFTER Challenger + Verifier approve the technical classification. This is a SEPARATE document, not a reformatting — it's a distillation that proves the orchestrator understood everything.

The decision report is the ONLY document the user reads. Requirements:
- **Self-contained**: the user reads this cold, without having seen any other document from this workflow. No references to finding IDs (C-301, inv4-T408), no "see dedup mapping", no schema fields.
- **One section per problem**: what's happening (plain language), why it happens (root cause), what I propose (concrete action), why my proposal fixes the root cause (the logic, not just "add rule to doc"), and how we'll know it worked (success criteria in human terms).
- **Honest about limits**: what's blocked, what we're deferring, what we don't know yet.
- **Test**: if the user has to ask "what does this mean?" or "why would that help?", the report failed.

Lienzo renders the decision report as HTML. The user reviews at Gate B1.5.

### Phase 2.5 — Adversarial attack on ACTION PLAN (NON-SKIPPABLE)
**Owner**: Challenger (Sonnet)

Dispatch via dispatch task to Cuestionador.

Challenger attacks the PLAN BEFORE any documents are modified. Three axes:

1. **MISSED FINDINGS**: Cross-reference raw investigator reports against consolidated classification. Was any finding silently dropped?
2. **MISCLASSIFICATION**: Is any EVOLUTION_TO_ACCEPT actually unintended drift? Is any BUG_TO_FIX actually working-as-designed?
3. **ACTION GAPS**: For each BUG_TO_FIX, does the proposed action address root cause or just symptoms? Will it prevent recurrence?

### Phase 2.75 — Verification of ACTION PLAN (NON-SKIPPABLE)
**Owner**: Verifier (Sonnet)

Dispatch via dispatch task to Verificador.

Verifier validates coverage:

1. **COVERAGE**: Every raw finding from every investigator maps to a consolidated item. No silent drops.
2. **ACTION COMPLETENESS**: Every BUG_TO_FIX specifies: WHICH document, WHAT to change, WHO does it.
3. **NO REGRESSIONS**: Proposed actions don't contradict existing FARO_ESTADO rules or agent CLAUDE.md content.

Present verified plan at **Gate B1.5** (user reviews plan before execution).

### Phase 3 — Update core docs
**Owner**: Executor (dispatched by orchestrator) + Orchestrator for architectural decisions

Based on verified classification (post Phase 2.5 + 2.75):
- **FARO_ESTADO**: update relevant sections (orchestrator specs changes, code executes)
- **Agent CLAUDE.md**: update affected agents (orchestrator specs, code writes)
- **SKILL files**: update if workflow mechanics changed (orchestrator writes — architectural)
- **§11 Lessons**: add new lessons (orchestrator drafts, code formats)

Architect-level changes (FARO_ESTADO structure, SKILL mechanics, enforcement rules) = orchestrator writes.
Mechanical changes (translations, formatting, path fixes) = code peer writes.

### Phase 3.5 — Verification of EXECUTED CHANGES (NON-SKIPPABLE)
**Owner**: Verifier (Sonnet)

Dispatch via dispatch task to Verificador.

Verifier checks the ACTUAL document changes:
- Every action from the verified plan was executed
- No action was silently dropped or partially applied
- Updated docs are internally consistent
- No regressions introduced (e.g., section that was correct now has errors)

Present verification at **Gate B2**.

### Phase 4 — Adversarial attack on FINAL RESULT
**Owner**: Challenger + Visual Adversarial (parallel, Sonnet)

Dispatch both in parallel:
- dispatch task to Cuestionador
- dispatch task to Adversarial_Grafico

Challenger attacks the executed result:
- Do the changes actually fix what the plan said they'd fix?
- Are enforcement mechanisms actually enforceable?
- Did execution introduce new problems?

Visual Adversarial attacks:
- Document readability and structure quality
- Consistent formatting across updated sections

### Phase 5 — Archive
**Owner**: Scribe (Sonnet)

Dispatch via dispatch task to Escribano.

Scribe archives:
- Consolidation report → `$FARO_ROOT/Informes/` (new folder: `Consolidation/`)
- Session summary → EcoDB (`type="observation"`, `agent_identifier=<orchestrator>`, `tags=["consolidation", "session-close"]`)
- Decision triples → EcoDB graph
- **If abstract.py exists**: regenerate public/ variant from updated internal files

### Phase 6 — Retrospective
**Owner**: Orchestrator

Write `retrospective.md` in session folder:
- What worked in this consolidation
- What didn't work
- What to change in workflow-consolidation v1.1
- Metrics: findings count, classification breakdown, time spent

Save to EcoDB as session close memory.

---

## Dependencies

### Input
- Previous consolidation date (from EcoDB or manual)
- Session folders in `$FARO_ROOT/Sesiones/`
- Current FARO_ESTADO, CLAUDE.md files, SKILL files

### Output
- Updated FARO_ESTADO + indices
- Updated CLAUDE.md files (if needed)
- Updated SKILL files (if needed)
- Consolidation report in `$FARO_ROOT/Informes/Consolidation/`
- EcoDB memories + graph triples
- Retrospective

### Next workflow
- If consolidation reveals need for new feature → workflow-design
- If consolidation reveals broken implementation → workflow-evolution
- Regular operation → next consolidation in N=15 sessions

---

## Self-improvement hooks (v2 foundation)

Phase 1 can consume structured session evaluations if they exist (`type="observation"`, `tags=["evaluation"]`). In v1, these are generated manually during Session Close Protocol. In v2, an automated Evaluator agent will generate them post-session.

Phase 2 can classify improvement proposals alongside divergences. Weaver uses Template #21 (IMPROVEMENT_PROPOSAL_template.md) for proposals that emerge from pattern analysis.

Phase 5 Scribe can trigger `abstract.py` to regenerate the public variant if the consolidation updated internal files that feed the public repo.
