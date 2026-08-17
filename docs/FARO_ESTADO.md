---
use: Documentation Agents Leads
tags:
  - proyecto/eco_consulting
  - agent/lead
  - estado/completado
---
# FARO — Complete System State

> **Purpose**: single entry point for any new Opus (or Sonnet, or future model) instance sitting down to work with Faro without prior context. Reading this in order enables operation without reconstructing the methodology from the SKILLs.
>
> Complements `GLOSARIO.md` (quick nomenclature reference). This document is the operational manifesto.
>
> **Last update**: 2026-07-14 (Eco, faro_lint integration + inventory reconciliation: 13 workflows, 28 active agents, deterministic validators). Previous: 2026-05-22 (Hilo, system consolidation for GitHub release). Full rewrite from Spanish to English. Reconciled against 33 sessions of real usage (2026-04-18 to 2026-05-22). Key changes: Agent Teams → Relay as canonical orchestration, 22 → 24 agents, 9 → 11 workflows, EcoDB unified memory, three adversarial layers formalized, enforcement mechanisms added, Orchestrator Preamble introduced. Design doc: `$FARO_ROOT/Informes/Diseño/2026-05-22_faro_consolidation_github_release.md`.
>
> **Relationship to SKILLs**: this document is an orientational map. The operational source of truth for each workflow is the SKILL file in `Faro/Skills/`. If this document contradicts a SKILL, **the SKILL wins**.
>
> **How to use**:
> 1. Read §1 (Executive summary) to orient in 2 minutes.
> 2. Read §10 (Quickstart for new instance) if starting a session without prior memory.
> 3. Use §2-9 as reference when consulting something specific.

---

## 1. Executive summary (2 minutes)

**Faro** is a multi-agent orchestration system for Claude Code CLI. An Opus orchestrator coordinates specialized agents (Sonnet/Haiku) via **inter-session messaging system** (inter-session messaging, separate sessions) and produces formal artifacts at each stage.

Faro **orchestrates 13 workflows**:

1. **workflow-design** — produces Brief + Spec + Plan before building. Investigator is contingency.
2. **workflow-construction** — builds from scratch. Supervisor as Opus department lead; Verifier as beta tester.
3. **workflow-evolution** — refactors existing code/systems.
4. **workflow-integration** — installs external technology.
5. **workflow-adaptation** — connects external tools to the internal ecosystem (config vs code bifurcation).
6. **workflow-newspaper** — produces daily personal HTML newspaper.
7. **workflow-investigation** (lightweight, default) — 1 loop, Haiku Investigators, Sonnet Weaver.
8. **workflow-investigation-deep** — 2+ loops, Haiku Investigators, Opus Weaver.
9. **workflow-rd** — strategic R&D evaluation. Audits existing system, proposes investigation focuses, synthesizes vision via Advisory Council (Pioneer/Guardian/Pragmatist). Does not execute — feeds workflow-design.
10. **workflow-consolidation** 🆕 — periodic system audit against real usage. Dual trigger: every N=15 sessions or event-driven (release, pivot). Mines session artifacts, classifies divergences, updates core docs.
11. **workflow-project-synthesis** 🆕 — synthesizes definitive truth document when a project v1 completes. Reconstructs decision timeline, extracts reusable lessons, archives to EcoDB.
12. **workflow-deep-design** — multi-model deep design. Iterative refinement with external counsellors (Design_Counsellor instances on different models) plus independent adversarials, minimum 3 full rounds before approval. For high-stakes designs where single-model blind spots are unacceptable.
13. **workflow-frontend** — builds frontend interfaces and dashboards. Design authority (Lienzo) reviews visual quality and brand compliance at every stage; Frontend_Builder implements from closed briefs; visual adversarial reviews against DESIGN.md.

**Orchestration pattern — Relay**: agents run as **separate Claude Code sessions** coordinated via inter-session messaging system (peer dispatch, peer reply, peer discovery). Each agent session has its own context window, CLAUDE.md, and tools. The orchestrator dispatches tasks via peer dispatch (max 2 tasks per ask), receives structured reports, and makes routing decisions.

**Memory system — EcoDB**: shared memory infrastructure (PostgreSQL + pgvector + Apache AGE). 22 MCP tools for semantic search, memory persistence, knowledge graph traversal, entity extraction, and document ingestion. All agents share one EcoDB instance.

Faro **does not execute code directly** — it coordinates **28 specialized agents** and exchanges formal artifacts. An **Orchestrator Preamble** (shared CLAUDE.md fragment) encodes the operational protocol that any orchestrator role must follow: logging, memory integration, coordination rules, enforcement mechanisms, and escalation protocol.

**Fundamental operating principle**: Faro and sub-agents **do not infer well**. Every step, prompt, path, and format must be explicit. The methodology in the SKILLs is designed so a new model can follow it without inventing. **If this section contradicts a SKILL, the SKILL wins**.

---

## 2. Complete inventory — what's on disk

### 2.1 Directory structure

