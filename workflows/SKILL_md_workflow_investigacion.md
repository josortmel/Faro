---
name: workflow-investigacion
description: |
  Lightweight workflow for researching a topic before deciding what to build, integrate or change. Default for any "research how X works", "what have others done with Y", "before touching this I want to understand Z". Runs 1 loop by default with Haiku Investigators (parallel by focus, 1-3 max) and Sonnet Weaver for synthesis. If the topic is technically complex (4+ focus areas, very new technology <2 years, major strategic decision), escalates to workflow-investigation-deep. The report ends with actionable information for workflow-design, not with open questions to the user except those that require non-technical input (account tier, budget, ethical preferences).
metadata:
  version: "4.0"
  relay_rewrite: 2026-05-22
  created: 2026-04-19
  updated_v3: 2026-04-26
  author_original: Hilo
  author_v3: Prima
  invocation: relay session (separate Claude Code instance)
  motivation_creation: |
    After the productive debut of workflow-investigation v1.0 on 2026-04-19 (Telegram multi-bot plugin investigation, ~820k tokens, 2 loops, Opus Weaver), the user decided to fork. v1.0 remains as workflow-investigation-deep for complex cases. This v2.0 lightweight covers the default case: 1 loop, Haiku Investigators, Sonnet Weaver. Same 4 canonical gates. New guiding principle 5: the report must end with technical decisions made by the Weaver with their best judgment, not passing technical disjunctions to the user.
tags:
  - workflow/investigacion
  - agent/investigator
  - agent/weaver
  - agent/challenger
---

# Workflow: Investigation (v3.0 — Relay, lightweight, default)

Orchestrates a quick investigation on a topic. Produces an **Investigation Report** in a single pass with verifiable findings, detected contradictions, actionable hypotheses and open questions. The report feeds the next workflow (typically design).

> **Guiding principle 1 — Do not improvise**: every step, prompt, path and format must be explicit. If you read this skill and think "here I have to decide how X is done" — stop and consult the user (gate). Do not improvise the methodology.
>
> **Guiding principle 2 — Verifiable sources are authority superior to any agent**: without a citable URL/repo/doc, it is a HYPOTHESIS. Every finding must carry a source marker: [WF] WebFetch verified, [WS] WebSearch summary (= hypothesis), [PW] Playwright, [EMP] empirical test, [DOC] official docs, [INT] internal source. No marker → no fact. The Challenger rejects findings without markers or with [WS]-only markers presented as verified. Cuestionador review is MANDATORY after every Weaver synthesis — cannot be skipped. Government/OECD sites frequently return 403 — flag as [WS], escalate as "fuente inaccesible relevante." When Investigator disk reports are stubs, orchestrator produces `consolidado_loopN.md` from relay results before dispatching Weaver.
>
> **Guiding principle 3 — 1 loop by default**: the bet of this workflow is that for bounded topics (1-3 focus areas, known domain, lightweight decision) 1 well-directed pass + Challenger is sufficient. If the Challenger returns ≥1 critical gap, Gate B2 offers 3 options to the user (Focused Loop 2 / scale to deep / close with debt). Do NOT execute Loop 2 automatically — it is the user's decision.
>
> **Guiding principle 4 — WebFetch first, Playwright only if it fails**: hard cost-optimization rule. Investigators always attempt WebFetch FIRST. Only when it fails (blocked site, JS-heavy non-renderable, authentication required) do they escalate to Playwright. Keeps the workflow cheap.
>
> **Guiding principle 5 — Information ready for design**: the report must end with technical decisions made by the Weaver with their best judgment and justification. Only PRODUCT decisions are escalated to the user (subscription tier, budget, ethical preferences, appetite for non-standard technologies). Pure technical disjunctions (which of two equivalent libraries?, which architectural pattern?) the Weaver closes. The report should not end with "the user decides between H1, H2, H3" unless all three imply genuine product trade-offs.
>
> **Guiding principle 6 — Every `VERIFIABLE_FINDING` is first-hand (2026-04-19 late-final)**: a URL is verifiable **only** if an Investigator or Faro touched it directly in this workflow (WebFetch OK or Playwright navigated and extracted content). URLs cited in content from other sources (*third-hand*) go to `INACCESSIBLE_SOURCES`, never to `VERIFIABLE_FINDINGS`. The Weaver cannot promote a URL from inaccessible to verifiable without someone having visited it. The Challenger **must validate** a random sample of 3-5 URLs cited as verifiable before issuing APPROVE (rule 6 of their CLAUDE.md). Principle born from the **hyperdev-channels** case (2026-04-19): the initial investigation cited a repo as Apache-2.0 viable verifiable; the next day manual verification revealed the repo did not exist publicly (404), invalidating the central recommendation of the report. Cheap prevention against transitivity-of-trust bias in research.

