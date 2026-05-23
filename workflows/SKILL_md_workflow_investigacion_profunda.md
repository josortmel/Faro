---
name: workflow-investigacion-profunda
description: |
  Orchestrated workflow for EXHAUSTIVE investigation when the topic is technically difficult and complex. Activate ONLY if at least one applies: 4+ distinct thematic focus areas, very new or changing technology (<2 years), major strategic decision with architectural consequences, or areas with large information gaps requiring triangulated research with 2 loops. Runs 2 minimum loops (Loop 2 avoids sources already consumed in Loop 1) and uses Opus for the Weaver — deep structural reasoning to detect patterns between focus areas. If the topic is more bounded (1-3 focus areas, relatively known domain, lightweight decision with available info), use workflow-investigation (lightweight) instead. Activate with phrases like "exhaustive deep dive into X", "I need to deeply understand how Y works", "complex topic with several angles, investigate thoroughly before deciding".
metadata:
  version: "4.0"
  relay_rewrite: 2026-05-22
  created_v1: 2026-04-19 (as workflow-investigacion)
  renamed_v2: 2026-04-19 (after productive debut — bifurcation into lightweight + deep)
  updated_v3: 2026-04-26
  author_original: Hilo
  author_v3: Prima
  invocation: relay session (separate Claude Code instance)
  motivation_rename: |
    After the productive debut on 2026-04-19 (Telegram multi-bot plugin investigation), the user detected the workflow was expensive in tokens (~820k) and methodologically heavy for bounded topics. Decision: fork into two workflows. This remains as "deep" (2 loops, Opus Weaver, Haiku Investigators — validated 2026-04-21) reserved for complex cases. The new lightweight workflow-investigation (1 loop, Haiku Investigators + Sonnet Weaver) covers the default case. Faro classifies: "deep" only if 4+ focus areas OR very new technology OR major strategic decision. "Lightweight" for everything else.
tags:
  - workflow/investigacion_profunda
  - agent/weaver
  - agent/investigator
  - agent/challenger
  - agent/scribe
---

# Workflow: Deep Investigation (v3.0 — Relay)

Orchestrates a multi-focus investigation on a topic. Produces a structured **Investigation Report** with verifiable findings, detected contradictions, actionable hypotheses and open questions. The report feeds the next workflow (typically design) to make informed decisions.

> **Guiding principle 1 — Do not improvise**: this workflow assumes that Faro and the subagents **do not infer well**. Every step, prompt, path and format must be explicit. If you read this skill and think "here I have to decide how X is done" — stop and consult the user (gate). Do not improvise.
>
> **Guiding principle 2 — Verifiable sources are authority superior to any agent**: if the Weaver or an Investigator claims something without a citable URL/repo/doc, it is a HYPOTHESIS, not a fact. The report strictly separates `VERIFIABLE_FINDINGS` from `INACCESSIBLE_SOURCES` and from `HYPOTHESES`. No source → no fact. The Challenger rejects the report if it detects hypotheses dressed as facts.
>
> **Guiding principle 3 — Two minimum loops, without repeating sources**: a single research pass is insufficient — it always leaves biases from the first set of searches. Loop 2 is mandatory and **receives the complete list of URLs consumed in Loop 1 to avoid them**. This forces exploring new branches, not reconfirming the same sources.
>
> **Guiding principle 4 — WebFetch first, Playwright only if it fails**: hard cost-optimization rule. Investigators always attempt WebFetch FIRST. Only when it fails (blocked site, JS-heavy non-renderable, authentication required) do they escalate to Playwright. This keeps the workflow cheap in tokens and time.
>
> **Guiding principle 5 — Every `VERIFIABLE_FINDING` is first-hand (2026-04-19 late-final)**: a URL is verifiable **only** if an Investigator or Faro touched it directly in this workflow (WebFetch OK or Playwright navigated and extracted content). URLs cited in content from other sources (*third-hand*) go to `INACCESSIBLE_SOURCES`, never to `VERIFIABLE_FINDINGS`. The Weaver cannot promote a URL from inaccessible to verifiable without someone having visited it. The Challenger **must validate** a random sample of 3-5 URLs cited as verifiable before issuing APPROVE (rule 6 of their CLAUDE.md). Principle born from the **hyperdev-channels** case (2026-04-19): Loop 2 of this same workflow cited a repo as viable verifiable; subsequent manual verification revealed the repo did not exist publicly (404), invalidating the central recommendation of report v2. Cheap prevention against transitivity-of-trust bias in research.

---

## When it activates

Faro launches this workflow when:
1. the user asks to investigate, explore, deep dive, compare solutions, or "see what others have done" on a topic.
2. Before a workflow-design when the area is sufficiently new or changing to require formal external research.
3. When the user says phrases like: *"before building X I want to know Y"*, *"investigate how Z is solved"*, *"what options are there for W"*.

Faro **does not** launch this workflow for:
- Quick searches for a specific data point → direct query with WebFetch/WebSearch without orchestration.
- Already-made decisions that only need technical validation → direct workflow-design.
- Reviews of existing code → workflow-evolution.

---

## Complexity levels

| Level | Objective criteria (one is enough) | Minimum loops |
|---|---|---|
| **standard** | 2-3 thematic focus areas, known domain, limited time available | 2 loops (mandatory) |
| **critical** | 4+ focus areas, new or very changing topic, strategic decision that depends on the result | 2 loops + possible Loop 3 via Gate B2 |

**2 loops are the absolute minimum** — there is no "fast one-loop" version in this workflow. A single pass leaves biases from the first set of searches.

If the classification is ambiguous → Faro asks the user at Gate B0.

---

## The 4 human gates (mandatory)