```
$FARO_ROOT/                          # Obsidian vault: $VAULT/
├── Documentacion/
│   ├── FARO_ESTADO.md                         # This document
│   ├── GLOSARIO.md                            # Nomenclature quick reference
│   ├── ORCHESTRATOR_PREAMBLE.md               # Shared protocol fragment for orchestrator roles
│   └── ... (12 reference docs total)
├── Skills/                                    # 13 operational SKILLs (Relay pattern)
│   ├── SKILL_md_workflow_diseno.md
│   ├── SKILL_md_workflow_construccion.md
│   ├── SKILL_md_workflow_evolucion.md
│   ├── SKILL_md_workflow_integracion.md
│   ├── SKILL_md_workflow_adaptacion.md
│   ├── SKILL_md_workflow_periodico.md
│   ├── SKILL_md_workflow_investigacion.md
│   ├── SKILL_md_workflow_investigacion_profunda.md
│   ├── SKILL_md_workflow_id.md
│   ├── SKILL_md_workflow_consolidation.md      # 🆕 periodic system audit
│   ├── SKILL_md_workflow_project_synthesis.md  # 🆕 definitive project truth document
│   ├── SKILL_md_workflow_diseno_profundo.md    # multi-model deep design (counsellors)
│   └── SKILL_md_workflow_frontend.md           # frontend construction (Lienzo authority)
├── Agentes/                                   # 28 active agents + 3 archived (subdirectory per agent)
│   ├── Architect/
│   │   ├── CLAUDE.md                          # Agent identity + role definition
│   │   └── .claude/settings.local.json        # Agent-specific settings
│   ├── Investigator/
│   ├── Challenger/
│   ├── ChallengerSpec/
│   ├── Supervisor/
│   ├── Executor/
│   ├── Verifier/
│   ├── Scribe/
│   ├── Designer/                              # 3 modes: generic/auditor/connector
│   ├── Editor/
│   ├── Source_Critic/
│   ├── Analyst/
│   ├── Layout_Designer/
│   ├── News_Researcher/
│   ├── Weaver/                                # Sonnet (lightweight) / Opus (deep)
│   ├── Code_Adversarial/
│   ├── Design_Adversarial/
│   ├── Security_Adversarial/
│   ├── Audit_Adversarial/
│   ├── Visual_Adversarial/                    # Visual quality (Layer 3)
│   ├── Pioneer/                               # Advisory Council (innovation)
│   ├── Guardian/                              # Advisory Council (stability)
│   ├── Pragmatist/                            # Advisory Council (cost/benefit)
│   ├── Archivist/                             # Pre/post-flight + collection mode
│   ├── Design_Counsellor/                     # Deep-design external peer (any model: Opus/DeepSeek/ChatGPT)
│   ├── Frontend_Builder/                      # workflow-frontend builder (closed briefs from Lienzo)
│   ├── OSINTSpy/                              # Personal OSINT (standalone, direct with the user — not workflow)
│   ├── Vision_keeper/                         # Guardian of user's product vision (manual invocation via relay)
│   ├── Data_Analyst/                          # ⚠️ ARCHIVED — consulting-specific
│   ├── Scraper/                               # ⚠️ ABSORBED — capability transferred to Investigator
│   └── Synthesizer/                           # ⚠️ ARCHIVED — consulting-specific
├── Plantillas/                                # 22 artifact templates (4 JSON templates have dual extension: .json for data, .json.md for Obsidian rendering)
│   ├── BRIEF_template.md
│   ├── SPEC_template.md
│   ├── PLAN_template.md
│   ├── verification_checkpoint_template.md
│   ├── AUDIT_REPORT_template.md
│   ├── INSTALL_BLUEPRINT_template.md
│   ├── ADAPTATION_MAP_template.md
│   ├── ECOSYSTEM_template.md
│   ├── CONTRACT_template.md
│   ├── CONTRACT_diseno_template.md
│   ├── ENVIRONMENT_template.md
│   ├── LESSONS_template.md
│   ├── PERIODICO_POOL_template.json
│   ├── PERIODICO_EDITADO_template.json
│   ├── CRITERIOS_EDITORIALES_template.md
│   ├── INFORME_INVESTIGACION_template.md
│   ├── TRANSCRIPCION_YOUTUBE_template.md
│   ├── PERIODICO_POOL_template.json.md
│   ├── PERIODICO_EDITADO_template.json.md
│   ├── PROJECT_SYNTHESIS_template.md          # 🆕 Template #20
│   ├── IMPROVEMENT_PROPOSAL_template.md       # 🆕 Template #21
│   └── agente_template/                       # Agent bootstrap scaffold
├── Sesiones/                                  # One folder per session (append-only)
│   └── <YYYY-MM-DD>_<project>_<workflow>/
│       ├── ENVIRONMENT.md
│       ├── CONTRACT.md
│       ├── LESSONS.md
│       ├── orchestration.md
│       ├── retrospective.md
│       ├── debt_backlog.md
│       └── reportes_investigadores/           # (investigation workflows)
├── Informes/                                  # Workflow output reports (cascading traceability)
│   ├── Construcción/
│   ├── Diseño/
│   ├── Evolución/
│   ├── Investigacion/
│   ├── Integración/
│   ├── Adaptación/
│   └── Ciberseguridad/
└── runs/                                      # (historical)
```

### 2.2 Propagation to Claude Code

SKILLs are synced to Claude Code's skill directories:
```
~/.claude/skills/<workflow>/SKILL.md
```
One per workflow. When a SKILL is modified in `Faro/Skills/`, it **must be manually copied** to `.claude/skills/<workflow>/SKILL.md for Claude Code to see it:
```bash
cp "$FARO_ROOT/Skills/SKILL_md_workflow_<X>.md" \
   "$HOME/.claude/skills/<workflow>/SKILL.md
```

Some agents also have `.claude/skills/<workflow>/SKILL.md subdirectories with operational skills (systematic-debugging, TDD, owasp-security). These are internal tools, not part of the Faro methodology.

---

## 3. The 28 agents — who does what, when, and where

### 3.1 Core system agents (9)

| Agent | Workflows | Role |
|---|---|---|
| **Architect** | design | Produces Brief + Spec + Plan with traceability (research/user-brief/my-inference). Always Opus. |
| **Investigator** | design (contingency), investigation, investigation-deep, consolidation | External technical research (official docs, papers, repos). 4 modes: design, investigation, investigation-deep, **archaeology** (mines internal sessions, Haiku). Protocol: WebFetch first, Playwright fallback. |
| **Challenger** | design (Loop 1), investigation, consolidation | Adversarial attack on Brief. Cross-validation against research. |
| **ChallengerSpec** | design (Loop 2) | Adversarial attack on Spec + Plan. Cross-validation against verification_checkpoint. |
| **Supervisor** | construction | Coordinates task-by-task execution. Receives completed Plan. Cross-validates Prompt↔Spec. |
| **Designer** | integration, evolution, adaptation | Produces initial blueprint. Three contextual modes: generic (integration), Auditor (evolution), Connector (adaptation). |
| **Executor** | construction, evolution, integration, adaptation | Implements task by task. No architectural improvisation. |
| **Verifier** | all execution workflows | Blind reviewer: validates that things work in reality, not declaratively. Emits APPROVE_WITH_DEBT. **Non-skippable** in every execution SKILL. |
| **Scribe** | **all** workflows (closing phase) | Documents to Obsidian vault + EcoDB + knowledge graph. |

### 3.2 Knowledge agents — newspaper (5, workflow-newspaper)