---

## When it activates

Faro launches this workflow when:
1. the user asks to investigate, explore, understand, compare solutions, or "see what others have done" on a topic.
2. Before a workflow-design when the area is new or there are doubts but it is not exhaustively complex.
3. Typical phrases: *"investigate how X is solved"*, *"what options are there for Y"*, *"before building Z I want to know W"*.

Faro **does NOT** launch this workflow for:
- Quick searches for a specific data point → direct query with WebFetch/WebSearch without orchestration.
- Already-made decisions that only need technical validation → direct workflow-design.
- Reviews of existing code → workflow-evolution.
- **Complex** topics with 4+ focus areas, very new technology, or strategic decision → **workflow-investigation-deep**.

## Lightweight vs deep classification criterion

Faro classifies as `deep` ONLY if at least one is met:
- ≥4 distinct thematic focus areas.
- Very new or changing technology (<2 years, unstable API).
- Major strategic decision (affects long-term architecture, blocks several downstream workflows).
- Large information gaps that require triangulated research with 2 loops.

In all other cases → `investigation` (lightweight). If doubtful → lightweight first, and if the Challenger detects critical gaps it is escalated via Gate B2.

---

## The 4 human gates (mandatory)

**Golden rule**: complete literal options, never A/B/C.

### Gate B0 — Load confirmation + scope

```
[GATE B0 — Load confirmation]
I have loaded workflow-investigation v3.0 (lightweight, 1 loop default).

Brief received: <1-2 sentence summary>
Classified level: lightweight — <justification: N focus areas, known domain, decision of type X>

Proposed thematic focus areas (N, recommended 1-3):
- F1: <title + concrete question>
- F2: <title + concrete question>
- F3: <title + concrete question>

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones/<YYYY-MM-DD>_<topic>_investigacion/
- Report working copy: report.md (single version; if Gate B2 triggers Focused Loop 2, report_v2.md is generated)
- Definitive report (at close, by Scribe): $FARO_ROOT/Informes/Investigacion/<YYYY-MM-DD>_<topic>.md
- Agents I will launch:
    1. N Haiku Investigators in parallel (one per focus area)
    2. Sonnet Weaver → REPORT
    3. Sonnet Challenger → attacks REPORT
    4. If Challenger returns APPROVE or only soft objections: Weaver integrates minor fixes (v1.1)
    5. If Challenger returns REQUEST_CHANGES/NEEDS_MORE_RESEARCH with criticals: Gate B2
    6. Sonnet Scribe — final archive
    7. Faro retrospective

Tool protocol:
- WebFetch first. If it fails → Playwright (Faro serial queue).
- Playwright has 1 shared tab — parallel Investigators CANNOT use Playwright simultaneously.

Options:
- "Proceed" — I start setup + dispatch Haiku Investigators.
- "Adjust focus areas: <describe>" — reformulate scope.
- "Scale to deep" — I launch workflow-investigation-deep instead (2 loops, Opus Weaver).
- "Do not proceed" — I cancel without touching anything.

What do I do?
```

### Gate B1 — REPORT approval (always, at close)