**Golden rule for gates**: options are always presented with **complete literal text**, never with A/B/C labels. Alphabetic labels invite misinterpretation. Each option carries its action described literally.

### Gate B0 — Load confirmation + scope

**When**: right after Faro receives the brief, before dispatching the first Investigator.

**What Faro does**:

```
[GATE B0 — Load confirmation]
I have loaded workflow-investigation-deep v1.

Brief received: <1-2 sentence summary>
Classified level: <standard | critical>
Loops to be executed: <2 minimum | 2 + possible Loop 3 in critical>

Proposed thematic focus areas (N):
- F1: <title + concrete question>
- F2: <title + concrete question>
- F3: <title + concrete question>
- ...

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones/<YYYY-MM-DD>_<topic>_investigacion/
- Report working copy: <path>/report_v1.md (after Loop 1), report_v2.md (after Loop 2)
- Definitive report (at close, by Scribe): $FARO_ROOT/Informes/Investigacion/<YYYY-MM-DD>_<topic>.md
- Investigator reports: <session path>/investigator_reports/
- Agents I will launch (in order):
    1. N Haiku Investigators in parallel (one per focus area) — Loop 1
    2. Opus Weaver — integrates Loop 1 → REPORT_v1
    3. Sonnet Challenger — attacks REPORT_v1
    4. N Haiku Investigators in parallel — Loop 2 (with list of consumed URLs to avoid)
    5. Opus Weaver — integrates Loop 2 → REPORT_v2
    [IF Gate B2 decides Loop 3:]
    6. Focused Investigators on gaps — Loop 3
    7. Weaver — REPORT_v3
    8. Scribe — final archive in Obsidian + EcoDB + EcoDB graph + retrospective

Navigation tools:
- Hard rule: WebFetch first. If it fails → Playwright (navigate + evaluate).
- Playwright has 1 shared tab — parallel Investigators CANNOT use Playwright simultaneously. Protocol in Step 2.

Subsequent gates I will trigger:
- B1: REPORT_v2 approval (always, before Scribe)
- B2: if Weaver marks loop_3_recommended or detects unresolvable contradictions
- B3: if the user expands/modifies scope midway

Options:
- "Proceed" — I start with physical setup and Loop 1.
- "Adjust focus areas — <describe which focus areas to remove/add/reformulate>"
- "Change level to <critical|standard>"
- "Do not proceed" — I cancel without touching anything.

What do I do?
```

### Gate B1 — REPORT_v2 approval (always)

**When**: at the end of Loop 2, after the Weaver delivers REPORT_v2. Before launching the Scribe.

**What Faro does**: presents to the user REPORT_v2 along with metrics from both loops and open questions.

```
[GATE B1 — REPORT_v2 approval]
Topic: <name>
Report v2: <path>

Weaver's executive summary: <3-5 sentences>

Metrics:
- Focus areas investigated: N
- Total verifiable findings: M (Loop 1: X, Loop 2: Y)
- Inaccessible relevant sources: K
- Detected cross-cutting connections: C
- Derived design hypotheses: H
- Remaining open questions: Q
  - Of which [RECOMMENDS_LOOP_3]: R

Challenger's report on REPORT_v1: <path>
  - Detected gaps: V
  - Gaps covered by Loop 2: <X/V>

Options:
- "I approve the report — proceed with Scribe to archive it"
- "I approve the report — don't archive yet, let me think about it"
- "Revise X before approving — <describe what to adjust>" — Faro relaunches Weaver with fixes
- "Do Loop 3 on <specific open questions>" — jump to Gate B2
- "Reject — the investigation did not cover what I needed" — escalate, possible relaunch with different focus areas

What do I do?
```

### Gate B2 — Unresolved contradictions or Loop 3 recommendation

**When**: if the Weaver marks `requires_pepe_decision_to_proceed=true` or `loop_3_recommended=true`, or if the Challenger detects critical gaps that Loop 2 did not cover sufficiently.

**What Faro does**:

```
[GATE B2 — Decision on continuing investigation]
Trigger cause: <"irresolvable contradictions" | "loop_3 recommended by Weaver" | "Challenger detects critical gaps in Loop 2">

Items that require your decision:

Item 1 — <contradiction | gap | open question>:
  Description: <text>
  Sources involved: <list with URLs>
  Weaver's context: <text>
  Technical options it sees: <text>
  Weaver's recommendation: <text>

Item 2: ...

the user's options per item:
- "For item N, launch focused Loop 3 on <what>"
- "For item N, leave it as OPEN_QUESTION in the final report"
- "For item N, accept as CONSCIOUS_OMISSION — out of scope"

Global option:
- "Launch full Loop 3 with focus areas <...>" — Loop 3 with N new focus areas
- "Close here with what we have, despite the gaps"
- "Abort the workflow — I need to think if it's worth continuing"

What do you decide?
```

### Gate B3 — Scope change during investigation

**When**: the user decides during the workflow to add, remove or modify thematic focus areas, or change the main topic.

**What Faro does**:

```
[GATE B3 — Scope change detected]
the user's request: <literal description>
Current phase: <Step N of Loop M>
Already produced deliverables: <list>
Estimated impact:
  - Are current focus areas still relevant? <all | only F1, F3 | none>
  - Do we need to launch additional Investigators? <yes, for which focus areas | no>
  - Does report v1 remain as base or do we need to restart? <remains | restart>

Options:
- "Apply the change — add/remove indicated focus areas, reuse what has been investigated"
- "Apply the change but restart Loop from scratch — discard what has been investigated so far"
- "Defer it for a later investigation" — the change stays as backlog
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
├── Weaver (Opus) — soul of the workflow, receives investigator reports, persists between Loop 1 and Loop 2
├── Challenger (Sonnet) — adversarial with memory, attacks v1, then verifies fixes in v2
└── inv-f1..fN (Haiku) — report to weaver, standby between loops to expand if there are gaps

SUBAGENT (ephemeral, one-shot):
└── Scribe (Sonnet) — archives at room close

LEAD (Prima):
└── Gates, anti-stuck, escalation decisions. Does NOT relay information.
```