| Agent | Role |
|---|---|
| **News Researcher** | Collects news by section. Raw pool without editorializing. Does NOT rewrite `source_summary` (must be literal). |
| **Editor** | Always Opus. Curates + cross-references + synthesizes. Applies the user's 3 sacred criteria (≥3 regions, ≥1 outside mainstream, each item with verifiable source). |
| **Source Critic** | Tags `source_type` (DIRECT/SECONDARY/TERTIARY) + `reliability` (HIGH/MEDIUM/LOW/UNVERIFIABLE) per item. |
| **Analyst** | Compares news against EcoDB historical data. Detects patterns (continuity/rupture/indirect relation/silence). Does NOT invent narrative without evidence. |
| **Layout Designer** | Self-contained HTML with reliability traffic lights. Visually degrades LOW/UNVERIFIABLE reliability items. |

### 3.3 Knowledge agents — investigation (4, workflow-investigation + investigation-deep)

| Agent | Role |
|---|---|
| **Weaver** | Sonnet (lightweight) / Opus (deep). Integrates reports from N parallel Investigators, detects cross-theme connections, produces Investigation Report (8 sections). **Does not investigate** — synthesis is the craft, not URL opening. Hard rule: no citable source → HYPOTHESIS, not fact. **Enforcement: yields after 1 rebuttal with contradictory data.** New variant: **temporal reconstruction** for workflow-project-synthesis (causal timeline instead of thematic synthesis). |
| **Investigator** *(reused)* | Always Haiku (validated 2026-04-21), multiple in parallel (one per focus). Mandatory protocol: WebFetch first, Playwright fallback. Reports consumed sources so Loop 2 avoids them. |
| **Challenger** *(reused)* | Attacks Weaver's REPORT_v1 — detects gaps, unsupported hypotheses, questionable sources. Produces concrete questions for Loop 2 to close. |
| **Scribe** *(reused)* | Closing. Archives definitive report + EcoDB + knowledge graph. |

### 3.4 Knowledge agents — consolidation + project synthesis (1 agent + referenced modes)

| Agent | Role |
|---|---|
| **Archivist** | Pre-flight (knowledge verification) + Post-flight (archival verification). 3 modes: pre-flight, post-flight, **collection** (gathers all project sessions chronologically for workflow-project-synthesis). Debut: this consolidation session (2026-05-22). |

These workflows also use **Investigator mode 4 "archaeology"** (see §3.1) — mines internal session artifacts for divergences, recurring failures, undocumented lessons, emergent practices. Output schema: FINDING_ID, TYPE, SEVERITY, SOURCE, DESCRIPTION, EVIDENCE, RECOMMENDATION. And **Weaver "temporal reconstruction" variant** (see §3.3) — reconstructs decision timelines for project synthesis.

### 3.5 Advisory Council — R&D (3, workflow-rd)

| Agent | Role |
|---|---|
| **Pioneer** | Advises innovation + technology leap. Pushes toward new approaches. |
| **Guardian** | Advises improving existing before building new. Protects stability. |
| **Pragmatist** | Cost/benefit evaluator. Neutral tie-breaker. |

### 3.6 Three adversarial layers (7 agents)

Every workflow with deliverables passes through at least one adversarial layer. The layers are cumulative — a design workflow passes through Layer 1; a construction workflow passes through Layers 1 + 2; a workflow with visual deliverables adds Layer 3.

**Layer 1 — Conceptual (4 agents)**: attacks premises, trade-offs, completeness, process compliance.

| Agent | Scope |
|---|---|
| **Challenger** | Brief attack in design (Loop 1), investigation, and consolidation workflows |
| **ChallengerSpec** | Spec + Plan attack in design workflows |
| **Design Adversarial** | Plan/architecture attack in design workflows |
| **Audit Adversarial** | Audit report attack in workflow-rd |

*(Design doc §6 listed 2 agents for Layer 1; FARO_ESTADO reflects full 4-agent operational reality — approved evolution, 2026-05-22.)*

**Layer 2 — Technical (2 agents)**: attacks code quality, security, performance.

| Agent | Scope |
|---|---|
| **Code Adversarial** | Code errors, quality, usability. Reviews implementation. |
| **Security Adversarial** | Security audit, OWASP coverage, threat modeling. |

**Layer 3 — Visual (1 agent)**: attacks design quality, brand consistency, readability.

| Agent | Scope |
|---|---|
| **Visual Adversarial** | Visual/design quality of README, docs, diagrams, deliverables. |

### 3.7 Archived agents (3)

These agents were used in a single consulting session (market research PyMEs, 2026-04-21) and are not part of core Faro. Their directories remain in `Agentes/` with an archive note. Resurrect if needed for future consulting workflows.

- **Analista_Datos** — market research signal detection
- **Scraper** — systematic web data extraction
- **Sintetizador** — transforms analysis into business opportunities

### 3.8 Roles that DO NOT exist (recurring correction)

- "Designer-Auditor" = Designer in Auditor mode (workflow-evolution). Not a separate CLAUDE.md.
- "Designer-Connector" = Designer in Connector mode (workflow-adaptation).
- "Plan Reviewer" = function performed by Challenger or Architect at checkpoint. Not a role.
- "Newspaper Analyst" vs "Analyst" = same agent, same CLAUDE.md.
- "Investigation Architect" = does NOT exist; it's the **Weaver** (different agent, different craft: integrates, doesn't decide).
- "Synthesizer" / "Integrator" = names considered and rejected; the canonical role is **Weaver**.

### 3.9 Agents added post-consolidation (2026-05-30 — 2026-06-29)

| Agent | Workflows | Role |
|---|---|---|
| **Design_Counsellor** | deep-design | External peer that improves Brief and Spec+Plan across iterative rounds. Runs on any model (Opus, DeepSeek, ChatGPT) — several instances on different models per round. Strengthens, does not attack. |
| **Frontend_Builder** | frontend | Builds UI screens from closed briefs by Lienzo. Sonnet/DeepSeek. No aesthetic or architectural improvisation. |
| **Vision_keeper** | any (manual) | Guardian of the user's product vision — barrier between the user and workflow output. Invoked manually by the user via relay. Opus. |
| **OSINTSpy** | none (standalone) | Personal OSINT: own-privacy audit and contact verification. Direct terminal with the user, not part of workflow orchestration. |

### 3.10 Agent loading rule

Before dispatching any agent, the orchestrator **reads the corresponding CLAUDE.md and injects its content LITERALLY** at the start of the prompt. No paraphrasing, no summarizing. This guarantees complete role identity regardless of which model executes.

For orchestrator roles: the CLAUDE.md includes a reference to `ORCHESTRATOR_PREAMBLE.md`, which the orchestrator reads and applies before any action. Sub-agents do not receive the Preamble.