```
[GATE B1 — REPORT approval]
Topic: <name>
Report: <path>

Weaver's executive summary: <3-5 sentences>

Metrics:
- Focus areas investigated: N
- Verifiable findings: M
- Inaccessible relevant sources: K
- Detected cross-cutting connections: C
- Derived hypotheses: H
- Remaining open questions: Q (only product decisions that require your input)

Challenger's report: <path>
  - Detected gaps: V
  - Critical: V_c
  - Covered by Weaver in v1.1 / by Focused Loop 2: <X/V>

Options:
- "I approve the report — proceed with Scribe to archive it"
- "I approve the report — don't archive yet, let me think about it"
- "Revise X before approving: <describe what to adjust>" — I relaunch Weaver with fixes
- "Scale to deep: the investigation did not cover what I needed" — I cancel archiving and launch workflow-investigation-deep with the already collected material
- "Reject — the report is not useful for design" — escalate, possible relaunch with different focus areas

What do I do?
```

### Gate B2 — Challenger detected criticals (escalation decision)

Only triggered if the Challenger returns `VERDICT: REQUEST_CHANGES` or `NEEDS_MORE_RESEARCH` with ≥1 critical gap.

```
[GATE B2 — Challenger detected N critical gaps]
Topic: <name>
Challenger report: <path>

Detected critical gaps:
  V1: <concrete description> — affects focus area F<X>
  V2: ...
  (total: N critical, M medium, K low)

Questions that Focused Loop 2 would close:
  Q1: <concrete question with specific URL/issue>
  Q2: ...

Weaver recommends: <technical proposal based on the criticals>

Options:
- "Focused Loop 2: launch 1-2 Haiku Investigators on these specific questions, then Weaver integrates in v1.1"
- "Scale to deep: scope exceeds the lightweight workflow; relaunch as workflow-investigation-deep leveraging already collected material"
- "Close with debt: report is archived with gaps documented as 'OPEN CRITICAL QUESTIONS'; I decide manually if they merit future follow-up"
- "Abort: the investigation is not viable with the available information"

What do you decide?
```

### Gate B3 — Scope change during investigation

Identical to workflow-investigation-deep:

```
[GATE B3 — Scope change detected]
the user's request: <literal description>
Current phase: <Step N of the Loop>
Already produced deliverables: <list>
Estimated impact:
  - Are current focus areas still relevant? <all | some | none>
  - Do we need to launch additional Investigators? <yes for which focus areas | no>

Options:
- "Apply the change — add/remove focus areas, reuse what has been investigated"
- "Apply the change but restart from scratch — discard what has been investigated so far"
- "Defer it for later investigation" — backlog
- "Cancel the request" — continue with original scope

What do I do?
```

---

## System agents — Relay (v4.0, 2026-05-22)

Each workflow is a **relay room**. Prima (lead) joins the room, contacts relay peers, and directs. Agents communicate directly with each other — Prima does not relay information.

### Team structure

```
join coordination room

RELAY PEERS (persistent, bidirectional via peer dispatch):
├── Weaver (Sonnet) — soul of the workflow, receives reports directly from investigators
├── Challenger (Sonnet) — adversarial, reads disk artifacts, direct feedback to weaver
└── inv-f1..fN (Haiku) — report to weaver, standby until weaver confirms close

SUBAGENT (ephemeral, one-shot):
├── Archivist (Haiku) — pre-flight (internal knowledge) + post-flight (metadata verification)
└── Scribe (Sonnet) — archives at team close

LEAD (Prima):
└── Gates, anti-stuck, escalation decisions. Does NOT relay information.
```

### Agent table

| Agent | Type | Model | Guaranteed tools | CLAUDE.md |
|--------|------|--------|--------------------------|-----------|
| **Weaver** | Relay peer | Sonnet | peer dispatch, Read, Write, Edit, Bash, project MCPs | `$FARO_ROOT/Agentes/Weaver/CLAUDE.md` |
| **Challenger** | Relay peer | Sonnet | peer dispatch, Read, Write, WebFetch (to validate URLs) | `$FARO_ROOT/Agentes/Challenger/CLAUDE.md` |
| **Investigators** | Relay peers | Haiku | peer dispatch, Read, Write, WebSearch, WebFetch, YouTube | `$FARO_ROOT/Agentes/Investigator/CLAUDE.md` |
| **Archivist** | Subagent | Haiku | Read, MCPs (EcoDB, obsidian) | `$FARO_ROOT/Agentes/Archivist/CLAUDE.md` |
| **Scribe** | Subagent | Sonnet | Read, Write, MCPs (EcoDB, obsidian) | `$FARO_ROOT/Agentes/Scribe/CLAUDE.md` |

