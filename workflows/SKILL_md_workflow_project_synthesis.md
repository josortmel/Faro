---
name: workflow-project-synthesis
description: |
  Orchestrated workflow for synthesizing a definitive truth document when a project v1 completes.
  Reconstructs the decision timeline, extracts reusable lessons, and archives a clean document
  suitable for EcoDB ingestion. Execute only when a project is declared complete by the human owner.
  The output is ONE document that tells v2 everything it needs to know.
metadata:
  version: "1.0"
  creation: 2026-05-22
  author: Hilo
  design_doc: "$FARO_ROOT/Informes/Diseño/2026-05-22_faro_consolidation_github_release.md"
tags:
  - agent/archivist
  - agent/weaver
  - agent/challenger
  - agent/visual_adversarial
  - agent/verifier
  - agent/scribe
  - workflow/project-synthesis
---

# Workflow: Project Synthesis (v1 — Relay)

Synthesizes a definitive truth document when a project v1 completes. The Scribe archives sessions. This workflow archives PROJECTS — one abstraction layer higher.

> **Governing principle 1 — Do not improvise**: reconstruct what actually happened, not what should have happened.
>
> **Governing principle 2 — Decision trail > post-hoc rationalization**: the synthesis must reflect real decisions with real dates and real rationale, not a cleaned-up narrative. If a bad decision was made, document it as such with what was learned.

---

## Trigger

**Single trigger**: human owner declares project v1 complete.

Not triggered by: session close, sprint end, or partial completion. Only full v1.

---

## The 4 gates (mandatory)

| Gate | When | What orchestrator presents |
|---|---|---|
| **B0** | After loading workflow | "Loaded workflow-project-synthesis v1. Project: [name]. Sessions: [date range]. Proceed?" |
| **B1** | After Phase 2 (timeline reconstructed) | "Weaver reconstructed decision timeline. [N] key decisions identified. Review accuracy before extraction?" |
| **B2** | After Phase 4 (synthesis document ready) | "Synthesis document complete. [Summary]. Approve before archival to EcoDB?" |
| **B3** | If scope changes | "Scope change: [what]. Adjust synthesis scope or continue?" |

**Always literal options at gates.** Never A/B/C.

---

## Agent composition (6 relay peers)

| Agent | Model | Role in this workflow |
|---|---|---|
| **Archivist** (mode 3: collection) | Haiku | Collects all project sessions chronologically |
| **Weaver** (temporal reconstruction variant) | Opus | Reconstructs decision timeline, extracts lessons, synthesizes |
| **Challenger** | Sonnet | Attacks completeness — would v2 have everything needed? |
| **Visual Adversarial** | Sonnet | Attacks document quality and readability |
| **Verifier** | Sonnet | Verifies synthesis covers all sessions (NON-SKIPPABLE) |
| **Scribe** | Sonnet | Archives to EcoDB + vault + graph |

---

## Phases

### Phase 1 — Collection
**Owner**: Archivist (mode 3: collection, Haiku)

Dispatch via dispatch task to Archivista.

Archivist gathers ALL project documentation from these sources:

**Session artifacts** (from `$FARO_ROOT/Sesiones/`):
- `orchestration.md` — decision logs with timestamps
- `retrospective.md` — session reflections, what worked/didn't
- `debt_backlog.md` — technical debt accumulated and resolved

**Workflow reports** (from `$FARO_ROOT/Informes/`):
- `Diseño/` — design documents (Brief, Spec, Plan) produced by workflow-design
- `Construcción/` — construction reports with task completion, adversarial findings, production readiness
- `Investigacion/` — research reports that informed design decisions
- `Evolución/` — evolution/refactor reports if the project was modified post-v1

**Adversarial records** (from `$FARO_ROOT/Agentes/Adversarial_*/Reports/`):
- Adversarial loop reports from design and construction phases

**EcoDB**:
- Memories related to the project: search shared memory
- Graph triples: explore graph connections
- Handoff memories: search shared memory

Delivers: chronological timeline of sessions + ALL project documents + key decisions + gaps.

**Critical**: if a design doc, construction report, or adversarial report exists for the project, it MUST be in the collection. Session logs alone are not enough — the formal artifacts are the source of truth.