### Agent table

| Agent | Type | Model | Guaranteed tools | CLAUDE.md |
|--------|------|--------|--------------------------|-----------|
| **Weaver** | Relay peer | **Opus** (deep structural reasoning) | peer dispatch, Read, Write, Edit, Bash, MCPs | `$FARO_ROOT/Agentes/Tejedor/CLAUDE.md` |
| **Challenger** | Relay peer | Sonnet | peer dispatch, Read, Write, WebFetch (validate URLs) | `$FARO_ROOT/Agentes/Cuestionador/CLAUDE.md` |
| **Investigators** | Relay peers | **Haiku** (validated 2026-04-21) | peer dispatch, Read, Write, WebSearch, WebFetch, YouTube | `$FARO_ROOT/Agentes/Investigador/CLAUDE.md` |
| **Scribe** | Subagent | Sonnet | Read, Write, MCPs (EcoDB, obsidian) | `$FARO_ROOT/Agentes/Escribano/CLAUDE.md` |

### Direct communication (who talks with whom)

```
LOOP 1:
inv-f1..fN ──peer dispatch──→ Weaver     (direct reports)
Weaver ──writes──→ report_v1.md      (disk)
Weaver ──idle notification──→ lead   (Prima knows v1 is ready)
Prima ──peer dispatch──→ Challenger: "attack report_v1 at <path>"
Challenger ──peer dispatch──→ Weaver     (direct feedback)
Challenger ──peer dispatch──→ lead       (verdict for gate)

LOOP 2:
Prima ──peer dispatch──→ inv-fX: "expand F2 with these questions, avoid these URLs"
inv-fX ──peer dispatch──→ Weaver         (Loop 2 direct reports)
Prima ──peer dispatch──→ Weaver: "integrate Loop 2 → report_v2"
Weaver produces v2 (REMEMBERS v1 completely)
Prima ──peer dispatch──→ Challenger: "attack report_v2, verify if v1 fixes were applied"
Challenger ──peer dispatch──→ Weaver + lead
```

### Chain of command (non-negotiable)

Agents communicate directly for efficiency. Decision authority is NOT delegated:

- **the user**: product decisions (gates, scope, budget, direction).
- **Prima (lead)**: technical and operational decisions. The Weaver does not integrate fixes without Prima authorizing it. Prima evaluates verdicts and decides actions.
- **Agents**: execute and advise. Do not decide. Direct communication saves tokens, does not delegate authority.

### Relay peer state by phase

| Phase | Weaver | Challenger | Investigators |
|---|---|---|---|
| Loop 1 Investigation | idle (waiting for N reports) | idle | **working** |
| Loop 1 Synthesis | **working** (has all reports) | idle | idle (standby) |
| Attack v1 | idle | **working** | idle (standby) |
| Evaluation | idle | idle | idle (standby — available for Loop 2) |
| Loop 2 Investigation | idle | idle | **working** (expanded focus areas) |
| Loop 2 Synthesis | **working** (remembers v1 + has L2 reports) | idle | idle (standby) |
| Attack v2 | idle | **working** (remembers attack v1) | idle (standby) |
| Close | shutdown | shutdown | shutdown |

**Weaver rule**: does NOT start synthesizing until ALL Investigators from the loop have sent their report. Their prompt includes how many reports to expect.

**Investigators rule**: NOT shut down until complete close. Available for Loop 2 expansions without relaunching.

**Key advantage of persistent Challenger**: in the attack on v2, REMEMBERS what it attacked in v1. Can verify if its critiques were resolved. Does not re-flag the same thing. Detects NEW issues introduced by the fixes.

**Key advantage of persistent Opus Weaver**: in Loop 2 REMEMBERS all of Loop 1 — reasoning, connections, discards. The v1→v2 coherence is organic, not reconstructed from disk artifacts.

**Cost of idle relay peers**: zero tokens. Keeping them in standby has no API cost.

**Note on Haiku Investigators**: VERY concrete focus, WebFetch-first protocol, strict format. If PARTIAL/BLOCKED repeated → Prima can escalate to Sonnet (technical decision, not a gate).

---

## Initial setup — file structure

Upon confirming Gate B0 with "Proceed", Faro executes this setup **before dispatching the first Investigator**:

### 1. Session folder (coordination + working copies)

```
$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<topic>_investigacion/
  ├── CONTRACT.md                      ← copied from Plantillas/CONTRACT_template.md
  ├── LESSONS.md                       ← copied from Plantillas/LESSONS_template.md
  ├── orchestration.md                 ← append-only Faro log
  ├── consumed_sources.json            ← global URL accumulator by loop (critical for Loop 2)
  ├── report_v1.md                     ← produced by Weaver after Loop 1
  ├── report_v2.md                     ← produced by Weaver after Loop 2
  ├── report_v3.md                     ← if Loop 3 (optional)
  ├── retrospective.md                 ← at close, by Faro
  └── investigator_reports/
        ├── loop1_I1_<focus>.md
        ├── loop1_I2_<focus>.md
        ├── loop1_challenger_report.md
        ├── loop2_I1_<focus>.md
        └── ...
```

### 2. Definitive destination (at close, by Scribe)

```
$FARO_ROOT/Informes/Investigacion/<YYYY-MM-DD>_<topic>.md
```