### Direct communication (who talks with whom)

```
inv-f1 ──dispatch──→ Weaver     (direct report)
inv-f2 ──dispatch──→ Weaver     (direct report)
inv-f3 ──dispatch──→ Weaver     (direct report)

Weaver ──writes──→ report.md (disk)
Weaver ──idle notification──→ lead (Prima knows v1 is ready)

Prima ──dispatch──→ Challenger: "attack report at <path>" (reads from disk, no duplication)

Challenger ──dispatch──→ Weaver (direct feedback)
Challenger ──dispatch──→ lead (verdict for gate)

Prima evaluates verdict → gate if there are criticals
Prima ──dispatch──→ Weaver: "integrate fixes → v1.1"
        (Weaver ALREADY has the feedback in its context — no relay)

If Challenger detects gap → Prima ──dispatch──→ inv-fX: "expand investigation on <gap>"
        (Investigators remain alive in standby for this)
```

### Relay peer state by phase

| Phase | Weaver | Challenger | Investigators |
|---|---|---|---|
| Investigation | idle (waiting for N reports) | idle (waiting) | **working** |
| Synthesis | **working** (has all reports) | idle | idle (standby) |
| Attack | idle | **working** (reads disk) | idle (standby) |
| Gate evaluation | idle | idle | idle (standby — available if there are gaps) |
| Fix integration | **working** | idle | idle (standby) |
| Close | shutdown | shutdown | shutdown |

**Weaver rule**: does NOT start writing until ALL launched Investigators have sent their report. Their prompt includes: "You will receive reports from N investigators. Wait until you have all N before synthesizing."

**Investigators rule**: NOT shut down until the Weaver has integrated the Challenger's feedback. If the Challenger detects a gap in a focus area, Prima can contact the corresponding Investigator to expand without relaunching.

**Cost of idle relay peers**: zero tokens. Only consume OS resources (live process). Keeping them in standby has no API cost.

### Chain of command (non-negotiable)

Agents communicate directly for efficiency. Decision authority is NOT delegated:

- **the user**: product decisions (gates, scope, budget, direction).
- **Prima (lead)**: technical and operational decisions (escalate agent, stop, evaluate sufficiency, decide if a fix closes a gap or needs more work). The Weaver does not integrate fixes without Prima authorizing it. The Challenger sends direct feedback to the Weaver but Prima evaluates the verdict and decides the action.
- **Agents**: execute and advise. Do not decide. Direct communication is plumbing — saves tokens, does not delegate authority.

**Note on Haiku Investigators**: Haiku is significantly cheaper but less powerful. Mitigation: VERY concrete focus (1 question per Investigator), WebFetch-first protocol, strict report format. If an Investigator returns `PARTIAL` or `BLOCKED` repeatedly, Prima can escalate it to Sonnet as needed (technical decision, not a gate).

---

## Initial setup — file structure

```
$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<topic>_investigacion/
  ├── CONTRACT.md                  ← copy of Plantillas/CONTRACT_template.md
  ├── LESSONS.md                   ← copy of Plantillas/LESSONS_template.md
  ├── orchestration.md             ← append-only
  ├── consumed_sources.json        ← URL accumulator (in case Gate B2 triggers Focused Loop 2)
  ├── report.md                    ← produced by Weaver after Loop 1
  ├── report_v1.1.md               ← if Weaver integrates minor Challenger fixes without Loop 2
  ├── report_v2.md                 ← only if Gate B2 triggers Focused Loop 2
  ├── retrospective.md             ← at close, by Faro
  └── investigator_reports/
        ├── loop1_I1_<focus>.md
        ├── loop1_I2_<focus>.md
        ├── loop1_challenger_report.md
        └── loop2_I'<j>_<focus>.md (only if Focused Loop 2)
```

**Definitive destination**: `$FARO_ROOT/Informes/Investigacion/<YYYY-MM-DD>_<topic>.md` (copied by the Scribe).

---

## Mandatory minimum schemas

Identical to deep:

- **Investigation Report**: template `INFORME_INVESTIGACION_template.md`, 8 mandatory sections.
- **Investigator Report**: format with `VERIFIABLE_FINDINGS` / `INACCESSIBLE_RELEVANT_FINDINGS` / `URLS_PENDING_PLAYWRIGHT` / `UNRESOLVED_QUESTIONS` / `BLOCKING_QUESTIONS`.
- **Challenger Report**: 5 categories (GAPS, CONTRADICTIONS, UNSUPPORTED_HYPOTHESES, QUESTIONABLE_SOURCES, INSUFFICIENTLY_COVERED_FOCUS_AREAS) + QUESTIONS_LOOP_2_MUST_CLOSE + REQUIRED_CLARIFICATIONS + SOFT_OBJECTIONS + FINAL_VERDICT.

---

## WebFetch-first protocol with serial Playwright queue

Identical to deep. Haiku Investigators attempt WebFetch first; mark failed URLs as `PENDING_PLAYWRIGHT`; Faro consolidates and processes the queue one by one with Playwright after the parallel pass is complete.

Exception: if a focus area is *a priori* about JS-heavy sites (Reddit, SPA forums), Faro dispatches the Investigator with `MODE: playwright_from_start`.

---

## Workflow flow

### Step 0: Faro validates and prepares

1. Receives brief.
2. **Asks the user: "What decision do you want to make with this report?"** The literal answer is included in Gate B0 as `Report purpose`. Each Weaver hypothesis must answer this purpose. If it doesn't, it's superfluous.
3. Decomposes into **thematic focus areas** (1-3 normally). If 4+ clear focus areas emerge → Faro proposes in B0 to scale to deep.
4. Pre-flight checks:
   - EcoDB accessible
   - The 4 CLAUDE.md files exist
   - 3 templates exist
   - WebFetch + Playwright available
   - Obsidian vault accessible
5. **Reads `Documentacion/05_Referencia_EcoConsulting.md`** — current stack, tools, open problems, project direction.
6. Gate B0 → wait for confirmation.

### Step 0.5: Archivist pre-flight (MANDATORY before Gate B0)

**Hard rule: NEVER launch investigators without first auditing what we already know. Incident that originated this rule (2026-04-21): Prima launched 7 Haiku investigators to search "how to modify Claude Code system prompts" when tweakCC — the exact tool — was documented in the vault and in EcoDB from 6 days earlier. 500k tokens spent investigating what we already knew.**

Launch the Archivist to search for internal knowledge about the brief's topic. The Archivist does the deep search in EcoDB and Obsidian that the lead used to do manually.

```
peer dispatch(to="Archivist", question="""
<content of Archivist/CLAUDE.md>

---

[BRIEF — Archivist Pre-flight]

Workflow topic: <brief>
Project: <path>

Execute Mode 1 (Pre-flight) of your CLAUDE.md.
Search EcoDB (`search` tool), EcoDB graph (neighbors, search_nodes) and Obsidian vault for everything we already know about this topic.
Classify into DIRECT_ANSWERS / RELEVANT_CONTEXT / NOTHING_FOUND.
Deliver in ARCHIVIST_PREFLIGHT format.""")
```

**Result of Step 0.5 is included in Gate B0** as section `Internal knowledge found`. If the internal knowledge already covers the topic partially or fully → propose in B0 to reduce focus areas to what is NOT covered, or not to launch external investigation.

**Investigators receive as KNOWN CONTEXT everything found in this step.** They don't investigate what we already know — they investigate what we're missing.

### Step 1: Create room and launch agents