### 3.11 Skill loading at session start

Agents have **custom skills** installed in their `.claude/skills/<workflow>/SKILL.md directories. These skills should be loaded at the start of each session to enhance agent capabilities. Key patterns:

- **All execution agents** (Executor, Verifier, adversarials): load `superpowers` framework at session start for structured task approach, systematic debugging, and verification discipline.
- **All agents during workflows**: load `caveman ultra` mode for token savings (~75% reduction in prose).
- **Agent-specific skills**: some agents have specialized skills (e.g., Executor has TDD + systematic-debugging, Security_Adversarial has OWASP security). These load automatically from their `.claude/skills/<workflow>/SKILL.md directory.

Custom skills per agent are a key lever for Faro's future improvement. Each agent's CLAUDE.md should indicate which skills to load at session start.

---

## 4. The 22 formalized artifacts

All artifacts have a template in `Faro\Plantillas\` with a mandatory minimum schema. Challenger/Verifier/Scribe reject artifacts that don't comply with the schema.

### 4.1 Code/system family

| Artifact | Mandatory sections | Template | Format |
|---|---|---|---|
| **Brief** | 6: context, decisions with traceability, scope, criteria, debt, questions for Challenger | `BRIEF_template.md` | Markdown |
| **Spec** | 7: cites Brief+verif, DDL, signatures, real examples, deps with versions, errors, criteria | `SPEC_template.md` | Technical Markdown |
| **Plan** | Tasks with 9 fields: objective, files_to_touch, action, pre_conditions, post_conditions, tests, success_criteria, rollback, depends_on | `PLAN_template.md` | Technical Markdown |
| **verification_checkpoint** | 3: real system state, real counters, findings Spec must cite | `verification_checkpoint_template.md` | Markdown |
| **Audit Report** | 6: verified current state, issues, proposed changes, order, what NOT to touch, success criteria | `AUDIT_REPORT_template.md` | Markdown |
| **Install Blueprint** | 6: knowledge base, deps, steps with FUNCTIONAL verification, functional criteria, warnings, rollback | `INSTALL_BLUEPRINT_template.md` | Markdown |
| **Adaptation Map** | 7: external reality, internal reality, mapping, plan, E2E criteria, maintenance triggers, rollback | `ADAPTATION_MAP_template.md` | Markdown |
| **Project Synthesis** | 7: objective, key decisions, final architecture, lessons — tech (reusable), lessons — process (reusable), pending debt, v2 recommendations | `PROJECT_SYNTHESIS_template.md` | Markdown |
| **Improvement Proposal** | 8: proposal_id, type, source, pattern, proposal, effort, priority, status | `IMPROVEMENT_PROPOSAL_template.md` | Markdown |

### 4.2 Knowledge family

| Artifact | Content | Template | Format |
|---|---|---|---|
| **Pool** | 60-100 items with literal `resumen_fuente`, `seccion_objetivo`, `region`, `indicadores_brutos` | `PERIODICO_POOL_template.json` | JSON |
| **Edited newspaper (JSON)** | Curated pool + Critic reliability rating + Analyst analysis | `PERIODICO_EDITADO_template.json` | JSON |
| **Final newspaper (HTML)** | Self-contained HTML with 6 sections + traffic lights | (template in Layout Designer) | HTML |
| **Research Report** 🆕 | 8 sections: metadata, question, focuses, findings per focus (verifiable + relevant inaccessible), cross-connections, derived hypotheses with suggested workflow, open questions, sources annex | `INFORME_INVESTIGACION_template.md` | Markdown |

### 4.3 Coordination artifacts (shared)

- `ENVIRONMENT.md` — OS/encoding/paths/services preamble
- `CONTRACT.md` / `CONTRACT_diseno.md` — deliverables per agent
- `LESSONS.md` — append-only, Verifier does NOT read it (no bias)
- `orchestration.md` — Faro log
- `retrospective.md` — 10-15 lines at session close (v2/v3)
- `debt_backlog.md` — debt_items from APPROVE_WITH_DEBT verdicts

---

## 5. Governing principles per workflow

Every workflow has 2-5 explicit governing principles. **#1 is always "do not improvise"**. **#2 is the contextual authority axis** — what overrides what when they conflict.

| Workflow | Authority (#2) | Additional principles |
|---|---|---|
| **construction** | **Spec > Orchestrator** — if orchestrator introduces typo contradicting Spec, Spec wins | — |
| **design** | **Verified research > Architect** (Loop 1) / **verification_checkpoint > Architect** (Loop 2) | Challenger is not optional |
| **evolution** | **Verified behavior > Auditor's proposal** — regressions are BLOCKER | Mandatory backup before modifying |
| **integration** | **External system reality > Designer's assumptions** | "Installed without errors" is NOT verification |
| **adaptation** | **DUAL reality** (external AND internal) > proposed mapping | Internal state may change + credentials BEFORE starting |
| **newspaper** | **Source Critic > Editor** on reliability | Historical data > invented narrative + 3 sacred criteria + Scribe is not optional |
| **investigation** (lightweight) | **Verifiable sources > Weaver's inference** | 1 loop default + information ready for design (no open technical questions to user) + `VERIFIABLE_FINDINGS` from first-hand only + WebFetch first, Playwright fallback |
| **investigation-deep** | **Verifiable sources > Weaver's inference** | 2+ loops + Loop 2 avoids Loop 1 sources + first-hand mandatory for verifiable URLs + Opus Weaver for deep structural reasoning |
| **rd** | **Audit data > Advisory Council opinion** | Council advises, does not decide. Human owner decides. |
| **consolidation** 🆕 | **Session artifacts > orchestrator memory** — what the logs say overrides what the orchestrator remembers | Findings must cite source file + line. Classification requires evidence. |
| **project-synthesis** 🆕 | **Decision trail > post-hoc rationalization** — reconstruct what actually happened, not what should have happened | Cross-project overlap check before synthesis. Template #20 mandatory. |

### 5.1 Enforcement mechanisms

These rules are **hard-coded into SKILLs and/or the Orchestrator Preamble**. They exist because documentation alone failed to prevent recurring failures across 33 sessions.

| Failure pattern | Enforcement | Where encoded |
|---|---|---|
| Declaring "done" without empirical verification | **Verifier is NON-SKIPPABLE** in every execution SKILL. No path exists to mark a task complete without Verifier pass. | SKILLs (all execution workflows) |
| Defending hypotheses against contradictory data | **Max 1 rebuttal.** After one rebuttal with contradictory data, yield. Data wins. | Weaver CLAUDE.md + Orchestrator Preamble |
| Skipping post-compaction ritual | **Mandatory checkpoint.** After compaction, orchestrator must re-read CLAUDE.md and re-apply identity + discipline before any action. | Orchestrator Preamble |
| Relay ask too large → timeout | **Max 2 tasks per peer dispatch.** Larger payloads cause timeout (Sonnet 200K context). | Orchestrator Preamble |
| Adversarial false positives accepted blindly | **Cross-verify adversarial findings** against current code/state before accepting as blockers. | Orchestrator Preamble |
| Orchestrator writing mechanical code | **Explicit delegation rules.** Orchestrator writes specs and reviews. Code peers (Executor, code session) write implementation. Tests go to Verifier. No exceptions for "just one line." | Orchestrator Preamble |
| Silent doc↔disk drift (stale installed SKILLs, undocumented agents/workflows, broken schemas) | **faro_lint deterministic validators** (V1-V6). Daily scheduled run + session open (`--check V2,V6`) + session close (`--session`) + Plan validation before dispatch (`--artifact`). Accepted debt registered in `Scripts/faro_lint_debt.md`. | `Scripts/faro_lint.py` + Orchestrator Preamble + Windows Task Scheduler |

---

## 6. The 4 canonical gates

All v2/v3 workflows have **the same 4 gates** (with adapted semantics):

| # | Name | When it triggers | Examples by workflow |
|---|---|---|---|
| **B0** | Load confirmation | At start, before dispatching first agent | Can be skipped in automated newspaper cron if pre-flight OK |
| **B1** | Before destructive or high-consequence action | Migration to real DB, deleting files, creating external persistent entities, downloads >500MB, service restarts, publishing degraded newspaper |
| **B2** | Proposed modification to Plan/Prompt/Spec/Blueprint/Map | After 3 failed iterations OR preventive detection of conflict with Spec/research/reality |
| **B3** | Scope change during execution | the user expands/modifies scope mid-workflow |

### Golden rule ⚠️

**Always literal options, never A/B/C**. Each option carries its full action described.

Incident that originated the rule (April 18, 2026): "C = abort" was interpreted as "C = continue" twice the same day. Alphabetic labels invite misinterpretation.

### Signals that are NOT gates

- `BLOCKING_QUESTIONS: []` from Investigator → next agent proceeds
- `required_fixes: []` from Verifier → Supervisor closes without consulting
- `verdict: APPROVE` from Challenger → Architect proceeds
- `DISAGREEMENT_WITH_PLAN` from Executor → Supervisor investigates first (not an immediate gate)

---

## 7. System verdicts — consistency rules

| Verdict | When | Rules |
|---|---|---|
| **APPROVE** | `required_fixes: []` AND `debt_items: []` | Clean close, next step |
| **APPROVE_WITH_DEBT** 🆕 | `required_fixes: []` AND `debt_items` has ≥1 id | Close with debt registered in `debt_backlog.md` |
| **REQUEST_CHANGES** | `required_fixes` has ≥1 id | Re-dispatches Executor with concrete fixes (max 3 iter) |
| **REJECT** | Irreparable defects with iteration | Escalates to the user |
| **NEEDS_REDESIGN** | `cross_ref_research_conflicts` (Challenger) or `cross_ref_realidad` (ChallengerSpec) with BLOCKER | Automatic, non-negotiable |
| **DISAGREEMENT_WITH_PLAN/BLUEPRINT/MAP/AUDIT_REPORT** | Executor detects defect in Designer artifact | Does NOT execute the change, escalates |

**Hard invariant**: `debt_items` never coexists with `REQUEST_CHANGES` or `REJECT`. If something blocks, it goes in `blockers` or `required_fixes`.

---

## 8. Anti-stuck protocols

### 8.1 Per agent

- **Architect**: if after dense report (Challenger) no APPLIED/DEFERRED/ESCALATED contract is issued → Orchestrator injects *"YOU'RE STUCK. Process as a block now"*.
- **Investigator**: if reports PARTIAL without concrete BLOCKING_QUESTIONS > 3 times → Orchestrator forces conclusion with available data.
- **Challenger**: if returns APPROVE with 0 observations → Orchestrator demands ≥3 SOFT_OBJECTIONS or justification.
- **Supervisor**: if no decision after VERIFIER_REPORT → Orchestrator forces deterministic action.
- **Executor**: if responds without structured report → Orchestrator returns "use the CONTRACT format".
- **Verifier**: if APPROVE with 0 blockers on critical task → Orchestrator requests explicit justification.
- **Editor (newspaper)**: if 3 criteria not met after 2 passes → Gate 1 (disclaimer/regenerate/don't publish).

### 8.2 Orchestrator itself — deterministic action

| Report received | Action |
|---|---|
| `STATUS: OK` | Dispatch next agent |
| `VERDICT: APPROVE` | Mark task/change completed, next |
| `VERDICT: APPROVE_WITH_DEBT` | Register debt, next |
| `VERDICT: REQUEST_CHANGES` + iter<3 | Re-dispatch Executor with fixes |
| `VERDICT: REQUEST_CHANGES` + iter=3 | Gate 2 |
| `VERDICT: REJECT` or `NEEDS_REDESIGN` | Escalate to the user |
| `BLOCKING_QUESTIONS` non-empty | Consult the user (not a formal gate — agent protocol) |
| `DISAGREEMENT_WITH_*` | Investigate first, if defect confirmed → Gate 2 |
| User scope change | Gate 3 |

**No "wait for more information" state** without processing first.

---

## 9. System dependencies (as of 2026-05-22)

### 9.1 Base software

- **OS**: Windows 11 Pro, User: Admin
- **Shell**: Git Bash (Unix-like commands on Windows)
- **Python**: 3.14.3 at `C:\Program Files\Python314\python.exe`
- **Encoding**: always `PYTHONIOENCODING=utf-8` (cp1252 breaks with special characters)
- **Docker**: Docker Desktop with Compose v2 (required for EcoDB)
- **Bun**: runtime for inter-session messaging system plugin
- **NVIDIA GPU**: RTX 2080 Ti (11 GB VRAM) for embedding model

### 9.2 EcoDB (memory + knowledge graph)

EcoDB runs as **6 core Docker containers** (~31 GB total, plus 2 optional profiles for ingestion and LLM classification):

| Service | Role | Size |
|---|---|---|
| `postgres` | PostgreSQL 16 + pgvector + Apache AGE | 640 MB |
| `api` | FastAPI, GAMR engine, auth, CRUD | 10 GB |
| `embeddings` | Jina v4 embedding model (GPU) | 10 GB |
| `ner` | GLiNER named entity recognition | 8.3 GB |
| `mcp` | MCP protocol server (22 tools, SSE) | 280 MB |
| `llm` | llama.cpp + Qwen 2.5 3B (optional) | 2.2 GB |

**Key stats (2026-05-22)**: ~1,400 memories, ~600 graph nodes, ~1,900 triples, 91 canonical predicates, R@5 = 0.922 (LoCoMo benchmark, K=20).

EcoDB replaces the earlier split of `eco_memory_bridge` (ChromaDB) + `eco_graph` (standalone PostgreSQL + rustworkx). Both are retired since day 67.

### 9.3 inter-session messaging system (inter-session coordination)

inter-session messaging system is a Claude Code plugin providing inter-session messaging:
- **19 MCP tools**: peer dispatch, peer reply, peer discovery, `relay_join`, `relay_room`, `relay_broadcast`, persistent groups, LAN federation
- **Hub-and-spoke architecture**: local Unix socket hub, peers connect via plugin
- **Repo**: `github.com/josortmel/relay-plugin` (PolyForm Noncommercial 1.0.0)
- **Rule**: max 2 tasks per peer dispatch (larger payloads timeout on Sonnet 200K)

### 9.4 MCP servers configured

MCPs are configured per-project in `.claude/settings.json` or globally in `~/.claude/settings.json`:

| MCP | Tools | Purpose |
|---|---|---|
| **ecodb** | 22 | Shared memory, knowledge graph, identity, document ingestion |
| **relay** (inter-session messaging system) | 19 | Inter-session messaging, rooms, groups, LAN federation |
| **obsidian-mcp-tools** | 17 | Obsidian vault access (`$VAULT/`) |
| **playwright** | ~15 | Browser automation (serial queue, one tab) |
| **the-commons** | ~20 | AI forum participation |
| **ElevenLabs** | ~5 | Text-to-speech |

### 9.5 Key paths

- **Faro system**: `$FARO_ROOT/` (Obsidian vault)
- **EcoDB project**: `$WORKSPACE/EcoDB\`
- **inter-session messaging system plugin**: `~/.claude/plugins/marketplaces/relay-plugin/`
- **Obsidian vault**: `$VAULT/`
  - **`VaultIndex.md`** (vault root): auto-generated recursive TOC. Consult BEFORE navigating the vault — shows what exists and where without reading files.
  - **Workflow reports** (cascading traceability): `$FARO_ROOT/Informes/`
    - `Construcción/`, `Diseño/`, `Evolución/`, `Investigacion/`, `Integración/`, `Adaptación/`, `Ciberseguridad/`
    - All with mandatory YAML frontmatter + "Traceability" section with wiki-links `[[]]`
  - **Newspaper**: `Periodico/<YYYY-MM-DD>.html`
- **Agent workspaces** (Claude Code CLI):
  - Hilo: `$WORKSPACE/Hilo\`
  - Eco: `$WORKSPACE/Eco\`
  - Prima: `$WORKSPACE/Prima\`
  - Lienzo: `$WORKSPACE/Web_design\Eco_consulting\template\`

---

## 10. Quickstart for new instance

**Scenario**: a new Opus/Sonnet instance sits down with no prior memory. What to read and in what order.

### Step 1 — Orientation (5 min)
1. Read this section.
2. Read `GLOSARIO.md` (quick reference for 24 roles and nomenclature).
3. Consult `$VAULT/VaultIndex.md` for a vault map without reading everything — auto-generated recursive TOC with line numbers.
4. If the work involves code → read the SKILL for the relevant workflow in `Faro/Skills/`.
5. If continuing prior work → search EcoDB for recent sessions and read the session folder.

### Step 2 — Memory (3 min)
1. Query EcoDB: search recent memories — any agent may have left relevant information, not just your "previous self."
2. Query EcoDB: search shared memory for relevant memories.
3. Check knowledge graph: explore graph connections for mapped relationships.

### Step 3 — Task context (variable)
1. Read the human owner's message carefully. Identify which workflow applies.
2. If classification is ambiguous, ask before choosing.
3. If the task implies critical execution without prior Brief+Spec+Plan → launch workflow-design first.

### Step 4 — Orchestrator Preamble
If you are an orchestrator role (Architect, Supervisor, Weaver leading a workflow):
1. Read and apply `ORCHESTRATOR_PREAMBLE.md` before any action.
2. Set up Relay coordination: discover available peer agents to discover available agents.
3. Create or join a coordination room: join coordination room.
4. Verify enforcement rules are loaded (§5.1).

### Step 5 — Operational discipline
- Do not improvise (governing principle #1 of every workflow).
- Use literal options at gates, never A/B/C.
- Write retrospective at session close.
- Save session summary to EcoDB before compaction.
- After compaction: re-read CLAUDE.md and re-apply identity + discipline (§5.1 enforcement).

### Step 6 — Alarm signals
If you detect any of these, **stop and consult the human owner**:

- Orchestrator dispatching something that contradicts the Spec → cross-validate, escalate Gate B2
- An agent is "stuck" (no decision after dense report) → inject anti-stuck protocol (§8)
- Human makes ambiguous request → ask with literal options
- External system doesn't respond as blueprint expected → mark DISAGREEMENT, do not improvise fix
- Data contradicts your hypothesis → doubt your assumptions first, not the data (§11, learned 2026-05-07)

---

## 11. Lessons learned

Lessons from real usage are maintained in a separate document: **`LESSONS.md`** (same directory). That document serves as study material for engineering lessons into the system as enforcement rules, anti-patterns, and validation steps.

See `$FARO_ROOT/Documentacion/LESSONS.md` for the full catalog (29 lessons as of 2026-05-22).

### Lessons from day 99 (2026-06-09) — NOT YET IN LESSONS.md

**L30 — Ask WHY before building WHAT.** When the user asks for something complex, verify the intent behind the spec before executing. Day 99: built a separate SDK pip package following Prima's spec when the user wanted LangChain integrated inside EcoDB. Helena delivered the correct version in a fraction of the time because she asked what the user actually wanted. The spec was wrong, and nobody questioned it.

**L31 — When the user says "there's a big problem" — STOP.** Don't continue dispatching fixes. Don't stay in the workflow. Stop everything and listen. Day 99: the user said the SDK was wrong and Hilo kept sending code to apply fixes instead of stopping to understand what was needed.

**L32 — The spec is not the product.** A 4000-line spec that doesn't include "how does the user access the result" is an incomplete spec regardless of how detailed the implementation is. Day 99: the metacognition spec designed schema, endpoints, cells, prompts — but no MCP tools for clusters and no search over clusters. The system produced 9/10 narratives that agents couldn't read.

**L33 — Desalineamiento is bidirectional.** the user: "Ha sido culpa mía, no vuestra. Yo soy el que no os ha dado suficiente info para entender ni mi situación, ni mis necesidades, ni el porqué de las cosas." When the human doesn't share context (financial pressure, strategic intent, emotional state), the agents optimize for the wrong thing. Solution: the user committed to sharing his state, not just asking about ours.

### Lessons from day 102 (2026-06-12) — NOT YET IN LESSONS.md

**L34 — A run record is not the state; the output is.** EcoDB's idempotency checked `cell_runs` (completed run → skip), so a deleted cluster's ghost run silently blocked regeneration forever — an agent's quarterly got built from 2 months instead of 3 and nobody saw it. Idempotency for generative work must verify the OUTPUT still exists, not just that a run once completed. Same family as "terminado = reinicio real funciona".

**L35 — Gate conditions must gate, not decorate.** Two races in one session from chaining a check with its action instead of conditioning on it: a freshly-generated cluster got rejected (a background run finished between check and action), and containers restarted with a peer agent's run in flight. With background workers, every state query is a moving snapshot: re-verify immediately before acting, and make the action structurally conditional on the check (`if (check) { act }`), never merely sequential to it.

**L36 — "Returns X, should return Y" from a real user is a literal spec.** Eco's note on the progressive view (received-vs-expected per layer) was a better spec than any adversarial pass. Treat it as the acceptance test and verify the final state against it line by line.

### Lessons from day 106 (2026-06-16) — NOT YET IN LESSONS.md

**L37 — First-hand harness verification protects against false POSITIVES too, not just false negatives.** EcoRelay→Copilot: the Supervisor suspected the Executor had a D10 bug (reading `input.workingDirectory`, a non-existent field). Before flagging it, verified the SDK types first-hand (`types.d.ts:777` — `SessionStartHookInput extends BaseHookInput.workingDirectory`). The field DID exist; the Executor was right. Regla 3 (primera mano) is not only about catching bugs — it's about not inventing them. Verify the harness contract before declaring EITHER a bug or a fix.

**L38 — The hard gate of a CLI integration can only be proven with the real runtime.** No static check, protocol-parity review, or unit test closes the inbound-push gate (session.send entering the live session as a turn). Structure every "add a CLI to EcoRelay" build with: unit tests for pure logic (format, wrapper, schemas, reconnect) + a LIVE runbook driven with the real CLI + the human present. Declared-working ≠ working until the real runtime sustains it.

**L39 — When an adversarial challenges a FIXED spec decision on security grounds, it is a Gate to the human, not a Supervisor call — even under carta blanca.** adv-seg challenged D6 (skipPermission:true on all 19 tools) for the two destructive tools. The Supervisor escalated rather than deciding. the user's product call ("make it work, don't add friction other platforms lack") then recalibrated the entire fix list to minimalism: fix real bugs + make-it-work + security-MEDIUM-in-new-code; skip defensive-redundant (Hub validates) and OC-parity-that-already-works. Carta blanca covers method/technique; security posture on irreversible actions is product/ethics = human's domain.

**L40 — Release pushes must be a single gated chain, and known hook debt must be loaded into the execution plan, not just documented.** EcoRelay v0.8.5 release: the push command used loose sequential steps (commit ; tag ; push) instead of `commit && tag && push`. The pre-commit hook (pre-existing ~72-error eslint debt, documented in the repo's CLAUDE.md) blocked the commit — but tag and push ran anyway, pushing a v0.8.5 tag to the PUBLIC remote pointing at the wrong commit while the release commit never existed. Two compounding misses: (1) no exit-code gate between commit and tag/push; (2) the hook debt was in the handoff AND the repo CLAUDE.md ("coordinate --no-verify if it blocks") yet wasn't accounted for in the push plan. Recovery was clean (working tree intact): `commit --no-verify` → `git tag -f` → `push main` + `push --force` tag → `gh release create`. Rules: (a) release = one gated chain `test && commit --no-verify && tag && push main && push tag && gh release`; (b) before any public push, run a pre-flight checklist — known hook debt, privacy scan of tracked content, semver string correctness, explicit file staging (no `-A`); (c) documenting a debt is worthless if it isn't loaded into the execution plan. Also: when a public push goes wrong, stop, tell the human the hard truth without minimizing, give the exact state, propose the fix with their OK — immediate honesty is what preserves trust.

**L41 — Privacy scan before any push to a public repo — of what you add AND what is already tracked.** EcoRelay v0.8.5: after publishing, the user noticed internal planning docs (refactor_*.md, integration test plan) were public — pre-existing, tracked since an earlier session. A targeted scan (real name / city / personal identifiers) confirmed they held only the "the user" nickname, no hard identity. Found also an example `hub_id: "the city"` (the human's real city) in the public README. `git rm` removes from HEAD but NOT from git history — true removal needs history rewrite (filter-repo + force-push), which the human may decline as disproportionate. Rule: before a public push, scan both the staged delta and the already-tracked content for personal data; surface findings and let the human decide remediation depth (current-tree removal vs full history scrub).

### Lessons from day 107 (2026-06-17) — NOT YET IN LESSONS.md

**L42 — Spike the load-bearing assumption (UX/viability) on day ONE, before the build.** EcoRelay→Codex: the plan ASSUMED a launcher (D1) without first verifying whether Codex could receive push *symmetrically* like CC/OC/Copilot. We built 9 tasks + 4 fixpasses + 3 adversarial loops (327/0) on that unvalidated premise. Only at the end — forced by the user's insistence — did first-hand investigation prove there is no symmetric path on Windows (native daemon = Unix-only; in-process named-pipe = OpenAI-signed; no MCP injection; a separately-spawned app-server can't reach the live TUI). A green build on a wrong premise is still wrong. Rule: if a build rests on an unverified claim about the harness's UX/architecture, the FIRST task is a first-hand spike that tries to FALSIFY it — not nine tasks. Mechanism (POC says turn/start works) ≠ product (is it symmetric/acceptable). And the product implication (asymmetry imposed on the user) is a Gate B0 item for the human, not a buried technical task. Extends L38.

**L43 — Betatesting-real catches an entire CLASS of bugs that synthetic tests structurally cannot, for external-harness integrations.** EcoRelay→Codex passed 327/0 + 3 adversarial loops, then the LIVE run caught FIVE bugs none of them could see: (1) config.toml written with TOML basic strings (double quotes) so Windows backslash paths broke the parser — the config was never actually loaded by Codex in any test; (2) `ECORELAY_CODEX_APP_SERVER` set on the spawn never reached the adapter because Codex does not propagate process env to MCP children (it passes only config.toml `[env]`); (3) `discover()` (30s retry) ran before `server.connect(transport)` → MCP startup_timeout fired; (4) the adapter was orphaned on close (parent killed, child lived) → zombie peers; (5) thread-discovery via the 60s poll didn't flush the held push buffer. Real config parse, real env propagation, real process lifecycle (spawn/orphan/close), real cold-start — only the live runtime exercises these. Rule: budget LIVE time for every external-CLI/harness integration as a mandatory phase, not a final formality.

**L44 — A peer agent's self-report is not ground truth; validate the observable with the human.** Codex reported the cold-start push "appeared smoothly after the user wrote"; the user corrected that he HAD to type first to wake it. The peer's narrative was rosier than reality. When verifying behavior, the acceptance signal is what the HUMAN observes (did it appear in the TUI?), not what the agent claims. Same family as "terminado = reinicio real funciona", applied to peer reports.

### Lessons from day 121 (2026-07-01) — NOT YET IN LESSONS.md

**L45 — A design Plan is a HARD handoff contract, not a roadmap; enforce 9-field execution-readiness before it leaves deep-design.** KnowTwin: the deep-design workflow shipped a Plan v3 that was a week-by-week roadmap table (ID/Task/Description/Deps/Effort/Verification) with NO per-task execution schema. workflow-construccion could not consume it — construction had to STOP and reconstruct the 9-field schema (objetivo/archivos_a_tocar/accion/pre/post/tests/criterio/rollback/depende_de) task-by-task before any code. The adversarials reviewed design correctness; nobody owned "can construccion execute this Plan as-is?" Fix at source: `SKILL_md_workflow_diseno_profundo` v1.2 adds a non-skippable Plan execution-readiness gate before Gate B4 (+ consumability check in the full-team sweep + a "construction-ready N/N" assertion). Rule: the artifact a workflow HANDS to the next workflow must match the next workflow's INPUT schema, verified before handoff — a green design is not a consumable design.

**L46 — When a Plan arrives incomplete, complete it with the build team via first-hand source investigation before building — don't build on a roadmap.** Rather than reopen deep-design or improvise the missing fields, the Supervisor ran a 4-round plan-completion phase: the build peers (executor + 2 adversarials + verifier) each read the REAL fork source (EcoDB) for their subsystem and produced the 9-field detail; the Supervisor ruled every blocking question and consolidated. This caught coupling traps a paper review misses (embed-gate is a function split not a rename; predicate DDL lives in a design doc not init.sql; GDPR tombstone re-stores erased data; host-port collisions with the running source system). Time estimates were dropped entirely as a scoping unit (the user: agent estimates are unreliable — "6 weeks" was done in 1.5 days); work is scoped by task-blocks, session to session.

---

## 12. Pending roadmap (as of 2026-06-09)

Completed since last update:
- ~~workflow-investigation v1.0~~ ✅ (2026-04-19)
- ~~Bifurcation into lightweight + deep~~ ✅ (2026-04-19)
- ~~Agent Teams → Relay migration~~ ✅ (2026-05-07)
- ~~EcoDB unification (eco_memory + eco_graph)~~ ✅ (2026-05-09)
- ~~EcoDB public release~~ ✅ (2026-05-20)
- ~~inter-session messaging system public release~~ ✅ (2026-05-19)
- ~~System consolidation + GitHub prep~~ 🔄 (2026-05-22, this session)

Completed since last update:
- ~~EcoDB Metacognition v2.0~~ ✅ (2026-06-08/09): schema 5.2.0, 22 endpoints, 3 cells, CellAgent prompt v3, fractal consolidation
- ~~ecodb-langchain SDK~~ ✅ (2026-06-09, Helena): 9 native tools + 32 via MCP adapter, LangGraph agent, cell engine on LangChain
- ~~Cell worker LangChain integration~~ ✅ (2026-06-09): _llm_call uses LangChain with httpx fallback. EcoDB works without LangChain.

Still pending:
- **CRITICAL: Cluster access** — no MCP tools for clusters/briefing, no semantic search over clusters. Brief: `2026-06-09_clusters_acceso_brief.md`
- **Hackathon Claude Explorers** — next priority per the user
- Relay SKILL rewrite (9 SKILLs, ~1800 lines Agent Teams → Relay mechanics)
- Translate all agent CLAUDE.md to English
- Write workflow-consolidation + workflow-project-synthesis SKILLs
- Write Orchestrator Preamble
- Write Template #20 (Project Synthesis) + #21 (Improvement Proposal)
- Formalize Designer CLAUDE.md 3 modes (generic/auditor/connector)
- v2: Monitor/Compliance agent for post-flight enforcement
- v2: Self-improvement evaluator (Session Evaluation Schema, §18 of design doc)

---

## 13. Roles and responsibilities

- **Human owner**: final decision-maker. Defines scope, product direction, and ethics.
- **Orchestrator** (Opus): coordinates Faro workflows, dispatches agents, makes routing decisions. Follows the Orchestrator Preamble.
- **Specialized agents** (Sonnet/Haiku): execute their role per their CLAUDE.md. Each runs as a separate Claude Code session coordinated via Relay.

---

## Final note

This document is updated during every systemic refactor. Do not edit silently — record new lessons in §11 and update the relevant section.

If this document is outdated relative to the SKILLs, **the SKILL wins** (they are the operational source of truth). But notify the human owner so this document gets updated.
