# Project Synthesis — [project name]

> **This document is the single source of truth** for the project as of its v1 completion. It synthesizes all design documents, construction reports, adversarial findings, session logs, and EcoDB memories into one definitive record. When ingested into EcoDB, this document IS the project.

---
workflow: project-synthesis
date: YYYY-MM-DD
project: [project name]
project_slug: [slug]
sessions_covered: [first session] to [last session]
total_sessions: N
author: [Weaver agent identifier]
design_docs: [[design_doc_1]], [[design_doc_2]]
construction_reports: [[construction_report_1]]
adversarial_reports: [[adversarial_report_1]]
---

## 1. Objective

What the project set out to do. Original scope as stated by the human owner. 2-4 sentences. Include the original trigger — what problem or need started this project.

## 2. Design Decisions (from design documents)

Sourced from Brief + Spec + Plan produced by workflow-design. Each decision includes its traceability:

| Date | Decision | Rationale | Alternatives discarded | Source | Traceability |
|---|---|---|---|---|---|
| YYYY-MM-DD | What was decided | Why | What was considered and rejected | Session/memory ref | research [P1] / user-brief / my-inference |

## 3. Final Architecture (from construction reports)

What was actually built (not what was planned). Sourced from construction reports + production readiness checklists:

- **Components and relationships**: what exists, how pieces connect
- **Technology stack**: with exact versions deployed
- **Data flow**: how information moves through the system
- **Integration points**: where this project connects to other systems
- **Deviations from plan**: what changed during construction and why (with session reference)
- **Production state**: deployment status, Docker containers, services, health checks

## 4. Adversarial Findings Summary

Sourced from adversarial loop reports (Code_Adversarial + Security_Adversarial + Design_Adversarial):

| Loop | Adversarial | Findings | Fixed | Deferred | Key insight |
|---|---|---|---|---|---|
| 1 | Code | N | M | K | Most impactful finding |
| 1 | Security | N | M | K | Most impactful finding |
| ... | ... | ... | ... | ... | ... |

## 5. Lessons — Technical (reusable)

Lessons that apply to ANY project, not just this one. Sourced from retrospectives + adversarial findings:

- **[Lesson title]**: what happened, what was learned, how to apply in future projects. Source: [session reference]. Status: [ENGINEERED into system / PENDING engineering].

## 6. Lessons — Process (reusable)

Lessons about how the team worked, not what was built. Sourced from retrospectives + orchestration logs:

- **[Lesson title]**: what happened, what was learned, how to apply in future workflows. Source: [session reference].

## 7. Pending Debt

Technical debt at project close. Sourced from debt_backlog.md files across all sessions:

| ID | Description | Priority | Reason deferred | Impact if not addressed | Session introduced |
|---|---|---|---|---|---|
| D1 | ... | HIGH/MEDIUM/LOW | ... | ... | YYYY-MM-DD |

## 8. Metrics

Quantitative data from the project lifecycle:

- Total sessions: N
- Total adversarial loops: N (across design + construction)
- Adversarial findings: N found, M fixed, K deferred
- Debt items: N introduced, M resolved, K remaining
- Key benchmark results (if applicable): [metric = value]

## 9. v2 Recommendations

What someone starting v2 should know. Ordered by priority:

1. **[Recommendation]**: why, what it enables, estimated effort. Source: [retrospective/adversarial finding that motivates this].
2. ...

---

## Traceability

- Design documents: [[design_doc_1]], [[design_doc_2]]
- Construction reports: [[construction_report_1]]
- Adversarial reports: [[adversarial_report_1]]
- Sessions: [[session_1]], [[session_2]], ...
- EcoDB memory IDs: [list]
- EcoDB graph origin: [project node]
- Previous synthesis (if v2+): [[previous_synthesis]]

---

## Verification

This document was verified by:
- **Verifier**: confirmed all sessions in collection appear in synthesis
- **Challenger**: confirmed completeness — v2 would have everything needed
- **Visual Adversarial**: confirmed document quality and readability