```
# 1. Join relay room
join coordination room

# 2. Contact Weaver (persistent — soul of the workflow)
peer dispatch(to="Weaver", question="""
<content of Weaver/CLAUDE.md>

---

[BRIEF — Sonnet Weaver, workflow-investigation (lightweight)]

You are a relay peer in a research team. You will receive reports from N investigators
directly via relay. **Do NOT start synthesizing until you have all N reports.**

Topic: <text>
the user's brief: <literal>
Report purpose (literal from the user): <text from Step 0>
Focus areas: F1..FN (you will receive 1 report per focus area)
Prior internal knowledge (from Step 0.5): <list>
Eco Consulting reference: <summary>

When you have all reports:
1. Produce REPORT complying with INFORME_INVESTIGACION_template.md (8 sections).
2. No citable source → HYPOTHESIS or OPEN QUESTION.
3. Section 5 (Cross-cutting connections) — your differential value.
4. Guiding principle 5: make technical decisions. Only escalate PRODUCT decisions.
5. Cross with internal knowledge. Verify against case constraints.
6. Each hypothesis answers the purpose.
7. Save REPORT in: <session path>/report.md
8. NO self-review — the report goes to the Challenger raw.

After the report, you will receive Challenger feedback directly via relay.
Integrate the fixes in v1.1 when it arrives.""")

# 3. Contact Challenger (persistent — adversarial with memory)
peer dispatch(to="Challenger", question="""
<content of Challenger/CLAUDE.md>

---

[BRIEF — Sonnet Challenger, workflow-investigation (lightweight)]

You are an adversarial relay peer. You will receive instructions from the lead (Prima) when there is
an artifact to attack. Read artifacts from disk — you will not receive the content by message.

When Prima tells you to attack:
1. Read the report from the indicated path.
2. Read the reference research from the indicated path.
3. Attack with the mandatory format from your CLAUDE.md.
4. Send your report via relay to 'Weaver' (direct feedback).
5. Send your verdict via relay to the lead (for gate).
6. Save the report to disk at the indicated path.

Minimum expected: 3 gaps + 3 concrete questions.
If you attack more than once, REMEMBER your previous attacks — verify if they were resolved.""")

# 4. Launch Investigators in parallel (1 per focus area, report to Weaver)
# NEVER pass full lead context — peers only need their brief
peer dispatch(to="inv-f1", question="""
<content of Investigator/CLAUDE.md>

---

[BRIEF — Investigator I1, workflow-investigation (lightweight)]

You are an investigator relay peer. Your focus is VERY concrete — do not expand scope.

Global topic: <text>
Your focus (F1): <title>
Concrete question: <text>
Scope context: <inside / outside>

Protocol: WebFetch first. If it fails → mark PENDING_PLAYWRIGHT.
No citable URL → UNRESOLVED_QUESTIONS, not VERIFIABLE_FINDINGS.

When done:
1. Save your report in: <session path>/investigator_reports/loop1_I1_<focus>.md
2. Send your complete report via relay to 'Weaver'.
3. Stay on standby — you may receive additional instructions if there are gaps.""")

# Repeat for inv-f2, inv-f3, etc.
```

### Step 1.5: Playwright queue (if applicable)

Identical to deep. Prima processes the serial queue and delivers results to the corresponding Investigator via relay.

### Step 2: Wait for Weaver synthesis

**Prima does NOT intervene.** The Weaver receives the N reports directly from the Investigators. When it has all of them, it synthesizes and writes report.md. Prima receives an idle notification when v1 is ready.

If an Investigator reports `PARTIAL` or `BLOCKED` → Prima evaluates whether to escalate to Sonnet or mark as insufficient coverage.

### Step 3: Prima activates the Challenger

```
peer dispatch(to="Challenger", question=
    "Attack the report at <session path>/report.md. "
    "Reference research at <session path>/investigator_reports/. "
    "Save your report at <session path>/investigator_reports/loop1_challenger_report.md")
```

The Challenger:
1. Reads the report from disk (without duplicating content by message)
2. Attacks with mandatory format
3. peer dispatch(to="Weaver") with direct feedback
4. peer dispatch(to="lead") with verdict for gate

### Step 3.5: Prima's decision per Verdict

Prima receives the Challenger's verdict via relay.

| Verdict | Prima's action |
|---|---|
| `APPROVE` (0 criticals) | Jump to Gate B1 with report v1 as is |
| `REQUEST_CHANGES` only soft objections | Weaver ALREADY has the feedback (direct from Challenger). dispatch task to Weaver. Then Gate B1. |
| `REQUEST_CHANGES`/`NEEDS_MORE_RESEARCH` with ≥1 critical | **Evaluate**: can the gap be closed by an Investigator still alive in standby? If yes → dispatch task to inv-fX. If not → **Gate B2** with the user. |

### Step 4 (optional — Focused Loop 2 if Gate B2 triggers it)