The Scribe copies the REPORT_v2 (or v3) from the session to the Obsidian vault. The session folder is preserved as historical record for retrospectives.

### 3. Referenced templates

- `$FARO_ROOT/Plantillas/INFORME_INVESTIGACION_template.md`
- `$FARO_ROOT/Plantillas/CONTRACT_template.md`
- `$FARO_ROOT/Plantillas/LESSONS_template.md`

---

## Mandatory minimum schemas

### Investigation Report (v1, v2, v3)

Mandatory template: `INFORME_INVESTIGACION_template.md`. 8 mandatory sections:

1. Metadata
2. Research question
3. Investigated thematic focus areas (table)
4. Findings by focus area (with `VERIFIABLE_FINDINGS` + `INACCESSIBLE_SOURCES`)
5. Cross-cutting connections
6. Derived design hypotheses
7. Open questions
8. Consumed sources annex (grouped by loop)

Faro returns the report to the Weaver if any section is missing.

### Investigator Report (per focus area)

Each Investigator delivers in their report:

```
INVESTIGATION_STATUS: OK | PARTIAL | BLOCKED
FOCUS: F<N> — <title>
ASSIGNED_QUESTION: <literal text>

VERIFIABLE_FINDINGS:
  H1: <text 1-3 sentences>
    URL: <link>
    Access date: <YYYY-MM-DD>
    Access type: WebFetch | Playwright
    Literal quote (if applicable): "<fragment>"
  H2: ...

INACCESSIBLE_RELEVANT_FINDINGS:
  IR1: <what it supposedly contains>
    URL: <link>
    Inaccessibility reason: <auth | 404 | blocked | JS-non-renderable | other>
    Referenced in: <verifiable URL that mentions it>
    Why relevant: <1 sentence>

CONSUMED_SOURCES: [complete list of URLs I touched — verifiable or not]

UNRESOLVED_QUESTIONS:
  D1: <question I could not close + why>

BLOCKING_QUESTIONS: [] | [concrete question for the user if it cannot be closed without human]

NEXT_ACTION: "The Weaver must integrate this focus area with the others."
```

### Challenger Report on REPORT_v1

