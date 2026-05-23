# Improvement Proposal — [title]

---
workflow: consolidation
date: YYYY-MM-DD
source_session: [session that generated this proposal]
author: [agent identifier]
---

## Proposal

| Field | Value |
|---|---|
| **PROPOSAL_ID** | IMP-NNN |
| **TYPE** | NEW_SKILL / NEW_TOOL / NEW_ANTI_PATTERN / ECODB_GAP |
| **SOURCE** | Session evaluation [session ID] or consolidation finding [finding ID] |
| **PATTERN** | What recurring behavior was detected (with evidence from N sessions) |
| **PROPOSAL** | What to build, configure, or change |
| **EFFORT** | LOW (< 1 session) / MEDIUM (1-2 sessions) / HIGH (3+ sessions) |
| **PRIORITY** | Frequency × Impact score. HIGH if pattern recurs 3+ times with measurable cost. |
| **STATUS** | PROPOSED / APPROVED / IMPLEMENTED / REJECTED |

## Evidence

Sessions where the pattern was observed:

| Session | Date | What happened | Cost/Impact |
|---|---|---|---|
| [session 1] | YYYY-MM-DD | Description | Time lost / tokens wasted / bug introduced |
| [session 2] | ... | ... | ... |

## Proposed Solution

Concrete description of what to build or change:

- **If NEW_SKILL**: name, trigger conditions, phases, agents involved
- **If NEW_TOOL**: MCP tool specification, inputs/outputs, integration point
- **If NEW_ANTI_PATTERN**: rule text, where to encode (Preamble / CLAUDE.md / SKILL), enforcement mechanism
- **If ECODB_GAP**: what's missing from EcoDB that caused repeated manual work

## Acceptance Criteria

- [ ] Criterion 1 (verifiable)
- [ ] Criterion 2 (verifiable)

## Rejection Criteria

Under what conditions this proposal should be REJECTED:

- If [condition], this proposal doesn't make sense because [reason].

---

## Traceability

- Consolidation session: [[consolidation_session]]
- Related findings: [FINDING_IDs from consolidation]
- EcoDB memory IDs: [list]
