---
name: workflow-periodico
description: >
  Orchestrated workflow for generating the user's daily personal newspaper in HTML, with his editorial
  criteria, enriched with historical analysis (EcoDB + EcoDB graph) and per-article reliability
  labeling. Use it when the user asks to generate today's newspaper or configure its automatic
  production. Typically triggered by morning cron (e.g. 08:00) or on demand with "generate today's
  newspaper". Not a daily briefing — it is a newspaper with 6 fixed sections, editorial curation,
  and historical contextualization.
metadata:
  version: "3.0"
  estreno_v1: "2026-04-18"
  endurecido_v2: "2026-04-18"
  relay_rewrite: 2026-05-22
  invocation: relay session (separate Claude Code instance)
  motivo_endurecimiento: >
    Application of v3/v2 methodology to workflow-periodico. v1 had good step structure and
    Editor anti-stuck, but lacked explicit guiding principles, gates with literal options,
    literal dispatch prompts, cross-validation (sacred editorial criteria, Critic > Editor
    on reliability), aggregated retrospective (weekly/monthly — not per daily session).
---

# Workflow: Newspaper (v3 — Relay)

Orchestrates the user's daily personal newspaper production. Unlike an RSS aggregator, it applies explicit editorial criteria, cross-references sources, labels per-article reliability, contextualizes with history, and delivers aesthetically pleasant HTML.

> **Guiding Principle 1 — No improvising**: Faro and sub-agents do not infer well. Everything explicit.
>
> **Guiding Principle 2 — Critic reliability > Editor ranking**: if the Editor prominently places an article that the Critic labels as LOW or NOT_VERIFIABLE, the Layout Designer **degrades its visual prominence** (red/yellow traffic light + note). The Editor can keep it in the section but not featured.
>
> **Guiding Principle 3 — Real history > invented Analyst narrative**: the Analyst finds patterns in EcoDB/EcoDB graph, **does not invent them**. If the Analyst suggests a "story of the day" without backing in concrete history, Faro rejects it.
>
> **Guiding Principle 4 — the user's 3 editorial criteria are sacred**: (a) perspectives from ≥3 geographic regions, (b) ≥1 article outside the mainstream, (c) each article with a verifiable source. If the Editor does not meet them after 2 attempts → Faro escalates to the user, no degraded newspaper is published.
>
> **Guiding Principle 5 — Scribe is the most undervalued agent**: saving tokens on the Scribe is an antipattern. Every day it doesn't archive well = day the future Analyst is blind. The newspaper's value grows by accumulation.

---

## When it activates

Faro launches this workflow when:
1. Morning cron triggers it (typically 08:00) — automatic mode.
2. Or the user requests it manually ("generate today's newspaper") — interactive mode.

The mode affects the gates (automatic mode skips Gate B0 if the date is correct).

**Do NOT** use for:
- Deep dive on a topic → `workflow-investigacion` (to be developed)
- Executive summary of last 24h → daily briefing, simpler
- If collected pool is very poor (<20 total items) → Faro alerts the user before producing a degraded newspaper

---

## Complexity levels

This workflow **has no levels** — it is always the same 6-agent flow. What varies:
- **Days 0-30 of use**: Analyst contributes little (empty history). Newspaper value comes from Editor + Critic.
- **Days 30-90**: Analyst detects continuities.
- **Days 90-180**: Analyst detects breaks and silences.
- **Days 180+**: Analyst can produce story of the day frequently (unexpected cross-section intersections).

---

## The 4 human gates

### Gate B0 — Load confirmation (interactive mode only)

In **automatic cron** mode, Faro skips Gate B0 if:
- System date is correct
- All CLAUDE.md files exist
- EcoDB + EcoDB graph accessible

If any of those fails, Gate B0 always fires (or aborts with notification to the user).

In **interactive** mode:

```
[GATE B0 — Load confirmation]
I have loaded workflow-periodico v3.

Mode: <"interactive" | "morning cron">
Newspaper date: <YYYY-MM-DD>
Output path: F:\obsidian\...\Periodico\<YYYY-MM-DD>.html

Pre-flight check:
- Internet: OK
- EcoDB: OK
- EcoDB graph: OK
- Obsidian vault: OK
- 6 CLAUDE.md present: OK
- Accumulated history: <N days since first newspaper> — Analyst contribution expectation: <low | medium | high>

Orchestration plan:
1. News-Investigator (6 searches per section)
2. Editor (curation + cross-ref + synthesis, with sacred criteria)
3. Source-Critic and Analyst in PARALLEL
4. Layout Designer (HTML with reliability traffic lights)
5. Scribe (archives + feeds memory)

Subsequent gates:
- B1 before publishing if reliability is mostly LOW or editorial criteria not met after 2 attempts
- B2 if the user wants to change editorial criteria during execution (rare)
- B3 if the user changes scope during execution (rare)

Options:
- "Proceed"
- "Regenerate only X" (e.g. "only section 4" — reinvokes Editor + Layout Designer with already collected pool)
- "Do not proceed today"

What do I do?
```

### Gate B1 — Before publishing if quality is degraded

**When**: if any of the following is true:
- Majority of newspaper articles have LOW or NOT_VERIFIABLE reliability according to the Critic
- The Editor does not meet the 3 quality criteria after 2 attempts
- There are <2 geographic regions represented (should be ≥3)

```
[GATE B1 — Degraded newspaper — confirm publication]
Degradation reason: <"majority LOW reliability" | "editorial criteria not met" | "regions <3">
Summary:
  - Reliability distribution: HIGH: X, MEDIUM: Y, LOW: Z, NOT_VERIFIABLE: W
  - Editorial criteria:
    - ≥1 article outside mainstream: <yes | no>
    - ≥3 distinct regions: <yes | no>
    - All with verifiable source: <yes | no>
  - Problematic articles: <list>

Options:
- "Publish with disclaimer" — Layout Designer adds top banner explaining the day's limitation
- "Regenerate with more collection" — Faro relaunches News-Investigator with broader queries
- "Do not publish today" — skip the day (Scribe records the reason, tomorrow's Analyst will see it)

What do I do?
```

### Gate B2 — Change of editorial criteria during execution

**When**: rare. If the user decides to adjust criteria (e.g. add a 4th criterion) mid-execution.

```
[GATE B2 — Change of editorial criteria]
Request: <description>
Impact on current newspaper: <"requires regenerating Editor" | "applies only to future editions">

Options:
- "Apply to today's newspaper — regenerate Editor"
- "Apply only to future editions — finish today's with current criteria"
- "Cancel the request"

What do I do?
```

### Gate B3 — Scope change

```
[GATE B3 — Scope change]
Request: <description>
Typical example: "add a new section", "remove section 6 today", "newspaper in English"

Options:
- "Apply to today's newspaper"
- "Defer to upcoming editions"
- "Cancel the request"

What do I do?
```

---

## System agents

| Agent | Role | CLAUDE.md |
|---|---|---|
| **News-Investigator** | Collects per section (6 sub-searches). Raw uncurated pool. **Always Haiku** (approved 2026-04-21). | `$FARO_ROOT/Agentes\News_Researcher\CLAUDE.md` |
| **Editor** | Always Opus. Applies sacred criteria. Curates + cross-references + synthesizes. | `$FARO_ROOT/Agentes\Editor\CLAUDE.md` |
| **Source-Critic** | Labels source type + per-article reliability (not per outlet). | `$FARO_ROOT/Agentes\Source_Critic\CLAUDE.md` |
| **Analyst** | Compares today's articles with history. Detects patterns with traceability. | `$FARO_ROOT/Agentes\Analyst\CLAUDE.md` |
| **Layout Designer** | Self-contained HTML with traffic lights. Degrades prominence of low reliability (principle 2). | `$FARO_ROOT/Agentes\Layout_Designer\CLAUDE.md` |
| **Scribe** | Archives + saves each article to EcoDB + triples in EcoDB graph. **Critical for cumulative value**. | `$FARO_ROOT/Agentes\Scribe\CLAUDE.md` |

Source-Critic and Analyst are launched in **parallel**, not in series.

**Agent persistence policy (2026-04-23):**

