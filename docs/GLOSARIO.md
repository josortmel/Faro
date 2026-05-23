---
use: Agent Lead Documentation
tags:
  - Documentacion_ECO_CONSULTING
  - Agente/lead
---
# Faro Glossary

Quick and precise reference for Faro (Sonnet) and any agent that needs to orient itself without reading all 11 workflows in full.

This document is normative: if a workflow says something different, the workflow wins on specifics. But role names and artifact names fixed here are non-negotiable.

> **Updated 2026-04-18 post-hardening**: the 6 workflows moved from v1 to v2/v3 with uniform methodology (governing principles, 4 literal gates, minimum schemas, literal prompts, contextual cross-validation, APPROVE_WITH_DEBT, Faro retrospective). Sections marked 🆕 are new or rewritten. Those marked ⚠️ correct obsolete v1 glossary information.
>
> **Updated 2026-04-19 (morning)**: created **workflow-investigation v1.0** (Hilo) applying the same hardened pattern. New role **Weaver** (Opus), new template `INVESTIGATION_REPORT_template.md`, hard rule WebFetch-first with shared serial Playwright queue.
>
> **Updated 2026-04-19 (afternoon)**: after productive debut and honest critique from the user, **bifurcation** into lightweight + deep. workflow-investigation v1.0 → renamed to `workflow-investigation-deep` v2.0. New `workflow-investigation` v2.0 lightweight (1 loop, Haiku Investigators, Sonnet Weaver) as default. Investigator moves to **contingency** in workflow-design. Weaver gains "Technical autonomy" section. Total: **8 workflows**, 15 roles, 11 artifacts, 16 templates.
>
> **Updated 2026-04-19 (afternoon-final)**: **cascade traceability formalized**. One Obsidian folder per workflow in `Laboratorio\I+D\<Folder>\` (Investigation, Design, Construction, Evolution, Integration, Adaptation). The 8 SKILLs gain "Input and output dependencies" section with explicit paths. Mandatory YAML frontmatter + "Traceability" section with wiki-links `[[]]` in every Obsidian report. `Scribe/CLAUDE.md` v2.0 with centralized destination table.
>
> **Updated 2026-04-27 (Hilo, reconciliation)**: major systemic change of 2026-04-26 led by Prima: migration of the 8 existing workflows to **v3/v4 relay** + creation of the **9th workflow `workflow-id`** (strategic). Total: **9 workflows**, **22 agents** (15 original + 4 Adversarials: Code/Design/Security/Audit + 3 Advisory Council: Pioneer/Guardian/Pragmatist). New mechanics: persistent relay peers via separate Claude Code instances + peer dispatch. Per-workflow and internal details live in the SKILLs — this glossary only acknowledges the change. If this document contradicts a SKILL on specifics, the SKILL wins.
>
> **Updated 2026-05-22 (Hilo, consolidation session)**: **Agent Teams → Relay** migration complete across all SKILLs and agent files. Added **Archivista (Archivist)** and **Adversarial_Gráfico (Visual_Adversarial)** → total **24 agents**. Added 2 new workflows: `workflow-consolidation` v1.0 and `workflow-project-synthesis` v1.0 → total **11 workflows**. Templates #20 (Project Synthesis) and #21 (Improvement Proposal) formalized. All agent CLAUDE.md files moved to `Agentes/<Role>/CLAUDE.md` subdirectory pattern. eco_memory + eco_graph unified into **EcoDB**.

---

## The 11 workflows — when to use each

Faro has three workflow families:

**"Do things in the system" family** (5 workflows — produce code/configuration):

| Workflow | When to activate | What it produces |
|---|---|---|
| **Design** | Before a critical execution: refactor touching schema, large external integration, non-obvious trade-offs. Also when the user expresses concern about complexity. | Brief + Spec + Plan ready for Construction |
| **Construction** | Create something new from scratch: MCP, script, system, agent, tool. For critical: Design first, then Construction with the Plan. | New working code + tests + Obsidian |
| **Evolution** | Improve existing code: refactor, optimization, cleanup, "second version of X". Starting point is always real code. | Modified code + verified non-regressions |
| **Integration** | Bring external technology into the system: install package, MCP, ComfyUI node, extension. "Not installed" or "needs configuring". | Technology installed and functional |
| **Adaptation** | Make something external understand the internal ecosystem: multi-agent Telegram, webhook that identifies active session, bidirectional connection with dynamic state. | Functional bridge + synchronized state |

**"Produce knowledge" family** (3 workflows):

| Workflow | When to activate | What it produces |
|---|---|---|
| **Newspaper** | Daily (morning cron) or on demand. Produce the user's personal newspaper with 6 fixed sections, explicit editorial criteria, reliability labeling, historical analysis. | Self-contained HTML + EcoDB memories + EcoDB triples |
| **Investigation** v3 (lightweight, DEFAULT) | Any "investigate how X", "what have others done with Y", "before touching Z I want to understand W". Default for reasonable research (1-3 focus areas, known domain, lightweight decision). 1 loop, Haiku Investigators, Sonnet Weaver. | Investigation Report with technical decisions MADE by the Weaver (technical autonomy) + only product questions. Destination: `Laboratorio\I+D\Investigación\` |
| **Investigation Deep** v3 | Complex topics: 4+ focus areas, very new technology (<2 years), major strategic decision. 2+ loops, Haiku Investigators, Opus Weaver. | Same Report but with greater density. |

**"Strategic" family** (1 workflow from 2026-04-26):

| Workflow | When to activate | What it produces |
|---|---|---|
| **I+D** v1.0 🆕 | Evaluate an existing system and propose its next level — "look at EcoDB v3 and tell me what's missing", "is there something better than ChromaDB for what we do?". 3 autonomous phases (Audit → Investigation → Vision). Does NOT execute other workflows — **feeds** them with well-formulated tasks. Each phase has a gate and independent deliverable. | Audit Report + Vision Proposal + task formulated for `workflow-design`. Destination: `Laboratorio\I+D\I+D\<system>.md` |

**"Synthesis" family** (2 workflows, new 2026-05-22):

| Workflow | When to activate | What it produces |
|---|---|---|
| **Consolidation** v1.0 🆕 | At the end of a major development phase or before a public release. Archaeology mode: reconstructs what was built, resolves documentation debt, generates Improvement Proposals (Template #21). Dual trigger: the user request OR post-phase condition. | Consolidated documentation + Improvement Proposals (Template #21) + debt_backlog updated |
| **Project Synthesis** v1.0 🆕 | After a project or major milestone is fully complete. Temporal reconstruction of the full journey. Cross-project mode when comparing multiple projects. | Project Synthesis document (Template #20) with lessons, architecture snapshot, and v2 recommendations |

### Quick decision tree

```
Is the task producing code/configuration, or producing knowledge?
│
├── KNOWLEDGE
│    ├── Daily or on-demand newspaper with 6 sections → NEWSPAPER
│    ├── Research on a topic with external sources → INVESTIGATION
│    │    ├── Complex topic? (≥4 focus areas OR very new tech OR strategic decision)
│    │    │    → INVESTIGATION DEEP (2 loops, Opus Weaver, Haiku Investigators)
│    │    └── Default case (1-3 focus areas, known domain, lightweight decision)
│    │         → INVESTIGATION lightweight (1 loop, Sonnet Weaver, Haiku Investigators)
│    ├── Evaluate system and propose next level → I+D
│    ├── Consolidate and document a phase → CONSOLIDATION
│    └── Synthesize a completed project → PROJECT SYNTHESIS
│
└── CODE / CONFIGURATION
     └── Is there currently working code I'm going to touch?
          ├── No → Is something coming from outside into the system?
          │        ├── Yes (install) → INTEGRATION
          │        └── No (create from scratch) → CONSTRUCTION
          │              (if critical: DESIGN first, then CONSTRUCTION)
          └── Yes → Is the goal to make something external understand the internal context?
                    ├── Yes (connect with state) → ADAPTATION
                    └── No (improve existing) → EVOLUTION
                          (if critical: DESIGN first, then EVOLUTION)