If Investigators are still alive (standby): Prima contacts them with the Challenger's questions. They avoid already-consumed sources.

If Investigators are no longer running (unlikely but possible by crash): launch 1-2 new ones as relay peers.

Investigators report to the Weaver directly. Weaver integrates in report_v2.md. Goes to Gate B1.

### Step 5: Gate B1 → the user's approval.

### Step 6: Close the relay room

```
# 1. Shutdown all relay peers
dispatch task to inv-f1
dispatch task to inv-f2
dispatch task to Challenger
dispatch task to Weaver

# 2. Scribe (ephemeral subagent, outside the relay room)
dispatch task to Scribe

# 3. Leave relay room
leave coordination room

# 4. Retrospective (Prima writes directly)
```

---

## Cost and performance (reference)

| Scenario | Estimated duration | Estimated tokens |
|---|---|---|
| Lightweight, 2 focus areas, direct APPROVE | ~15-25 min | ~50-100k |
| Lightweight, 3 focus areas, minor fixes (v1.1) | ~25-40 min | ~100-180k |
| Lightweight, 3 focus areas + Focused Loop 2 | ~40-60 min | ~180-300k |

Comparison: workflow-investigation-deep real debut = ~820k tokens, 2 complete loops, Opus Weaver.

---

## Healthy metrics

| Ratio | Expected |
|---|---|
| Verifiable sources / URLs touched | >60% |
| Actionable hypotheses per focus area | 0.5-2 |
| Challenger critical gaps | 0-2 (if >2, topic may have required deep) |
| Open PRODUCT questions at the end | 1-3 (genuine the user decisions) |
| Open technical questions at the end | **0 ideally** (guiding principle 5 — Weaver closes them) |

---

## Anti-stuck protocols

### Haiku Investigator → repeated PARTIAL
If an Investigator reports `PARTIAL` or `BLOCKED` >1 pass, Faro evaluates:
- If focus area is complex → escalate that Investigator to Sonnet as needed.
- If focus area is simple but sources are poor → mark focus area as "insufficient coverage" for the Challenger.

### Sonnet Weaver → leaves technical disjunctions as questions for the user
If the Weaver tries to leave something as "the user decides between H1/H2/H3" when there is evidence to recommend, Faro injects:
> *"Guiding principle 5: take a technical position. If H1, H2, H3 are alternatives without product trade-off, recommend one with justification. Only leave open if the choice involves tier/budget/preference."*

### Challenger → APPROVE with 0 observations
Identical to deep. Faro injects: "change angle, what sources were NOT cited that should be? Return at least 3 SOFT_OBJECTIONS".

### Prima (lead) — deterministic action table
| Signal received | Action |
|---|---|
| Idle notification from all Investigators | Process Playwright queue if there are pending. Weaver starts on its own (has all N reports). |
| Idle notification from Weaver (report.md written) | peer dispatch to Challenger: "attack report at <path>" |
| relay from Challenger with `VERDICT: APPROVE` | Jump to Gate B1 |
| relay with `REQUEST_CHANGES` only soft | Weaver already has the feedback (direct). peer dispatch: "integrate → v1.1" |
| relay with `REQUEST_CHANGES`/`NEEDS_MORE_RESEARCH` + criticals | Can Investigator in standby cover it? If yes → peer dispatch to Investigator. If not → Gate B2. |
| `BLOCKING_QUESTIONS` from Investigator | Consult the user (agent protocol) |
| Scope change | Gate B3 |

---

## Agent loading protocol

| Agent | Type | Model | Room | CLAUDE.md |
|--------|------|--------|-----------|-----------|
| Weaver | Relay peer | Sonnet | inv-<project> | `$FARO_ROOT/Agentes/Weaver/CLAUDE.md` |
| Challenger | Relay peer | Sonnet | inv-<project> | `$FARO_ROOT/Agentes/Challenger/CLAUDE.md` |
| Investigators | Relay peers | Haiku | inv-<project> | `$FARO_ROOT/Agentes/Investigator/CLAUDE.md` |
| Scribe | Subagent (general-purpose) | Sonnet | — (outside room) | `$FARO_ROOT/Agentes/Scribe/CLAUDE.md` |

---