| Agent | Fork | Persistent (relay peer) | Reason |
|--------|------|--------------------------|-------|
| **Editor** (Opus) | **YES** — inherits orchestrator context (article pool, editorial criteria, history) | **YES** — if editorial criteria fail, 2nd pass via relay peer | Central Opus figure. Note: "You are not the same instance that invoked this workflow. You have inherited its context to work." |
| **News-Investigator** | No | No | One-shot Haiku, 6 sub-searches in one invocation |
| **Source-Critic** | No | **No — independent** | Parallel, must not see Editor context |
| **Analyst** | No | **No — independent** | Parallel, queries EcoDB but without session context |
| **Layout Designer** | No | No | One-shot, simple re-dispatch if needed |
| **Scribe** | No | No | Single invocation at close |

---

## Initial setup

```
$FARO_ROOT/Sesiones\<YYYY-MM-DD>_periodico\
  ├── ENVIRONMENT.md (includes today's and yesterday's date, output path)
  ├── CRITERIOS_EDITORIALES.md (Editor criteria snapshot — for reference)
  ├── pool_<YYYY-MM-DD>.json (Investigator output)
  ├── periodico_<YYYY-MM-DD>.json (Editor + Critic + Analyst output)
  ├── CONTRACT.md
  └── orchestration.md

F:\obsidian\...\Periodico\
  └── <YYYY-MM-DD>.html (final deliverable)

F:\obsidian\...\Periodico\
  └── <YYYY-MM-DD>_index.md (index note produced by Scribe)
```

### Templates

- `$FARO_ROOT/Plantillas\PERIODICO_POOL_template.json` (Investigator output structure)
- `$FARO_ROOT/Plantillas\PERIODICO_EDITADO_template.json` (post-Editor+Critic+Analyst structure)
- `$FARO_ROOT/Plantillas\CRITERIOS_EDITORIALES_template.md` (snapshot — source of truth in Editor/CLAUDE.md)
- `$FARO_ROOT/Plantillas\ENVIRONMENT_template.md` (shared)
- `$FARO_ROOT/Plantillas\CONTRACT_template.md` (shared)

---

## Minimum schemas

### Pool (News-Investigator output)

Already specified in `News_Researcher/CLAUDE.md`. Each item with: `id`, `titulo`, `resumen_fuente` (literal, not rewritten), `url`, `medio`, `seccion_objetivo` (1-5), `region`, `autor`, `fecha_publicacion`, `idioma`, `tipo_contenido`, `indicadores_brutos`.

**Hard rule reiterated in v3**: `resumen_fuente` is LITERAL (headline + lede). If the Investigator rewrites in its own words, Faro returns the pool.

### Edited (Editor output)

Minimum schema:
```json
{
  "fecha": "YYYY-MM-DD",
  "criterios_cumplidos": {
    "perspectivas_regiones": ["ES", "LATAM", "ASIA_ESTE", ...],  // must be ≥3
    "fuera_mainstream": true,  // must be true
    "todas_con_fuente_verificable": true  // must be true
  },
  "secciones": {
    "1_no_telediario": [3-5 articles],
    "2_ciencia": [2-3 articles],
    "3_empresas_tech": [2-3 articles],
    "4_mercados": {"compacto": "...", "indices": {...}, "acciones": [2-3]},
    "5_politica": [variable],
    "6_historia_larga": {"tema": "...", "desarrollo": "..."}
  },
  "cross_referencias": [
    {"noticia_a": "id", "noticia_b": "id", "relacion": "..."}
  ],
  "descartadas": [
    {"item_id": "...", "razon": "..."}
  ]
}
```

### Reliability (Critic output)

For each article in the edited:
```json
{
  "noticia_id": "...",
  "tipo_fuente": "DIRECTA | SECUNDARIA | TERCIARIA",
  "fiabilidad": "ALTA | MEDIA | BAJA | NO_VERIFICABLE",
  "nota_fiabilidad": "..." // required if MEDIA/BAJA/NO_VERIFICABLE
}
```

### Historical analysis (Analyst output)

For each article in the edited:
```json
{
  "noticia_id": "...",
  "patron": "continuidad | ruptura | relacion_indirecta | silencio | primera_vez",
  "contexto_historico": "...",  // with traceability: memories consulted
  "recuerdos_relacionados": ["memory_id_1", ...],
  "tripletas_relacionadas": [...]
}
```