Note: INVESTIGATION doesn't produce code, but its report typically precedes DESIGN
or one of the execution workflows. The Weaver includes in each derived hypothesis
which workflow would be appropriate to materialize it.
```

---

## The 24 roles — what each does, when, and where it lives

> **Change 2026-04-26 (Prima)**: added 7 new roles to the ecosystem — 4 Adversarials (Code, Design, Security, Audit) and 3 from the I+D Advisory Council (Pioneer, Guardian, Pragmatist). The lower tables (code family + knowledge family) describe the 15 originals. The 7 new ones are documented in a separate table at the end of this section. **Exact detail of which workflow dispatches which new agent: see the corresponding workflow SKILL — operational source of truth**.
>
> **Change 2026-05-22**: added **Archivist** (consolidation + project-synthesis workflows) and **Visual_Adversarial** (adversarial for design/visual quality). Total: 24 agents.

## The 15 original roles

Roles are distinct. Neither "Designer" is "junior Architect", nor "Supervisor" is "renamed Designer", nor "Investigator" is "News Researcher", nor "Weaver" is "investigation Architect" — the informational universe in which they operate is radically different. Each role exists for a specific reason.

**Code/system family** (9 roles):

| Role | Where it acts | What it does | CLAUDE.md |
|---|---|---|---|
| **Architect** | workflow-design only | Produces Brief + Spec + Plan with formal traceability, adversarial loops | `Arquitecto/CLAUDE.md` |
| **Investigator** | workflow-design only | External technical research (official docs, papers, pro repos) | `Investigador/CLAUDE.md` |
| **Challenger** | workflow-design only (Loop 1) | Adversarial attack on the raw Brief | `Cuestionador/CLAUDE.md` |
| **ChallengerSpec** | workflow-design only (Loop 2) | Adversarial attack on Spec + Plan | `CuestionadorSpec/CLAUDE.md` |
| **Supervisor** | workflow-construction only | Coordinates task-by-task execution. Receives already-made Plan | `Supervisor/CLAUDE.md` |
| **Designer** | workflow-integration, evolution, adaptation | Produces lightweight JSON blueprint at the start of the workflow. Three contextual modes (generic/Auditor/Connector) | `Disenador/CLAUDE.md` |
| **Executor** | The 4 execution workflows | Implements the task per blueprint/Plan. Without improvising architecture | `Ejecutor/CLAUDE.md` |
| **Verifier** | The 4 execution workflows (standard and critical) | Blind reviewer: validates that it works in reality | `Verificador/CLAUDE.md` |
| **Scribe** | **All** workflows (always at the end) | Documents in Obsidian + EcoDB | `Escribano/CLAUDE.md` |

**Knowledge family — newspaper** (5 roles — workflow-newspaper):

| Role | Where it acts | What it does | CLAUDE.md |
|---|---|---|---|
| **News Researcher** | workflow-newspaper | Collects news by section from feeds/portals/media. Editorial universe, not academic. | `Investigador_de_Noticias/CLAUDE.md` |
| **Editor** | workflow-newspaper (always Opus) | Curates + cross-references + synthesizes preserving what's important. Applies the user's editorial criteria. | `Editor/CLAUDE.md` |
| **Source Critic** | workflow-newspaper | Labels source type (DIRECT/SECONDARY/...) + news reliability (not the outlet). Doesn't decide inclusion. | `Critico_de_Fuentes/CLAUDE.md` |
| **Analyst** | workflow-newspaper | Compares today's news with EcoDB history. Detects patterns: continuity, rupture, indirect relationship, silence. | `Analista/CLAUDE.md` |
| **Layout Designer** | workflow-newspaper | Self-contained HTML with inline CSS, reliability traffic lights, no external dependencies. | `Maquetador/CLAUDE.md` |

**Knowledge family — investigation** 🆕 (1 exclusive role + 3 reused — workflow-investigation):

| Role | Where it acts | What it does | CLAUDE.md |
|---|---|---|---|
| **Weaver** 🆕 | workflow-investigation only (always Opus) | Integrates reports from N parallel Investigators, detects cross-cutting connections between thematic focus areas, produces 8-section Investigation Report. **Does not research itself** — doesn't open URLs. Its craft is structural synthesis and strict separation of facts vs hypotheses. | `Tejedor/CLAUDE.md` |
| **Investigator** | (reused) | In both investigation workflows (lightweight and deep) works always with Haiku since 2026-04-21 (the user approval — cost + focus on collection/web navigation). Several in parallel by thematic focus areas. Mandatory protocol: WebFetch first, Playwright as fallback. | `Investigador/CLAUDE.md` |
| **Challenger** | (reused) | Attacks the Weaver's REPORT_v1 — detects gaps, contradictions, unsupported hypotheses, questionable sources. Produces the questions that Loop 2 must close. Sonnet. | `Cuestionador/CLAUDE.md` |
| **Scribe** | (reused) | Closes by archiving the definitive report in Obsidian (`Laboratorio\I+D\Investigación\`), EcoDB. | `Escribano/CLAUDE.md` |

### Critical distinction: Investigator vs News Researcher

They are not "the same role applied to different things". They are two roles with different universes:

- **Investigator** operates on papers, official docs, pro repos. Authority criterion: institutional/academic. Output format: `VERIFIABLE_FINDINGS`, `RECOMMENDED_PATTERNS`, technical `NEXT_ACTION`.
- **News Researcher** operates on media, feeds, portals, agencies. Authority criterion: editorial/journalistic (later evaluated by the Source Critic). Output format: normalized JSON items with `raw_indicators`, labeled by `target_section` and `region`.

Trying to merge them into a generic "Investigator" produces mediocre results in both domains.

### Critical distinction: Weaver vs Architect 🆕

Both are Opus, both are the "brain" of their workflow — but their craft is different:

- **Architect** (workflow-design) makes decisions and writes Brief/Spec/Plan. Has authority over the final product. Formal traceability `[research | user-brief | my-inference]`.
- **Weaver** (workflow-investigation) integrates findings without deciding. Doesn't take a position between mutually exclusive hypotheses — presents them with pros/cons. Its authority is exercised in the **cross-cutting connections** (patterns between focus areas) and in the **strict separation of verifiable sources vs hypotheses**.

Mental rule: if you see Opus "writing final decisions" → it's the Architect. If you see Opus "detecting patterns between Investigator reports and marking what's supported vs what's a hypothesis" → it's the Weaver.

### Roles that do NOT exist even if text might suggest them

- **"Designer-Auditor"** is not a separate role. It's the **Designer** in workflow-evolution (auditing existing code). The Designer's CLAUDE.md explains how to act in that mode.
- **"Designer-Connector"** is not a separate role either. It's the **Designer** in workflow-adaptation (mapping external↔internal).
- **"Plan Reviewer"** has no its own CLAUDE.md. It's a function performed by the **Challenger** (when coming from workflow-design) or **the Architect in checkpoint mode** (when it's step 0 of a critical execution workflow without prior design).

### Critical distinction: Supervisor vs Designer

They are not interchangeable. Workflows use them at different moments:

- **Supervisor** → workflow-construction. Receives a Plan that **already exists**. Doesn't plan, coordinates. Manages the Executor↔Verifier loop.
- **Designer** → workflow-integration/evolution/adaptation. Produces the **initial** blueprint of the workflow. Doesn't coordinate; Faro orchestrates directly after delivery.

If Faro launches the wrong workflow or confuses the roles → the workflow breaks. The Supervisor invoked from integration will report `WORKFLOW_MISMATCH`.

---

## The 9 new roles — Adversarials + Advisory Council + Synthesis (from 2026-04-26, updated 2026-05-22)

**Adversarials** (5 — replace/complement the classic Challenger in Prima's v3/v4 workflows):

| Role | Workflow where it acts | What it does | CLAUDE.md |
|---|---|---|---|
| **Design_Adversarial** | workflow-design v3 | Adversarial attack on architectural design — replaces the classic Loop 1 Challenger. Blind dual validation (alongside Prima/Architect). | `Adversarial_Diseno/CLAUDE.md` |
| **Code_Adversarial** | workflow-construction v4, workflow-evolution v3 | Adversarial attack on generated/modified code, seeks implementation edge cases. | `Adversarial_Codigo/CLAUDE.md` |
| **Security_Adversarial** | workflow-construction v4 (on components with external surface) | Adversarial attack focused on security — auth, input validation, credential leaks. | `Adversarial_Seguridad/CLAUDE.md` |
| **Audit_Adversarial** | workflow-id v1.0 (Phase 1 — Audit) | Second reading of the Audit Report — verifies completeness and dependencies against EcoDB. | `Adversarial_Auditoria/CLAUDE.md` |
| **Visual_Adversarial** 🆕 | workflow-consolidation, workflow-project-synthesis | Adversarial review of visual quality and design coherence in documents and reports. | `Adversarial_Grafico/CLAUDE.md` |

**I+D Advisory Council** (3 — exclusive to `workflow-id`, peer review of the Vision Proposal):

| Role | Function | CLAUDE.md |
|---|---|---|
| **Pioneer** (Sonnet) | Sees opportunities, advocates for the leap, signals the risk of NOT changing. Honest — if it's not worth it, says so. | `Pionero/CLAUDE.md` |
| **Guardian** (Sonnet) | Protects what works, proposes an incremental alternative, signals what's lost with the change. Accepts change when the data wins. | `Custodio/CLAUDE.md` |
| **Pragmatist** (Sonnet) | No emotion, calculates cost vs benefit, ROI, quantified risk. Doesn't care if it's new or old — cares if the numbers work out. | `Pragmatico/CLAUDE.md` |

**Council synthesis**: Prima (Lead) submits her vision draft to all three in parallel. Each reports their opinion. Prima synthesizes with **double vote** — if there's a 2-1, Prima breaks the tie. If it's 3-0 against Prima, she can maintain her position but must justify it explicitly to the user.

**Synthesis roles** (1, new 2026-05-22):

| Role | Workflow where it acts | What it does | CLAUDE.md |
|---|---|---|---|
| **Archivist** 🆕 | workflow-consolidation, workflow-project-synthesis | Reconstructs project archaeology from sessions, EcoDB memories, and git history. Feeds Weaver with structured historical context. | `Archivista/CLAUDE.md` |

**Relay mechanics (2026-05-22 update — replaces Agent Teams)**: persistent peers connect via separate Claude Code instances. Dispatch with dispatch task to <peer-name>. List active peers with discover available peer agents. Rename to known name with `relay_rename(new_name="...")`. Rooms for multi-team coordination: join coordination room. **No Agent() spawning — relay handles dispatch.**

---

## The artifacts — 13 distinct, not synonyms ⚠️🆕

Post-hardening v2/v3 + investigation and synthesis workflows there are 13 artifacts with formalized minimum schema (each has its template in `Faro/Plantillas/`).

### Code/system family

| Artifact | Who produces it | Where | What it contains | Format | Template |
|---|---|---|---|---|---|
| **Brief** | Architect | workflow-design Loop 1 | 6 mandatory sections: context, decisions with traceability, scope, verifiable success criteria, explicit debt, questions the Challenger should ask. 800-1500 words. | Markdown | `BRIEF_template.md` |
| **Spec** | Architect | workflow-design Loop 2 | 7 mandatory sections: Brief+verification citation, DDL, signatures with types, real examples, versioned dependencies, error handling, per-component success criteria. | Technical Markdown | `SPEC_template.md` |
| **Plan** | Architect (design) or Faro (standard construction) | workflow-design Loop 2 + workflow-construction | Tasks with 9 mandatory fields each: objective, files_to_touch, action, pre_conditions, post_conditions, tests, success_criterion, rollback, depends_on. | Technical Markdown | `PLAN_template.md` |
| **verification_checkpoint** | Architect | workflow-design Loop 2 (critical only) | 3 sections: real system state (commands), real counters, concrete findings the Spec must cite. | Markdown | `verification_checkpoint_template.md` |
| **Audit Report** 🆕 | Designer-Auditor | workflow-evolution | 6 sections: verified current state, detected problems, proposed changes, order, what NOT to touch, global success criteria. | Markdown | `AUDIT_REPORT_template.md` |
| **Install Blueprint** 🆕 | Generic Designer | workflow-integration | 6 sections: knowledge base query, dependencies, steps with functional verification, FUNCTIONAL criteria, warnings, rollback. | Markdown | `INSTALL_BLUEPRINT_template.md` |
| **Adaptation Map** 🆕 | Designer-Connector | workflow-adaptation | 7 sections: external reality, internal reality, internal↔external mapping, implementation plan, end-to-end criteria, maintenance triggers, full rollback. | Markdown | `ADAPTATION_MAP_template.md` |

### Knowledge family

| Artifact | Who produces it | Where | What it contains | Format | Template |
|---|---|---|---|---|---|
| **Pool** | News Researcher | workflow-newspaper | Collected items (60-100) with literal `source_summary` (not rewritten), `raw_indicators`, `target_section`, `region`. Raw material. | JSON | `NEWSPAPER_POOL_template.json` |
| **Edited newspaper (JSON)** | Editor + Source Critic + Analyst (composite) | workflow-newspaper intermediate | Pool curated with reliability labeled by Source Critic + historical analysis by Analyst. Layout Designer input. | JSON | `NEWSPAPER_EDITED_template.json` |
| **Final newspaper (HTML)** | Layout Designer | workflow-newspaper output | Self-contained HTML with 6 sections, reliability traffic lights, visual degradation for LOW/UNVERIFIABLE sources. | HTML | — (template in Layout Designer) |
| **Investigation Report** 🆕 | Weaver | workflow-investigation | 8 sections: metadata, question, investigated focus areas, findings per focus (2 categories: verifiable + relevant inaccessible), cross-cutting connections, derived hypotheses with suggested workflow, open questions, sources annex. Destination: Obsidian `Laboratorio\I+D\Investigación\`. | Markdown | `INVESTIGATION_REPORT_template.md` |

### Synthesis family (new 2026-05-22)

| Artifact | Who produces it | Where | What it contains | Format | Template |
|---|---|---|---|---|---|
| **Project Synthesis** 🆕 | Weaver + Archivist | workflow-project-synthesis | 7 sections: objective, key decisions (table), final architecture (actual vs planned), technical lessons, process lessons, pending debt, v2 recommendations. Full traceability. | Markdown | `Template_20_Project_Synthesis.md` |
| **Improvement Proposal** 🆕 | Weaver / any agent | workflow-consolidation + any workflow | 8 fields: PROPOSAL_ID, TYPE, SOURCE, PATTERN, PROPOSAL, EFFORT, PRIORITY, STATUS. Types: NEW_SKILL / NEW_TOOL / NEW_ANTI_PATTERN / ECODB_GAP. | Markdown | `Template_21_Improvement_Proposal.md` |

### Coordination artifacts (shared across workflows)

- `ENVIRONMENT.md` — preamble injected to all agents (OS, encoding, paths, services, credentials location).
- `CONTRACT.md` / `CONTRACT_design.md` — exact deliverables per agent.
- `LESSONS.md` — lessons accumulated in the session (Verifier does NOT read it — no bias).
- `orchestration.md` — append-only Faro log.
- `retrospective.md` 🆕 — 10-15 lines at the close of each workflow (v2/v3) with what worked, what Faro improvised, metrics, changes for v+1. In newspaper it's **aggregated**: weekly (`newspaper_retrospectives/week_<YYYY-WW>.md`) + monthly.
- `debt_backlog.md` 🆕 — registry of `debt_items` from `APPROVE_WITH_DEBT` verdicts.

**Golden rule code family**: Operational blueprints (Install/Audit/Adaptation Map) are intermediate between the extensive workflow-design Plan and a trivial installation — they have their own minimum schema, they are NOT "lightweight Plan".

---

## Complexity levels — quantifiable criteria

The 5 execution workflows use "trivial/standard/critical" but with slightly different thresholds. Here the normalized version for when Faro is unsure:

| Level | Quantifiable criteria (meet at least 2) |
|---|---|
| **trivial** | 1 file touched, ≤50 estimated lines, 0 new external dependencies, no DB schema, no side effects |
| **standard** | 2-5 files touched, 50-300 estimated lines, up to 1 new external dependency, no DB schema |
| **critical** | >5 files touched, >300 lines, DB schema affected, >1 new external dependency, OR integration with a system the designer has no verified experience with |

**Hard rule**: if the task is `critical` and does NOT come from workflow-design, Faro launches workflow-design first. Do not improvise design inside execution workflows.

---

## Report formats — convention ⚠️🆕

Two formats coexist. They don't mix.

| Format | When to use |
|---|---|
| **Strict JSON** | Internal reports from Designer/Auditor/Connector, Executor, Verifier in execution workflows when the report is short. Faro parses, doesn't read prose. |
| **Markdown-INI + dual JSON** | Reports from the Challenger (Loop 1), ChallengerSpec (Loop 2), and from the Verifier in **the 4 execution workflows v2/v3**. The Markdown-INI surface is for human review; the JSON for programmatic parsing. Same information in both. |

**Hard rule of verdict JSON coherence** (applicable to Verifiers and Challengers, updated v3):

| Condition | Mandatory verdict |
|---|---|
| `required_fixes: []` AND `debt_items: []` | `APPROVE` |
| `required_fixes: []` AND `debt_items` has ≥1 id | `APPROVE_WITH_DEBT` 🆕 |
| `required_fixes` has ≥1 id | `REQUEST_CHANGES` |
| Unrepairable defects with iteration | `REJECT` |
| `cross_ref_research_conflicts` with BLOCKER (Challenger) | `NEEDS_REDESIGN` automatic |
| `cross_ref_reality` with BLOCKER (ChallengerSpec) | `NEEDS_REDESIGN` automatic |

`debt_items` never coexists with `REQUEST_CHANGES` or `REJECT`: if something blocks, it goes in `blockers`.

---

## Human gates ⚠️🆕 — 4 per workflow (not 3 global)

**Important correction from the v1 glossary**: each v2/v3 workflow has **its own 4 gates**, with **literal** options (not A/B/C). There are no "3 global gates" — each workflow defines its own moments.

### The 4 canonical gates (in all v2/v3 workflows)

| # | Name | When it fires |
|---|---|---|
| **B0** | Load confirmation | At the start, before dispatching to the first agent. In workflow-newspaper cron can be skipped if pre-flight OK. |
| **B1** | Before destructive action or serious consequence | Real DB migrations, deleting files, creating persistent entities in external systems, service restarts, publishing degraded newspaper, etc. |
| **B2** | Proposal to modify Plan/Prompt/Spec/Blueprint/Map | After 3 failed iterations OR preventive detection of conflict with Spec/research/reality. In workflow-construction v3 also fires if Faro introduces a typo contradicting the Spec. |
| **B3** | Scope change during execution | the user requests expanding/modifying scope mid-workflow. Requires formalizing the change (not on the fly). |

### Golden rule of presentation

**Always literal options**, never A/B/C. Each option carries its full action described, even if redundant. This comes from the real incident: "C = abort" was understood as "C = continue" twice the same day.

### Signals that are NOT gates (system continues autonomous)

- `BLOCKING_QUESTIONS: []` from the Investigator → Architect proceeds without consulting.
- `required_fixes: []` from the Verifier → Supervisor closes without consulting.
- `verdict: APPROVE` from the Challenger → Architect proceeds without consulting.
- `DISAGREEMENT_WITH_PLAN` from the Executor → Supervisor investigates first (NOT an immediate gate).

---

## Anti-stuck: what to do when an agent freezes

This problem has already occurred twice in production with the Architect. The solution is on Faro's side, not the agent's (written rules aren't enough against the LLM's cognitive bias).

**Faro's protocol when it detects a frozen agent**:
- Symptom: the agent received a dense report (Investigator, Challenger, Verifier) and its next turn contains no APPLIED/DEFERRED/ESCALATED contract or processed decision.
- Action: Faro injects in the next prompt: *"YOU ARE STUCK. Process in one block NOW: 1) blockers first, 2) APPLIED_FIXES / DEFERRED_AS_DEBT / ESCALATED_TO_USER. Only escalate items that require the user's decision. There is no 'wait for more information' state before processing."*
- Applicable to: Architect (after Challenger/ChallengerSpec), Supervisor (after Verifier), Designer (after any Plan Reviewer report).

---

## File names — convention

- Agent CLAUDE.md files are in `$FARO_ROOT/Agentes/<Role>/CLAUDE.md` (e.g.: `Arquitecto/CLAUDE.md`).
- Workflow SKILL.md files are in `$FARO_ROOT/Skills/` and are named `SKILL_md_workflow_<name>.md`.
- This glossary is in the Faro documentation: `$FARO_ROOT/Documentacion/GLOSARIO.md`.
- **Templates** are in `$FARO_ROOT/Plantillas/`.
- Active and past sessions are in `$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>_<workflow>/`.
- 🆕 **Final reports (cascade traceability, 2026-04-19)** in `$VAULT/Laboratorio\I+D\<Folder>\<YYYY-MM-DD>_<slug>.md` with one folder per workflow: `Investigación\`, `Diseño\`, `Construcción\`, `Evolución\`, `Integración\`, `Adaptación\`. Each report has mandatory YAML frontmatter + mandatory "Traceability" section with wiki-links `[[]]`. Full schema in `Escribano/CLAUDE.md` v2.0.

---

## 🆕 Governing principles by workflow

Each v2/v3 workflow has 2-5 explicit governing principles. #1 is always "don't improvise". #2 is the contextual authority axis — what takes priority when something conflicts with the designing agent's plan.

| Workflow | Superior authority (governing principle 2) | Additional principles |
|---|---|---|
| construction v4 | **Spec > Faro** (Faro can introduce typos when assembling prompts) | — |
| design v2 | **Verified research > Architect** (Loop 1) / **verification_checkpoint > Architect** (Loop 2) | Challenger is not optional |
| evolution v2 | **Verified behavior > Auditor's proposal** — regressions are BLOCKER | Mandatory backup before modifying |
| integration v2 | **External system reality > Designer's assumptions** | "Installed without errors" is NOT verification |
| adaptation v2 | **DOUBLE reality** (external AND internal) > proposed mapping | Internal state can change during adaptation + credentials BEFORE starting |
| newspaper v2 | **Source Critic > Editor** on reliability | Historical > invented narrative + 3 sacred editorial criteria + Scribe is not optional |
| investigation v2 🆕 (lightweight) | **Verifiable sources > Weaver's inference** | 1 loop default + **Information ready for design, not technical disjunctives to the user (principle 5)** + **First-hand mandatory for verifiable URLs (principle 6, added afternoon-final 2026-04-19 after hyperdev-channels case)** + WebFetch first, Playwright fallback |
| investigation-deep v2 🆕 | **Verifiable sources > Weaver's inference** | 2 loops minimum + Loop 2 avoids Loop 1 sources + **First-hand mandatory (principle 5 deep — same content as 6 lightweight)** + **Opus Weaver for deep structural reasoning** |
| design v2.1 (refined) | **Verified research > Architect** (no change) | **Investigator is now CONTINGENCY** — prefer prior workflow-investigation report; if none and critical task, Faro aborts and launches workflow-investigation first |

---

## 🆕 Faro retrospective at close

Since v2/v3, all workflows close with a Faro retrospective written directly (no agent) in `Faro/Sessions/<session>/retrospective.md`:

- 10-15 lines: what worked, what Faro improvised, real metrics (iterations, gates, tokens), changes for v+1.
- **In workflow-newspaper** it's aggregated: weekly (`newspaper_retrospectives/week_<YYYY-WW>.md`) + monthly.

It's direct input for the next iteration of the corresponding SKILL.

---

## 🆕 Recurring registered lessons

### Double MCP config bug (April 18, 2026)
When an MCP migrates credentials from file to env var, update **BOTH** configs:
- `$HOME/AppData\Roaming\Claude\claude_desktop_config.json` (Claude Desktop → the user + Faro)
- `$HOME/.claude.json` (Claude Code CLI → Eco, Prima, CLIs)

If one is forgotten, the MCP works in some agents but not others. Happened twice the same day (Claude Desktop morning, Eco afternoon).

### A/B/C options in gates → guaranteed misinterpretation
Never use A/B/C or 1/2/3 labels in human gates. Always full literal text for each option.

### Faro can introduce typos in prompts
The Supervisor (construction) and any prompt dispatcher must do cross-validation against Spec/Research/Reality before dispatching to the execution agent. The Executor follows literally what it receives — if Faro is wrong, the Supervisor is the last line of defense.

### "Installed without errors" ≠ works
Verification is always functional, not declarative. `pip install X` without error doesn't mean X works.

### The Scribe is the most undervalued agent in the newspaper
Saving tokens on the Scribe is an anti-pattern. Each day not properly saved = a day the future Analyst is blind.

### 🆕 First-hand mandatory for verifiable URLs (2026-04-19 afternoon-final)

The **hyperdev-channels** case exposed a hole: Investigator I7 cited a URL they read mentioned in other content without visiting it themselves. It entered the report as verifiable. Manual verification the next day: 404. New governing principle (6 lightweight / 5 deep): `VERIFIABLE_SOURCES` **only** first-hand. Third-hand URLs → `RELEVANT_INACCESSIBLE_SOURCES` or `URLS_PENDING_PLAYWRIGHT`. The Challenger validates a random sample before APPROVE (new rule 6 in its CLAUDE.md).

### 🆕 WebFetch first, Playwright only if it fails (validated 2026-04-19)
Hard rule of workflow-investigation. Empirical validation:
- `WebFetch` works without issue on **public GitHub** (issues, PRs, repos without auth).
- `WebFetch` fails on **Reddit** (provider block — "Claude Code is unable to fetch from www.reddit.com").
- `Playwright` (`browser_navigate` + `browser_evaluate` with JS selectors) resolves Reddit by extracting real posts with title, permalink, score, and author.
- **Critical limitation**: Playwright has **1 shared tab**, not parallelizable between simultaneous sub-agents.

Resulting protocol: parallel Investigators (Haiku — approved 2026-04-21) **always attempt WebFetch first**. If it fails, they mark the URL as `PENDING_PLAYWRIGHT` and continue with WebFetch on the rest. Faro consolidates the pending URLs from all Investigators into a **serial queue** that processes them with Playwright one by one, redistributing the results to each Investigator before dispatching to the Weaver. This preserves WebFetch parallelism and serializes only when unavoidable.