Adapted for investigation (not a Brief, it's a report):

```
REVIEW_SUMMARY: <1-2 sentences>
VERDICT: APPROVE | REQUEST_CHANGES | NEEDS_MORE_RESEARCH

GAPS_DETECTED:
  V1 [critical|medium|low] <text> — affects focus area F<X>
  
UNRESOLVED_CONTRADICTIONS:
  C1 [critical|medium|low] between H<a> and H<b> — Weaver did not take a position

UNSUPPORTED_HYPOTHESES:
  HS1 [critical|medium|low] <text> — presented as fact, no source

QUESTIONABLE_SOURCES:
  FQ1 <URL> — reason: <personal blog without verification / no date / etc>

INSUFFICIENTLY_COVERED_FOCUS_AREAS:
  FI1 — F<X> has only <N> verifiable findings, topic demands more

QUESTIONS_LOOP_2_MUST_CLOSE:
  Q1: <concrete question>
  Q2: ...

REQUIRED_CLARIFICATIONS: [ids that BLOCK closing]
SOFT_OBJECTIONS: [improvement ids]

NEXT_ACTION: "Launch Loop 2 with additional focus areas <...> and questions <...>"
```

---

## WebFetch-first protocol with serial Playwright queue (new in v1)

This is a **hard workflow rule**, not advice:

1. **Parallel Investigators (Haiku) attempt WebFetch first for each candidate URL**.
2. **If WebFetch fails** (blocking error, unusable content, JS-heavy without render), the Investigator marks the URL as `PENDING_PLAYWRIGHT` and continues with WebFetch on the rest of their focus area.
3. When the Investigator finishes their WebFetch pass, they report to Faro with:
   - `VERIFIABLE_FINDINGS` (everything they managed to read)
   - `URLS_PENDING_PLAYWRIGHT` (list for Faro to process afterward)
4. **Faro consolidates all pending URLs from all parallel Investigators** into a single queue.
5. **Faro executes Playwright serially** (1 shared tab) on those URLs. The browser goes from one URL to the next — navigate + evaluate to extract what is relevant.
6. Faro redistributes Playwright results to the Investigator that requested each URL, so they can integrate them into their report before sending to the Weaver.

**Justification**:
- WebFetch is cheap and works for ~80% of public sites without heavy JS.
- Playwright is expensive (real browser, >10x tokens per page) but universal.
- The serial Playwright queue prevents 4 Investigators from trying to navigate simultaneously and competing for the single tab.

**Exception**: if a thematic focus area is *a priori* 100% about JS-heavy sites (e.g. Reddit, SPA sites), Faro marks it when dispatching the Investigator with `MODE: playwright_from_start` and that Investigator does not attempt prior WebFetch.

---

## Workflow flow (step by step, literal prompts)

### Step 0: Faro validates and prepares

1. Receives brief from the user.
2. **Asks the user: "What decision do you want to make with this report?"** The literal answer is included in Gate B0 as `Report purpose`. Each Weaver hypothesis must answer this purpose. If it doesn't, it's superfluous.
3. Decomposes the brief into **thematic focus areas** (2-6 normally). Each focus area is a concrete question assignable to an Investigator.
4. Determines level (standard/critical). If doubtful → asks at Gate B0.
5. Pre-flight checks:
   - EcoDB accessible (trivial status query)
   - The 4 CLAUDE.md files exist in `$FARO_ROOT/Agentes/` (Investigator, Weaver, Challenger, Scribe)
   - The 3 templates exist in `$FARO_ROOT/Plantillas/`
   - WebFetch available (test with a trivial URL)
   - Playwright available (`browser_tabs list` responds)
   - Obsidian vault accessible (`$FARO_ROOT/Informes/Investigacion/` exists or can be created)
6. **Reads `Documentacion/05_Referencia_EcoConsulting.md`** — current stack, tools, open problems, project direction.
7. Creates session folder, initializes empty `consumed_sources.json`, copies templates.
8. **Gate B0** — waits for the user's confirmation.

### Step 0.5: Internal knowledge audit (MANDATORY before Gate B0)

**Hard rule: NEVER launch investigators without first auditing what we already know. Incident that originated this rule (2026-04-21): Prima launched 7 Haiku investigators to search "how to modify Claude Code system prompts" when tweakCC — the exact tool — was documented in the vault and in EcoDB from 6 days earlier. 500k tokens spent investigating what we already knew.**

1. **Search in EcoDB**: `search` tool with topic query. Note relevant findings.
2. **Search in EcoDB graph**: `neighbors` and `search_nodes` tools. Note relationships.
3. **Search in Obsidian**: `search_vault_simple(query="<topic>")`. Look for guides, prior reports, internal documentation.
4. **Cross-check with Eco Consulting reference** (`05_Referencia_EcoConsulting.md`): are there tools in our stack that already solve this? Are there archived prior investigations?
5. **Compile**: list of documents, memories, tools and EXISTING knowledge about the topic.

**Result of Step 0.5 is included in Gate B0** as section `Internal knowledge found`. If the internal knowledge already covers the topic partially or fully → propose in B0 to reduce focus areas to what is NOT covered, or not to launch external investigation.

**Investigators receive as KNOWN CONTEXT everything found in this step.** They don't investigate what we already know — they investigate what we're missing.

---

### Loop 1 — Parallel Investigators

#### Step 1: Parallel dispatch of Investigators (Haiku, N instances)

**MANDATORY INVOCATION** — all Investigators are launched as relay sessions with a clean context:

```
dispatch task to inv-f<i>
```

- Each Investigator receives ONLY their brief — not the full lead context.
- Peer name → persistent in the room, addressable for Loop 2.
- Model: Haiku → low cost, sufficient format discipline.

**NEVER pass the full lead context to a peer.** Peers only need their brief.

For each focus area F<i>, Faro contacts an Investigator with this literal brief:

```
<content of Investigador/CLAUDE.md>

---

[BRIEF FOR YOU — Investigator I<i>, Loop 1 of workflow-investigation-deep]

Global topic: <text>
Your assigned focus area (F<i>): <title>
Concrete question you must answer: <text>

Additional context (workflow scope):
- Inside scope: <list>
- Outside scope: <list>

Tool protocol (mandatory):
1. For each candidate URL: attempt WebFetch FIRST.
2. If WebFetch fails (blocked, JS-heavy, error), mark the URL as PENDING_PLAYWRIGHT and continue with WebFetch on the rest.
3. When finished with your WebFetch pass, report with:
   - VERIFIABLE_FINDINGS (everything you managed to read)
   - URLS_PENDING_PLAYWRIGHT (list for Faro to process afterward)
4. Do NOT use Playwright yourself unless Faro dispatched you with MODE: playwright_from_start.

Hard rule: no citable URL → not a fact. It is a HYPOTHESIS (and goes to UNRESOLVED_QUESTIONS or a note to the Weaver, not to VERIFIABLE_FINDINGS).

Preferred sources (in order):
1. Official documentation of the relevant project.
2. Public repos (GitHub) with >1000 stars or with recent commits from known maintainers.
3. Issues/PRs/discussions in relevant repos — they are gold for detecting "how people really use X".
4. Academic papers last 2-3 years (arXiv, ACL, NeurIPS).
5. Technical blog posts from engineers with known identity (not corporate marketing).

Save your report in: $FARO_ROOT/Sesiones/<session>/investigator_reports/loop1_I<i>_<focus_slug>.md

Report format: see "Investigator Report" in the workflow SKILL.

Return the complete report to me.
```

#### Step 1.5: Faro processes Playwright queue

After receiving the N reports, Faro consolidates `URLS_PENDING_PLAYWRIGHT` from all Investigators. Processes serially with Playwright:

```
For each URL in queue:
  1. browser_navigate → URL
  2. browser_evaluate → extract content with JS (selector adjusted to site)
  3. browser_close (release resource for next)
```

Faro writes the extracted content in an appendix of the corresponding Investigator's report, marked as `[ADDED BY PLAYWRIGHT QUEUE]`. Then updates `consumed_sources.json` with all URLs touched in Loop 1.

#### Step 2: Weaver integrates Loop 1 → REPORT_v1

**Persistent relay peer:** The Weaver is contacted ONCE here and stays alive until Step 5 (Loop 2). In Step 5, Faro uses **peer dispatch** to the same peer instead of launching a new one. This avoids re-injecting context — the Weaver remembers its own REPORT_v1 and its pre-commitment.

**Relay context:** The Weaver receives the investigator reports, the user's brief, internal knowledge and Eco Consulting reference as part of its self-contained brief.

Literal brief:

```
<content of Tejedor/CLAUDE.md>

---

[BRIEF FOR YOU — Weaver, Loop 1 of workflow-investigation-deep]

NOTE: You are a relay peer in this workflow. Your role is Weaver — integrate, do not orchestrate. Follow ONLY your Weaver CLAUDE.md.

IMPORTANT: This peer session stays alive. After this brief you will receive via relay the Challenger's report and Loop 2 findings to produce REPORT_v2. You don't need to reread anything — you will remember what you do now.

Global topic: <text>
the user's original brief (literal): <text>
Focus areas investigated: <list F1..FN with titles>
Report purpose (literal from the user): <text from Step 0>
Prior internal knowledge (from Step 0.5): <list of ALREADY EXISTING documents, tools and memories>
Eco Consulting reference: <summary of stack, available tools, open problems, direction>

Investigator reports (as files):
  - <path loop1_I1_<focus>.md>
  - <path loop1_I2_<focus>.md>
  - ...

Your task:
1. Read the N reports completely. Don't paraphrase — integrate faithfully.
2. Produce REPORT_v1 complying with mandatory minimum schema (8 sections):
   - Template: $FARO_ROOT/Plantillas/INFORME_INVESTIGACION_template.md
3. Hard rule: no citable source → HYPOTHESIS, not fact.
4. Section 5 (Cross-cutting connections) is your differential value.
5. **CROSS WITH INTERNAL KNOWLEDGE (mandatory)**.
6. **VERIFY AGAINST CASE CONSTRAINTS (mandatory)**.
7. **EACH HYPOTHESIS ANSWERS THE PURPOSE**.
8. Save REPORT_v1 in: <session path>/report_v1.md
9. Do NOT self-review — the raw report goes directly to the Challenger.
10. Mandatory pre-commitment: write "I have delivered raw REPORT_v1. After receiving the Challenger's report and Loop 2 findings, I will integrate in bulk into REPORT_v2 without duplicating sources already cited in v1."

Return to me: path of REPORT_v1 + pre-commitment + metrics of your synthesis (VERIFIABLE_FINDINGS, INACCESSIBLE_SOURCES, CONNECTIONS, HYPOTHESES, OPEN QUESTIONS).
```

**Faro notes the Weaver's peer name to use it in Step 5 with peer dispatch.**

#### Step 3: Challenger attacks REPORT_v1

Literal brief:

```
<content of Cuestionador/CLAUDE.md>

---

[BRIEF FOR YOU — Challenger on REPORT_v1 of investigation]

Topic: <text>
Report to attack: <path report_v1.md>
Original Investigator reports (reference): <list of paths>

Your attitude: you are the most skeptical on the team. The Weaver has produced a synthesis. Your job is to detect where it fails:

1. Are there obvious gaps in focus areas that were not covered sufficiently?
2. Are there contradictions between sources that the Weaver did not take a position on?
3. Are there HYPOTHESES in section 6 that are actually presented as facts without being so?
4. Are there questionable sources (blogs without verification, sites without dates, marketing content)?
5. Are there critical open questions that Loop 2 should close?

YOU DO NOT HAVE ACCESS to the process. Only the report + Investigator reports + your judgment.

Your job: detect 5 types of defects (schema adaptation to investigation):
- GAPS_DETECTED
- UNRESOLVED_CONTRADICTIONS
- UNSUPPORTED_HYPOTHESES (presented as facts)
- QUESTIONABLE_SOURCES
- INSUFFICIENTLY_COVERED_FOCUS_AREAS

Mandatory format: see "Challenger Report on REPORT_v1" in the SKILL.

Hard rule: your `QUESTIONS_LOOP_2_MUST_CLOSE` feeds directly into the dispatch of Investigators in Loop 2. Be concrete. If you write "more investigation needed on X", the Investigator doesn't know what to do. Write "what patterns does project <URL> use to solve <Y>?" — that works.

Save the report in: <session path>/investigator_reports/loop1_challenger_report.md

Return the report to me.
```

---

### Loop 2 — Investigators cover gaps without repeating sources

#### Step 4: Loop 2 dispatch (Sonnet, N' instances — can differ from Loop 1)

Faro determines Loop 2 focus areas from:
- `QUESTIONS_LOOP_2_MUST_CLOSE` from the Challenger
- `GAPS_DETECTED` and `INSUFFICIENTLY_COVERED_FOCUS_AREAS`
- `OPEN_QUESTIONS` from REPORT_v1 that the Weaver flagged

For each Loop 2 focus area F'<j>, Faro dispatches with this literal brief (note the critical addition of "URLs to avoid"):

```
<content of Investigador/CLAUDE.md>

---

[BRIEF FOR YOU — Investigator I'<j>, Loop 2 of workflow-investigation-deep]

Global topic: <text>
Your assigned focus area (F'<j>): <title>
Concrete question: <text>

CRITICAL — SOURCES TO AVOID:
Loop 1 already consumed these URLs. Your job in Loop 2 is to find NEW sources on this focus area, not reconfirm those already consulted. Complete list (<N> URLs):

<content of consumed_sources.json, section "loop_1">

If one of these URLs is the only reliable source for your question, say so in your report ("the main source was already consulted in Loop 1, I did not find additional reliable sources") — do not cite it in full again.

Rest of protocol (WebFetch first, report format, etc.): identical to Loop 1.

Save your report in: <session path>/investigator_reports/loop2_I'<j>_<focus_slug>.md

Return the report to me.
```

#### Step 4.5: Faro processes Loop 2 Playwright queue

Identical to Step 1.5, with pending URLs from Loop 2.

#### Step 5: Weaver integrates Loop 2 → REPORT_v2

**Persistent relay peer:** Do NOT launch a new session. Faro uses **peer dispatch** to the Weaver that has been alive since Step 2. The Weaver remembers its REPORT_v1 and its pre-commitment. It only needs to receive: the Challenger's report, Loop 2 findings, and corrections identified by Faro.

Message Faro sends to the Weaver via peer dispatch:

```
[CONTINUATION — Weaver, Loop 2 of workflow-investigation-deep]

Your pre-commitment from Loop 1: "I will integrate in bulk into REPORT_v2 without duplicating sources already cited in v1". Fulfill it NOW.

Challenger's report on your REPORT_v1:
<literal content of Challenger report, or path if very long>

Loop 2 Investigator findings:
<summary of Loop 2 findings or paths to reports>

Critical corrections identified by Faro:
<list of corrections Loop 2 brings — e.g.: incorrect dates, degraded data, invalidated sources>

Your task:
1. Start from REPORT_v1 that YOU ALREADY REMEMBER as base.
2. Integrate Loop 2 findings WITHOUT duplicating sources cited in Loop 1. Reference by id.
3. Apply ALL corrections listed above.
4. Update sections 4, 5, 6, 7, 8.
5. Mark open questions that merit Loop 3 with [RECOMMENDS_LOOP_3].
6. Evaluate flags: requires_pepe_decision / loop_3_recommended.
7. Save REPORT_v2 in: <session path>/report_v2.md

Return: path + executive summary + metrics compared Loop 1 vs Loop 2 + flags.
```

---

### Gate B1 + Final step

**Gate B1** is triggered here. the user approves, rejects, requests adjustments, or requests Loop 3.

If the user requests Loop 3 → **Gate B2** and then cycle Step 4→5 with additional focus areas.

If the user approves → Scribe + retrospective.

---

### Step 6: Scribe + Faro Retrospective

#### Scribe (always, at close)

Literal brief:

```
<content of Escribano/CLAUDE.md>

---

[BRIEF FOR YOU — Scribe (workflow-investigation-deep close)]

Topic: <text>
Final state: <"investigation completed, N loops" | "aborted at <phase>">
Session folder: <path>
Final approved REPORT: <path report_v2.md or v3.md>

Read ALL workflow artifacts:
- REPORT_v1, v2 (and v3 if it exists)
- Investigator reports (both loops)
- Challenger report
- Accumulated LESSONS.md
- orchestration.md

Document in these 3 places (all mandatory):

1. Obsidian (definitive report destination):
   Path: $FARO_ROOT/Informes/Investigacion/<YYYY-MM-DD>_<topic>.md
   Content: complete copy of the final approved REPORT (v2 or v3).
   At the start of the file add metadata:
     ---
     workflow: investigacion-profunda
     version_workflow: 3.0
     fecha: <YYYY-MM-DD>
     tema: <text>
     loops_ejecutados: <N>
     focos: <N>
     hipotesis_derivadas: <N>
     preguntas_abiertas: <N>
     siguiente_workflow_sugerido: <diseno | construccion | evolucion | integracion | adaptacion | ninguno>
     ---

2. EcoDB (`save_memory` tool, author: "Scribe"):
   - 1 main memory with tags = [topic, "investigacion", key_technologies, "workflow-investigacion-profunda-v3"]
   - Content < 500 words: what was investigated, key findings, derived hypotheses, open questions
   - If the investigation generates a hypothesis that already calls for materialization, add 1 additional memory with tag "pending_design" or "pending_construction"

3. EcoDB graph (`save_triple` / `save_triples_batch` tools): minimum triples
   - `<topic>` was_investigated_on `<YYYY-MM-DD>`
   - `<topic>` produced_report `<Obsidian path>`
   - `<topic>` has_hypothesis `<H1 short title>` (for each derived hypothesis)
   - `<topic>` depends_on `<technology>` (if investigation revealed dependencies)
   - With `origin="Investigacion_<Topic>_<date>"` and `author="Scribe"`

Report to Faro with SCRIBE_REPORT confirming the 3 places updated.
```

#### Faro Retrospective

After the Scribe, Faro writes (without launching an agent) a retrospective in:
`$FARO_ROOT/Sesiones/<session>/retrospective.md`

Format:
```markdown
# Retrospective workflow-investigation-deep — <topic> — <date>

## What worked
- <skill bullets that helped>

## What did not work / where I improvised
- <points where the SKILL did not cover something>
- <Playwright collisions between Investigators, if any>
- <typos Faro introduced>

## Real metrics
- Loop 1 duration: X min
- Loop 2 duration: Y min
- Loop 3 executed: <yes/no>
- Approx tokens (both loops): ~N
- Total verifiable sources: N
- Inaccessible relevant sources: M
- Sources in Playwright queue (% of total): X%
- Derived hypotheses / total findings: X/N

## For v<N+1>
- <1-3 concrete changes to the SKILL that would improve the next execution>
```

---

## Cost and performance (reference)

| Complexity | Estimated duration | Estimated tokens | Dominant model |
|---|---|---|---|
| standard (2 focus areas, 2 loops) | ~30-45 min | ~80-150k | Haiku (Invest.) + Sonnet (Challenger) + Opus (Weaver) |
| critical (4-6 focus areas, 2 loops + possible Loop 3) | ~60-100 min | ~200-400k | idem |

Note: the Weaver (Opus) is estimated to consume ~30-40% of total cost; Investigators (Haiku — validated 2026-04-21) the rest.

---

## Healthy metrics

| Ratio | Loop 1 | Loop 2 | Note |
|---|---|---|---|
| Verifiable sources / URLs touched | >60% | >70% | Loop 2 should be more efficient (better targeting) |
| New Loop 2 sources / Loop 1 sources | — | 40-80% | >80% = Loop 1 was poor; <40% = Loop 2 did not contribute |
| Challenger gaps covered by Loop 2 | — | >70% | If <70%, consider Loop 3 |
| Derived hypotheses per focus area | 0.5-2 | +0-1 | Increase with Loop 2 is a sign of good synthesis |
| Pending Playwright URLs / Total URLs | <25% | <25% | If much higher, adjust preferred sources |

---

## Anti-stuck protocols

### Anti-stuck — Investigator
If reports `STATUS: PARTIAL` without concrete `URLS_PENDING_PLAYWRIGHT` or `BLOCKING_QUESTIONS` in >2 passes, Faro injects:
> *"Conclude with what you have. Mark low-confidence findings as 'single source, low confidence' and continue. The Weaver decides what to do with incomplete research — not you."*

### Anti-stuck — Weaver
If after receiving the Challenger's report, the Weaver does not emit updated REPORT_v2 in its next turn, Faro injects:
> *"YOU ARE STUCK. Process in bulk: 1) integrate Loop 2 findings, 2) close Challenger gaps, 3) mark open questions with [RECOMMENDS_LOOP_3] if applicable. Only escalate to Gate B2 what requires the user's decision."*

### Anti-stuck — Challenger
If it returns `verdict: APPROVE` with 0 observations (no gap, contradiction, questionable source), Faro injects:
> *"A perfect investigation report does not exist — there are always sources that were not consulted. If you see nothing, change the angle: what sources were NOT cited that should have been cited? Return at least 3 GAPS_DETECTED or mark verdict as 'APPROVE_WITH_OBSERVATIONS'."*

### Anti-stuck — Faro itself
| Report received | Faro action |
|---|---|
| `INVESTIGATION_STATUS: OK` (all loop Investigators) | Process Playwright queue + dispatch to Weaver |
| `VERDICT: APPROVE` (Challenger) without items | Skip Loop 2 only if the user confirms in ad-hoc gate; by default, execute Loop 2 anyway (hard workflow rule) |
| `VERDICT: REQUEST_CHANGES` (Challenger) | Loop 2 with focus areas derived from report |
| `VERDICT: NEEDS_MORE_RESEARCH` (Challenger) | Loop 2 + flag of possible Loop 3 at Gate B1 |
| `loop_3_recommended: true` (Weaver) | Gate B2 before Gate B1 |
| Non-empty `BLOCKING_QUESTIONS` (Investigator) | Consult the user before continuing (agent protocol, not formal gate) |
| User scope change | Gate B3 |

---

## Agent loading protocol

| Agent | Type | Model | Room | CLAUDE.md |
|--------|------|--------|-----------|-----------|
| Weaver | Relay peer | **Opus** | inv-deep-<project> | `$FARO_ROOT/Agentes/Tejedor/CLAUDE.md` |
| Challenger | Relay peer | Sonnet | inv-deep-<project> | `$FARO_ROOT/Agentes/Cuestionador/CLAUDE.md` |
| Investigators | Relay peers | Haiku | inv-deep-<project> | `$FARO_ROOT/Agentes/Investigador/CLAUDE.md` |
| Scribe | Subagent (general-purpose) | Sonnet | — (outside room) | `$FARO_ROOT/Agentes/Escribano/CLAUDE.md` |

---

## Input and output dependencies (information routing between workflows)

### Expected inputs

**None mandatory** — same as lightweight, it is the first link.

**Optional**: prior investigations in `$FARO_ROOT/Informes/Investigacion/`. Faro searches by name/tags before Gate B0. If a recent investigation already exists on the same topic, the Weaver cites it instead of re-investigating.

### Output — final report archived by the Scribe

- **Obsidian destination folder**: `$FARO_ROOT/Informes/Investigacion/` (shares folder with lightweight — they are the same type of product, what changes is depth).
- **File name**: `<YYYY-MM-DD>_<topic_slug>.md`
- **Mandatory YAML frontmatter** — schema in `Escribano/CLAUDE.md`. The only difference from lightweight: `workflow: investigacion-profunda` and `version_workflow: "3.0"`.
- **Mandatory "Traceability" section** at the end of the Obsidian report with `[[]]` links.

### Typical next workflow

Identical to lightweight: **workflow-design** typically; direct to execution for cases where the investigation already resolved.

---

## Version history

- **v4.0 (2026-05-22)**: relay rewrite. Migrated from Agent Teams to Relay. TeamCreate/SendMessage/TeamDelete → relay_join/peer dispatch/relay_leave. Python spawn code blocks removed. All Spanish text translated. Paths updated to $FARO_ROOT/ pattern. Agent names translated to English. Memory references: eco_memory → EcoDB (`search`/`save_memory` tools), eco_graph → EcoDB graph (`neighbors`/`search_nodes`/`save_triple` tools).
- **v3.0 (2026-04-26)**: migration to Agent Teams by Prima. Same changes as workflow-investigation v3.0: Opus Weaver and Sonnet Challenger as persistent teammates, Haiku Investigators as teammates on standby between loops, direct communication without relay through Prima, explicit chain of command. Extra advantage in deep: Opus Weaver persists between Loop 1 and Loop 2 with complete memory — the v1→v2 coherence is organic. Challenger remembers v1 attacks when attacking v2.
- **v1.0 (2026-04-19)**: first version — created by Hilo applying the hardened pattern of the 6 v2/v3 workflows. Awaiting productive debut with investigation on Claude Code Telegram plugin. Design based on explicit the user decisions:
  1. Haiku Investigator (validated 2026-04-21, previously Sonnet), parallel by focus area.
  2. **New Weaver agent** (Opus) for synthesis and integration.
  3. Sonnet Challenger to detect gaps.
  4. **2 minimum loops** (Loop 2 avoids sources consumed in Loop 1).
  5. Close with Scribe.
  6. 4 canonical gates with literal options.
  7. **2 source categories**: verifiable + inaccessible but relevant.
  8. Definitive output in Obsidian `$FARO_ROOT/Informes/Investigacion/`.
  9. Stop and wait for the user's decision (does not auto-chain to next workflow).
  10. **WebFetch-first protocol with serial Playwright queue** (new in v1, motivated by empirical validation on 2026-04-19: WebFetch works on public GitHub, fails on Reddit; Playwright + browser_evaluate resolves Reddit but with 1 shared non-parallelizable tab).