### Phase 2 — Reconstruction
**Owner**: Weaver (temporal reconstruction variant, Opus)

Dispatch via dispatch task to Tejedor.

Weaver reconstructs:
- **Decision timeline**: what was decided, when, by whom, why, what alternatives were discarded
- **Pivot points**: where the project changed direction and what triggered it
- **Failures**: what didn't work and what was learned
- **Evolution**: how the design/architecture changed from initial plan to final state

This is **causal narrative, not thematic synthesis**. Different craft from investigation workflows.

Present at **Gate B1**.

### Phase 2.5 — Cross-project extraction (conditional)
**Owner**: Weaver (same session)

**Conditional**: skip if this is the first project in EcoDB.

If other project synthesis docs exist: search shared memory.
Check for overlap — don't duplicate lessons already captured in another project's synthesis.

### Phase 3 — Extraction
**Owner**: Weaver (same session)

Separate findings into three buckets:
- **Reusable technical lessons**: apply to ANY project (technology choices, architecture patterns, performance insights)
- **Reusable process lessons**: apply to ANY workflow (team dynamics, adversarial patterns, estimation accuracy)
- **Project-specific context**: applies ONLY to this project (specific design decisions, domain knowledge, stakeholder context)

### Phase 4 — Synthesis
**Owner**: Weaver (same session)

Produce the synthesis document using **Template #20** (PROJECT_SYNTHESIS_template.md):

1. Objective — what the project set out to do
2. Key Decisions — chronological table (date, decision, rationale, alternatives, source)
3. Final Architecture — what was actually built (not planned)
4. Lessons — Technical (reusable)
5. Lessons — Process (reusable)
6. Pending Debt — what was left undone
7. v2 Recommendations — what v2 should know

Target: 3000-6000 words. Dense, not padded.

Present at **Gate B2**.

### Phase 5 — Validation (NON-SKIPPABLE)
**Owner**: Challenger + Visual Adversarial (parallel, Sonnet)

Dispatch both:
- dispatch task to Cuestionador
- dispatch task to Adversarial_Grafico

Challenger attacks completeness:
- Would someone starting v2 have everything they need?
- Are there decisions documented without rationale?
- Are lessons actually reusable or project-specific mislabeled?
- Is pending debt honest or minimized?

Visual Adversarial attacks:
- Document structure and readability
- Table formatting and consistency
- Traceability section completeness

Dispatch Verifier (NON-SKIPPABLE):
- dispatch task to Verificador

Verifier confirms:
- Every session in the collection appears in the synthesis
- No session was silently dropped
- Key decisions from orchestration logs are reflected
- Lessons are correctly categorized (technical vs process vs project-specific)

### Phase 6 — Archive
**Owner**: Scribe (Sonnet)

Dispatch via dispatch task to Escribano.

Scribe archives:
- Synthesis document → `$FARO_ROOT/Informes/Synthesis/<YYYY-MM-DD>_<project>_synthesis.md`
- Summary memory → EcoDB (`type="tecnico"`, `tags=["project-synthesis", "<project-slug>"]`)
- Decision triples → EcoDB graph (key decisions as subject-predicate-object)
- Cross-references → wiki-links to all session folders

### Phase 7 — Retrospective
**Owner**: Orchestrator

Write `retrospective.md`:
- What worked in the synthesis process
- What was hard to reconstruct (missing docs, gaps in orchestration logs)
- Recommendations for future session documentation to make synthesis easier

Save to EcoDB.

---

## Dependencies

### Input
- Project name + declaration of v1 complete (from human owner)
- All session folders for the project
- EcoDB memories + graph triples related to the project

### Output
- Project Synthesis document (Template #20)
- EcoDB memories (summary + decision triples)
- Retrospective

### Next workflow
- If synthesis reveals unfinished critical work → back to human owner for v2 decision
- If synthesis reveals process improvements → workflow-consolidation or improvement proposal (Template #21)

---

## Difference from Scribe

The Scribe archives **sessions** — what happened in one sitting.
This workflow archives **projects** — the full story across many sessions.

The Scribe runs at every session close.
This workflow runs once per project v1 completion.

The Scribe captures facts.
This workflow reconstructs narrative, extracts lessons, and produces recommendations.