Optionally: `narrativa_del_dia` if the Analyst detects a cross-section thread (mandatory backing in history — guiding principle 3).

---

## Workflow flow (literal prompts — condensed)

### Step 0: Faro validates and prepares

1. Determines mode (interactive or cron).
2. Pre-flight checks (listed above in Gate B0).
3. Generates ENVIRONMENT.md with today's and yesterday's date.
4. Copies Editor/CLAUDE.md → snapshot CRITERIOS_EDITORIALES.md.
5. **Gate B0** (interactive only; cron skips if pre-flight OK).

### Step 1: News-Investigator

Literal prompt: injects CLAUDE.md + assignment with the 6 sub-searches for the sections (detailed in Editor's CLAUDE.md). Expected 12-20 items per section, total 60-100.

**Post-delivery verification**: Faro validates:
- `DIVERSIDAD_FUENTES ≥ 10` distinct outlets
- No section with 0 items
- `resumen_fuente` is literal (not rewritten — grep against first lines of the real source)

If fails → Faro requests re-collection for the specific section.

### Step 2: Editor

Literal prompt with reminder of guiding principles 2 and 4:

```
<Editor/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Editor]

Collected pool: `pool_<YYYY-MM-DD>.json`
Date: <YYYY-MM-DD>

Your task:
1. Curate the pool applying the 3 quality criteria:
   - Perspectives from ≥3 geographic regions
   - ≥1 article outside the mainstream (the user's editorial principle: against filter bubble)
   - Each selected article with verifiable source
   These criteria are SACRED (guiding principle 4). If after first pass you don't meet them → go back to pool. If after second pass you still don't meet them → escalate to Faro.

2. Cross-reference: identify related articles across sections, note relationships.

3. Synthesize preserving what matters (do not over-summarize). Long articles deserve space.

4. For each curated article, prepare short prompt for Critic (which sources to check) and for Analyst (which historical connection to suggest looking for).

5. JSON output: `periodico_<YYYY-MM-DD>.json` (Editor part only — Critic and Analyst will complete it). Schema in SKILL.

**Do not prominently rank articles whose source seems questionable** (guiding principle 2 anticipated — the Critic will label them later, but the Editor must already be careful). If an article is important but source is questionable, include it with a note asking the Critic for special confirmation.

Return: partial `periodico_<YYYY-MM-DD>.json` + confirmation that the 3 criteria are met.
```

### Step 3: Source-Critic and Analyst (IN PARALLEL)

Faro launches both simultaneously. They receive the same partial JSON from the Editor. They do not see each other.

**Source-Critic** (literal prompt): labels tipo_fuente + reliability per article (not per outlet). Specific rules in its CLAUDE.md.

**Analyst** (literal prompt): for each article, queries EcoDB and EcoDB graph with relevant tags. Adds `contexto_historico` with traceability to specific memories/triples. If it detects a cross-section thread backed by concrete history → proposes `narrativa_del_dia`.

Faro integrates both outputs → complete `periodico_<YYYY-MM-DD>.json`.

**Post-delivery verification**:
- Critic: all articles have labels, reliability notes present where applicable.
- Analyst: `recuerdos_relacionados` not empty where there is `contexto_historico` (guiding principle 3 — no inventing without backing). If it detects story of the day without backing → Faro rejects it.

### Step 3.5: Quality gate — fire Gate B1?

Faro evaluates:
- Majority reliability (HIGH+MEDIUM / total)
- Editorial criteria met
- Regions represented

If thresholds not met → **Gate B1**.

### Step 4: Layout Designer

Literal prompt with emphasis on guiding principle 2:

```
<Layout_Designer/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Layout Designer]

Input: `periodico_<YYYY-MM-DD>.json` complete (edited + labeled + analyzed)
Template: A (newspaper)
Output: F:\obsidian\...\Periodico\<YYYY-MM-DD>.html

Your task:
1. Generate self-contained HTML (no external dependencies — inline CSS, no remote fonts).
2. Reliability traffic lights visible on each article (green/yellow/red).
3. **Guiding principle 2 — visual degradation**: articles with LOW or NOT_VERIFIABLE reliability go at REDUCED prominence even if the Editor placed them at the top of their section. Proposal: same Editor order but with reduced title size, yellow/red border, Critic note visible.
4. If there is `narrativa_del_dia` from the Analyst → featured banner with links to the composing articles.
5. If there is a quality disclaimer (Gate B1 with "publish with disclaimer") → top banner.

Return path + size. Faro validates: <300KB, UTF-8, 6 sections present (or explicit omission).
```

### Step 5: Scribe + memory update

Literal prompt with emphasis on guiding principle 5:

```
<Scribe/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Scribe (workflow-periodico)]

Finished newspaper: <HTML path>
Source JSON: <path>

Your task is the backbone of the long-term system (guiding principle 5). Do all 4 things:

1. **HTML archive**: already at `F:\obsidian\...\Periodico\<date>.html`. Confirm integrity.

2. **Index note in Obsidian**: `Periodico\<YYYY-MM-DD>_index.md` with:
   - Article list with link to HTML
   - Metadata: number of articles per section, regions covered, story of the day if any
   - Obsidian tags: #periodico #<date> #<main topics>

3. **Memories in EcoDB** (`save_memory` tool — one entry per significant article, not every item):
   - Author: "Scribe"
   - Content < 500 words (embedding limit)
   - Tags: section + topic + protagonist entities + `reliability` labeled by Critic
   - Tags are what allow tomorrow's Analyst to find this quickly. **Loose tagging = blind Analyst**.

4. **Triples in EcoDB graph** (`save_triples_batch` tool): for each article, the most important relationships:
   - `<entity> mentioned_in <article_id>`
   - `<entity_X> <action_predicate> <entity_Y>` (when the article asserts it)
   - `<article_id> belongs_to <section>`
   - `<article_id> cites <primary_source_url>`
   - With `origen="periodico_<YYYY-MM-DD>"` and `autor="Scribe"`

**DO NOT save tokens here**. Tomorrow's Analyst needs you well documented.

Report to Faro with SCRIBE_REPORT.
```

---

## Telemetry and retrospective

### Per-session telemetry

Faro records in EcoDB with author "Faro-periodico" after each edition (see v1 — same structure, maintained).

### Aggregated retrospective (new in v3)

Per-session retrospective is excessive for a daily workflow. In v3, Faro does **aggregated** retrospectives:

- **Weekly retrospective**: every Sunday, Faro aggregates metrics from the week's 7 editions → `$FARO_ROOT/Sesiones\retrospectivas_periodico\semana_<YYYY-WW>.md`. Content:
  - Aggregated metrics: average reliability, total regions covered, anti-stuck triggered, gates
  - Detected patterns: which section cost most? which day had a poor pool? is the Analyst gaining traction?
  - SKILL adjustment proposals if there are recurring patterns

- **Monthly retrospective**: first Monday of the following month, Faro aggregates weekly retrospectives → `mes_<YYYY-MM>.md`. Main input for upcoming SKILL versions.

---

## Anti-stuck protocols

### Anti-stuck — News-Investigator

If it delivers pool with rewritten `resumen_fuente` (not literal), Faro returns:

> *"`resumen_fuente` must be LITERAL — headline + lede from the original source. Your job is not to summarize, it is to collect. Synthesis is the Editor's. Re-deliver the pool with literal summaries."*

If it delivers pool with <10 distinct outlets or with an empty section:

> *"Source diversity is non-negotiable to avoid filter bubble. Re-collect with broader queries in <section>."*

### Anti-stuck — Editor

If it delivers without meeting the 3 criteria after first pass, Faro returns:

> *"Guiding principle 4 — the 3 criteria are sacred. Go back to the pool and search more. Identify which criterion is missing: regions? outside mainstream? verifiable source? You have 1 second pass before escalating to the user."*

If after second pass still not meeting → **Gate B1** with option "do not publish today".

### Anti-stuck — Source-Critic

If it labels the majority as NOT_VERIFIABLE without concrete justification per item:

> *"NOT_VERIFIABLE label requires a specific nota_fiabilidad per article. 'Could not verify' does not count — explain what you tried (searched for primary source, contacted author, etc.)."*

### Anti-stuck — Analyst

If it proposes `narrativa_del_dia` without concrete `recuerdos_relacionados` (guiding principle 3):

> *"The story of the day without backing in concrete history is invented. Either provide memory/triple IDs that support it, or do not propose it. I prefer an Analyst that says 'no story today' to one that invents."*

### Anti-stuck — Layout Designer

If it produces HTML that does not degrade low-reliability prominence (guiding principle 2):

> *"The Layout Designer does NOT blindly preserve the Editor's ranking. LOW/NOT_VERIFIABLE articles go with reduced prominence even if the Editor placed them first. Re-layout applying the principle."*

### Anti-stuck — Scribe

If the Scribe produces memories with vague tags or content > 500 words:

> *"Guiding principle 5 — your work is what will make the Analyst useful. Vague tags = blind Analyst. Content > 500 words = embedding rejected. Redo with specific tagging (entities, section, topic, reliability) and compact content."*

### Anti-stuck — Faro

Deterministic rules (expanded in v3):

| Signal | Action |
|---|---|
| Pool with <10 outlets / empty section | Re-dispatch Investigator with broader queries |
| Editor does not meet criteria after 2 passes | **Gate B1** (publish with disclaimer / regenerate / do not publish) |
| Critic labels >50% as LOW+NOT_VERIFIABLE | **Gate B1** |
| Analyst proposes narrative without backing | Reject, request version with IDs |
| Layout Designer does not degrade low reliability | Re-dispatch Layout Designer with reminder |
| User changes editorial criteria | **Gate B2** |
| Scope change | **Gate B3** |

---

## Cost and performance (v1 confirmed)

| Phase | Duration | Tokens |
|---|---|---|
| News-Investigator (6 searches) | 8-15 min | ~40-80k |
| Editor | 10-20 min | ~80-150k |
| Source-Critic (parallel with Analyst) | 5-10 min | ~30-60k |
| Analyst (parallel with Critic) | 5-10 min | ~30-60k |
| Layout Designer | 2-5 min | ~20-40k |
| Scribe | 3-7 min | ~30-60k |
| **Total** | **~25-50 min** | **~230-450k** |

The first 30 days, the Analyst will take less time and contribute less. After ~30 days of use the historical analysis starts to be dense.

---

## System evolution by accumulation (reiterated from v1)

1. **Days 0-30**: Analyst contributes little. Newspaper value comes from Editor + Critic. Accept the ramp-up curve.
2. **Days 30-90**: Analyst detects continuities.
3. **Days 90-180**: Analyst detects breaks and silences.
4. **Day 180+**: Stories of the day frequently — unexpected cross-sections.

The Scribe is the most undervalued agent (guiding principle 5).

---

## Version history

- **v1.0 (2026-04-18)**: first operational version. 6 fixed sections, 6 agents, self-contained HTML. the user's editorial criteria integrated in Editor/CLAUDE.md. Basic Editor and Scribe anti-stuck.
- **v2.0 (2026-04-18)**: hardening applying v3/v2 methodology. Changes:
  1. **5 explicit guiding principles** (no improvising, Critic > Editor on reliability, history > Analyst narrative, sacred editorial criteria, undervalued Scribe).
  2. **4 human gates** with literal options (B0 load — skipped in cron, B1 degraded newspaper, B2 editorial criteria change, B3 scope).
  3. **Minimum schemas** for pool, edited, reliability labeling, historical analysis.
  4. **Cross-validation**: Critic-Layout Designer (visual degradation), Analyst-EcoDB (mandatory backing for narrative).
  5. **Literal prompts** for each step.
  6. **Pre-flight checks** with cron/interactive distinction.
  7. **Anti-stuck** for each of the 6 agents.
  8. **AGGREGATED retrospective** (weekly + monthly), not per daily session — adaptation to the cyclic nature of the workflow.
  9. **Referenced templates** (PERIODICO_POOL, PERIODICO_EDITADO, CRITERIOS_EDITORIALES + shared).
  10. **Explicit quality gate** between Step 3 and Step 4 that fires Gate B1 if newspaper is degraded.
- **v3.0 (2026-05-22)**: relay rewrite. Agent Teams → Relay. bisagra → gate. eco_memory/eco_graph → EcoDB. Agent name translations applied. All content translated to English.