## Input and output dependencies (information routing between workflows)

### Expected inputs (what this workflow consumes)

**None mandatory** — workflow-investigation is the first link in the information chain.

**Optional**: reports from related previous investigations in `$FARO_ROOT/Informes/Investigacion/` as historical context. The Weaver can cite them if they contribute — especially if the topic was already investigated and this session expands or updates the previous finding. Faro should do a search by project name / tags / date before Gate B0.

### Output — final report archived by the Scribe

- **Obsidian destination folder**: `$FARO_ROOT/Informes/Investigacion/`
- **File name**: `<YYYY-MM-DD>_<topic_slug>.md`
- **Mandatory YAML frontmatter** — full schema defined in `Scribe/CLAUDE.md`. For this workflow:
  ```yaml
  workflow: investigacion
  version_workflow: "3.0"
  fecha: YYYY-MM-DD
  proyecto: <human name>
  proyecto_slug: <slug>
  sesion_faro: $FARO_ROOT/Sesiones/<session>/
  informe_previo_consumido: null  # or "[[Investigación/YYYY-MM-DD_proyecto]]" if reusing prior investigation
  siguiente_workflow_sugerido: diseño | construccion | evolucion | integracion | adaptacion | ninguno
  artefactos_faro:
    informe: report.md
    retrospectiva: retrospective.md
    reportes_investigadores: investigator_reports/
  eco_memory_ids: [<ids>]
  eco_graph_origen: Investigacion_<topic>_<date>
  tags: [workflow/investigacion, estado/cerrado, proyecto/<slug>]
  ```
- **Mandatory "Traceability" section** at the end of the Obsidian report with `[[]]` links:
  - Link to prior consumed report (if exists).
  - Absolute path of the Faro session folder.
  - IDs of memories created in EcoDB.
  - Origin + author of triples in EcoDB graph.

### Typical next workflow

**workflow-design** when the investigation derives hypotheses that require Spec+Plan before implementing. For lightweight cases can go directly to **workflow-construction / evolution / integration / adaptation**. The Weaver marks `siguiente_workflow_sugerido` in the frontmatter so Faro chains it without improvising.

---

## Version history

- **v3.0 (2026-05-22)**: relay rewrite. Migrated from Agent Teams to Relay. TeamCreate/SendMessage/TeamDelete → relay_join/peer dispatch/relay_leave. Python spawn code blocks removed. All Spanish text translated. Paths updated to $FARO_ROOT/ pattern. Agent names translated to English.
- **v2.0 (2026-04-19)**: lightweight (new). 1 default loop, parallel Haiku Investigators, Sonnet Weaver, Sonnet Challenger, Sonnet Scribe. New guiding principle 5: information ready for design, not technical questions to the user. Forked from v1.0 (now workflow-investigation-deep). Designed for ~50-300k tokens vs ~820k of deep, ~15-60 min vs ~90 min.
- **v2.0 + traceability (2026-04-19 late)**: added "Input and output dependencies" section with explicit paths, mandatory YAML frontmatter and Traceability section in Obsidian report. Motivation: the user detected the cascade between workflows was too implicit.
- **v3.0 (2026-04-26)**: migration to Agent Teams. Changes:
  1. Weaver and Challenger as **persistent teammates** (bidirectional via SendMessage).
  2. Investigators as **teammates** reporting directly to the Weaver (no relay through Prima).
  3. Challenger sends direct feedback to Weaver AND verdict to lead — Prima does not relay.
  4. Investigators in **standby** until close — available to expand if Challenger detects gaps.
  5. Prima goes from "secretary who relays" to **lead who directs**: gates, anti-stuck, decisions.
  6. Scribe remains as ephemeral subagent at close (outside the team).
  7. Explicit state table by workflow phase.
  8. Motivation: first workflow-design (SocialIntel, 26-Apr) demonstrated that relaunching agents as new forks duplicates context (~750k tokens in 3 Architect lives) and loses internal memory. Agent Teams empirically validated same day.
- **v1.0 (2026-04-19)**: renamed to **workflow-investigation-deep**. Reserved for complex cases (4+ focus areas, very new technology, strategic decision). 2 minimum loops, Opus Weaver.
