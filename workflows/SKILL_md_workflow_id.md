---
name: workflow-id
description: |
  Strategic R&D workflow. Evaluates an existing system, researches the state of the art, and produces a proposal for the next technological leap. Does not execute changes — generates the brief for workflow-design. This is the Chief R&D Officer's workflow: look at what we have, research what exists, and propose where to go. Each phase produces an autonomous deliverable approved by the user. If it stops midway, nothing is lost.
metadata:
  version: "2.0"
  relay_rewrite: 2026-05-22
  created: 2026-04-26
  author: Prima
  invocation: relay session (separate Claude Code instance)
  motivation: |
    Eco Consulting needs a workflow that is neither pure research (no code) nor tactical evolution (fix what exists). R&D is the hybrid: audits the present, researches the future, and proposes the leap. Real cases waiting: EcoDB v3, infrastructure of agents post-Agent Teams.
tags:
  - workflow/id
  - agent/auditor
  - agent/audit_adversarial
  - agent/pioneer
  - agent/guardian
  - agent/pragmatist
  - agent/investigator
  - agent/scribe
---

# Workflow: R&D (v2.0 — Relay)

Evaluates an existing system and proposes its next level. Does not fix bugs or refactor — **decides the future**. Produces a well-formulated brief for workflow-design.

> **Guiding principle 1 — Each phase is autonomous**: if the user stops the workflow at any phase, there is a useful deliverable. The audit report stands on its own. The research focus areas stand on their own. The vision proposal stands on its own. Nothing depends on the workflow reaching the end.
>
> **Guiding principle 2 — R&D feeds, does not execute**: this workflow does NOT launch workflow-design or workflow-construction internally. It produces well-formulated briefs that the user approves and Prima executes as independent workflows. No nested workflows, no fragility.
>
> **Guiding principle 3 — Real constraints first**: any leap proposal is tested against our real constraints (stack, budget, team knowledge, existing dependencies). A proposal that ignores constraints is fantasy, not R&D.
>
> **Guiding principle 4 — The state of the art is not the answer**: knowing what exists outside is input, not output. The output is what WE do with that information given who we are and what we have.

---

## When it activates

Prima launches this workflow when:
1. the user asks "what could we improve about X?" at a strategic, not tactical, level
2. A system has fulfilled its original purpose and needs to evaluate the next step
3. New technology changes the rules of the game for an existing system
4. Prima detects accumulated technical debt that deserves a deep review

Typical phrases: "look at EcoDB and tell me what's missing", "does our agent infrastructure scale?", "is there something better than ChromaDB for what we do?"

**NOT** launched for:
- Bugs or tactical improvements → workflow-evolution
- Researching a topic without an existing system → workflow-investigation
- Building something new → workflow-construction

---

## The 3 gates (between each phase)

### Gate B0 — Load confirmation + system to evaluate

```
[GATE B0 — Load confirmation]
I have loaded workflow-r&d v2.0.

System to evaluate: <name + path>
Motivation: <why now>

Orchestration plan:
- Phase 1: Audit of current system → Audit Report
- Phase 2: State-of-the-art research → separate workflow-investigation
- Phase 3: Vision proposal → Brief for workflow-design

Each phase produces an independent deliverable with an approval gate.

Options:
- "Proceed with audit" — I start Phase 1.
- "Adjust scope" — describe what to adjust.
- "Do not proceed" — I cancel.

What do I do?
```

### Gate B1 — Audit approval + research focus areas

After Phase 1. Prima presents:

```
[GATE B1 — Audit completed]
System: <name>
Audit Report: <path>

Summary:
- Current state: <1-2 sentences>
- Detected limitations: N
- Leap opportunities: M
- Accumulated debt: K items

Proposed research focus areas (format ready for workflow-investigation):
- F1: <concrete question about state of the art>
- F2: <question about technological alternative>
- F3: <question about scalability/future>

Options:
- "Approve focus areas — launch workflow-investigation with these focus areas" — Prima launches it as a separate workflow
- "Adjust focus areas" — describe what to change
- "Stop here — the audit is sufficient for now" — archive and close
- "Scale to deep" — the focus areas are complex, use workflow-investigation-deep

What do I do?
```

### Gate B2 — Vision proposal approval

After Phase 3. Prima presents:

```
[GATE B2 — Vision proposal]
System: <name>
Proposal: <path>

Summary:
- Proposed leap: <1-2 sentences>
- Estimated cost: <tokens, time, complexity>
- Main risk: <what could go wrong>
- Conservative alternative: <what we would do if we don't make the leap>

Brief formulated for workflow-design:
<text of the brief ready to copy and paste>

Options:
- "Approve — launch workflow-design with this brief" — Prima executes it
- "Adjust the proposal" — describe what to change
- "Save but don't execute yet" — archive for future
- "Reject — does not merit the leap" — close with justification

What do you decide?
```

---

## System agents — Relay

```
join coordination room

RELAY PEERS (separate sessions):
├── Auditor (OPUS) — reads the full system, produces report + focus areas
├── Adversarial_Audit (Sonnet) — second reading: verifies completeness and dependencies
├── Pioneer (Sonnet) — advisory council: advocates for innovation and technological leap
├── Custodian (Sonnet) — advisory council: advocates for improving what exists
├── Pragmatist (Sonnet) — advisory council: evaluates cost vs benefit without emotion
└── Investigator (Haiku) — standby for quick queries

SUBAGENT:
└── Scribe (Sonnet) — archives at close

LEAD (Prima):
└── Directs, produces vision draft, synthesizes council debate (double vote).
```

### Agent table

| Agent | Type | Model | CLAUDE.md |
|--------|------|--------|-----------|
| **Auditor** | Relay peer | **Opus** | `Arquitecto/CLAUDE.md` (Auditor mode) |
| **Adversarial_Audit** | Relay peer | Sonnet | `Adversarial_Auditoria/CLAUDE.md` |
| **Pioneer** | Relay peer | Sonnet | `Pionero/CLAUDE.md` |
| **Custodian** | Relay peer | Sonnet | `Custodio/CLAUDE.md` |
| **Pragmatist** | Relay peer | Sonnet | `Pragmatico/CLAUDE.md` |
| **Investigator** | Relay peer | Haiku | `Investigador/CLAUDE.md` (standby) |
| **Scribe** | Subagent | Sonnet | `Escribano/CLAUDE.md` |

### R&D Advisory Council (peer review of the vision)

Prima produces the proposal draft. Then submits it to the council:

- **Pioneer**: sees the opportunities, advocates for the leap, points out the risk of not changing. Honest — if it's not worth it, says so.
- **Custodian**: protects what works, proposes the incremental alternative, points out what is lost with the change. Accepts change when the data wins.
- **Pragmatist**: without emotion, calculates cost vs benefit, ROI, quantified risk. Doesn't care if it's new or old — cares if the numbers add up.

**Prima synthesizes with double vote.** If there is 2-1 in the council, Prima breaks the tie. If there is 3-0 against Prima, Prima can maintain its position but must justify it explicitly to the user.

### Chain of command

- **the user**: approves each phase, decides whether to make the leap. Receives each deliverable WITH the adversarial critique AND the council debate.
- **Prima**: directs, produces vision draft, synthesizes council, formulates brief. Double vote.
- **Auditor**: reports the present. Does not decide the future.
- **Council (Pioneer/Custodian/Pragmatist)**: advise. Do not decide. Prima synthesizes.

#### WARNING — Correct agent invocation rule (2026-04-28)

**ALL agents are launched as relay sessions with a clean context + peer name.**

```
dispatch task to <agent-name>
```

**NEVER pass the full lead context to a peer.** Peers only need their brief.

**Incident 2026-04-28:** 7 investigators launched without clean context = 700k tokens burned just on startup.

---

## Workflow flow

### Step 0: Prima validates and prepares

1. Receives brief from the user.
2. Pre-flight:
   - System exists on disk and is accessible
   - EcoDB accessible
   - Prior documentation of the system in Obsidian (search in R&D/)
3. Creates session folder.
4. **Gate B0**.

### Phase 1 — Audit (Auditor Opus)

Prima contacts the Auditor with a specific brief:

```
peer dispatch(to="Auditor", question="""
[BRIEF — Auditor, Phase 1 of workflow-r&d]

System to audit: <path>
the user's motivation: <literal>

Your task:
1. Query EcoDB (`search` tool) with author='*' — find system history, past decisions, documented debt.
2. Query EcoDB graph (neighbors, search_nodes) — find relationships, dependencies, integrations.
3. Search in Obsidian — prior reports on this system.
4. Read the CURRENT code/configuration completely.
5. Produce R&D AUDIT REPORT with these sections:

## 1. Current state
- What the system does today (functional)
- How it is used (integrations, users, frequency)
- Real metrics (performance, volume, cost)
- Current technical stack with versions

## 2. Detected limitations
- L<N>: description + evidence + current impact
- Classification: design limitation | technical debt | obsolescence | scale

## 3. Leap opportunities
- O<N>: what could be different + why it matters
- Do not propose solutions — identify SPACES for improvement

## 4. Accumulated debt
- From EcoDB: deferred decisions, documented debt
- From code: TODOs, workarounds, documented hacks
- From architecture: decisions that don't scale

## 5. Proposed research focus areas
- F<N>: concrete question about state of the art (format ready for workflow-investigation)
- Each focus must answer: "does something better exist for <limitation L<N>>?"

## 6. What NOT to touch (what works well and does not merit change)

Save in: <session>/audit_report.md
""")
```

When the Auditor delivers:

```
dispatch task to Adversarial_Audit
```

Adversarial_Audit verifies completeness → reports to Prima.

→ **Gate B1** with the user (audit report + Adversarial verification + proposed focus areas).

### Phase 2 — Research (separate workflow)

If the user approves the focus areas → Prima launches `/workflow-investigation` or `/workflow-investigation-deep` as an **independent** workflow. Not inside this relay room.

When the research closes and the report is in Obsidian → Prima resumes this workflow.

### Phase 3 — Vision (Prima + Advisory Council)

**Step 3.1**: Prima synthesizes:
- Audit report (what we have)
- Research report (what exists outside)
- Eco Consulting reference (our real constraints)
- Its own judgment as R&D chief

Produces **draft** Vision Proposal.

**Step 3.2**: Prima submits the draft to the Council:

```
dispatch task to Pioneer
dispatch task to Custodian
dispatch task to Pragmatist
```

The three evaluate in parallel. Each reports to Prima with its opinion format.

**Step 3.3**: Prima synthesizes the debate (double vote):
- If consensus → reinforces the proposal
- If dissent → documents the positions and justifies its decision
- If 3-0 against Prima → can maintain position but makes it explicit to the user

Produces **definitive Vision Proposal** (draft + council debate integrated).

→ **Gate B2** with the user (proposal + council opinions + Prima synthesis).

### Vision Proposal format

Produces **Vision Proposal**:

```
# Vision Proposal — <system> v<next>

## 1. Proposed leap
What we change and why. Not incremental — strategic.

## 2. Justification
- Limitations it resolves (reference to audit report)
- State of the art that enables it (reference to research report)
- Our constraints it respects (reference to Eco Consulting)

## 3. What does NOT change
What we preserve from the current system and why.

## 4. Estimated cost
- Complexity of the workflow-design that will follow
- Tokens/time estimated for design + construction
- Main risk and mitigation

## 5. Conservative alternative
What we would do if we don't make the leap. Why it is not enough.

## 6. Brief for workflow-design
Text ready to copy as input for /workflow-design.
```

→ **Gate B2** with the user.

### Close

Scribe archives everything (audit report + vision proposal) in Obsidian + EcoDB (`save_memory` tool) + EcoDB graph (`save_triple` tool).

```
leave coordination room
```

Prima's retrospective.

---

## Setup — file structure

```
$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<system>_id/
  ├── audit_report.md              ← Phase 1 (Auditor)
  ├── vision_proposal.md           ← Phase 3 (Prima)
  ├── orchestration.md
  └── retrospective.md

Obsidian destination: $FARO_ROOT/Informes/I+D/<YYYY-MM-DD>_<system>.md
```

---

## Cost and performance

| Phase | Estimated duration | Estimated tokens |
|------|-------------------|------------------|
| Audit | 20-40 min | 50-150k (Opus reads code) |
| Research | (separate workflow) | (depending on light/deep) |
| Vision | 10-20 min | ~30-50k (Prima synthesizes) |

---

## Version history

- **v2.0 (2026-05-22)**: relay rewrite. Migrated from Agent Teams to Relay. TeamCreate/SendMessage/TeamDelete → relay_join/peer dispatch/relay_leave. Agent spawn code blocks removed. Agent names translated to English. All Spanish text translated. Paths updated to $FARO_ROOT/ pattern.
- **v1.0 (2026-04-26)**: created by Prima. Strategic R&D workflow with 3 autonomous phases (audit, research, vision). Each phase with gate. Does not execute other workflows — feeds them. Motivation: Eco Consulting needs to evaluate existing systems (EcoDB, agent infrastructure) and decide technological leaps with criteria, not improvisation.
