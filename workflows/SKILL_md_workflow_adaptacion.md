---
name: workflow-adaptacion
description: |
  Orchestrated workflow for connecting external tools or technologies with the internal specifics of the ecosystem. Use it when the user wants to make something that already exists (an API, an app, an external service) work specifically with the system's agents, projects, sessions, or memory — not just install it, but integrate it so it "knows" who Eco is, who Prima is, what session is active, what the memory graph looks like. Also activates when a generic tool must be customized for a specific agent, or when multiple agents need independent channels or instances in an external system.
metadata:
  version: "4.1"
  agent_teams_v3: 2026-04-26
  autor_v3: Prima
  estreno_v1: 2026-04-16
  endurecido_v2: 2026-04-18
  relay_rewrite: 2026-05-22
  invocation: relay session (separate Claude Code instance)
  motivo_endurecimiento: |
    Application of v3 methodology to workflow-adaptacion. The adaptation workflow has a particular nature — it works simultaneously in TWO realities (external system + internal ecosystem) and both can contradict the mapping proposed by the Designer-Connector. Guiding principle 2 here is DOUBLE: external reality + internal reality > proposed mapping.
tags:
  - workflow/adaptacion
  - agent/executor
  - agent/verifier
  - agent/investigator
  - agent/designer_connector
  - agent/designer
  - agent/scribe
---

# Workflow: Adaptation (v4 — Relay)

Orchestrates the connection of external tools with the internal specifics of the ecosystem. **Not installing** — making something external understand the context: agents, projects, active sessions, memory.

> **Guiding Principle 1 — No improvising**: Faro and sub-agents do not infer well. Everything explicit.
>
> **Guiding Principle 2 — Double reality > proposed mapping**: the Designer-Connector proposes a mapping between external system (API, app, service) and internal ecosystem (agents, projects, sessions, memory). If the reality of **either side** contradicts the mapping, reality wins. The Verifier tests with a **real end-to-end flow**, not simulation.
>
> **Guiding Principle 3 — Internal state may change during adaptation**: active session, active agent, active project — all may change while configuring. The adaptation must be robust to that change, or must declare it as an explicit limitation.
>
> **Guiding Principle 4 — External credentials are requested BEFORE starting**: tokens, API keys, app IDs. Ask the user at the start, not when the Executor gets stuck halfway.

---

## When it activates

Faro launches this workflow when:
1. the user asks to connect already-installed technology with the internal ecosystem.
2. And the task has been classified as trivial / standard / critical.

**Do NOT** use for:
- Installing new technology → workflow-integracion
- Modifying behavior of already-adapted tools → workflow-evolucion
- Building an adaptation from scratch (no precedent) with architectural decisions → workflow-diseño first

---

## Complexity levels

| Level | Criteria | Action |
|---|---|---|
| **trivial** | One external API to a single agent, no shared state, no dynamic credentials | Executor |
| **standard** | Multiple agents with independent instances/channels in external system, stable internal state | Connector + Executor + Verifier |
| **critical** | Bidirectional connection with dynamic state (active session changes, active project changes), or external system that maintains state between sessions | **workflow-diseño first**, then this workflow with Plan |

---

## The 4 human gates

### Gate B0 — Load confirmation

```
[GATE B0 — Load confirmation]
I have loaded workflow-adaptacion v4.

Assignment received: <summary>
External tool to adapt: <name + URL or reference>
Internal agents involved: <Eco, Prima, Faro, ...>
Level: <trivial | standard | critical>

**REQUIRED EXTERNAL CREDENTIALS** (guiding principle 4):
<Faro lists which credentials/tokens/IDs it thinks will be needed based on the tool>

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones\<YYYY-MM-DD>_<tech>_adaptacion\
- Reports: <path>\.faro\reportes_adaptacion\
- Agents:
    1. Designer-Connector — produces Adaptation Map (internal ↔ external)
    2. Executor (works both sides simultaneously)
    3. BLIND Verifier (real end-to-end flow with real cases)
    4. Scribe (includes future maintenance triggers)

Subsequent gates:
- B1 before creating entities in external system (bots, webhooks, API keys)
- B2 if the Adaptation Map requires revision
- B3 if the user changes scope

Options:
- "Proceed and give me the list of credentials I need to paste"
- "Adjust X"
- "Do not proceed"

What do I do?
```

### Gate B1 — Before creating persistent entities in external system

**When**: any action that creates state in the external system that is not automatically cleaned up (e.g. creating a Telegram bot, a GitHub webhook, an OAuth provider app, an API key).

```
[GATE B1 — Persistent entity creation in external system]
Step N of the Adaptation Map: <title>
Action: <"create 'Eco' bot in Telegram" | "register webhook in GitHub" | etc.>
Entity to create: <type + proposed name>
Consequence if it fails halfway: <orphaned entity in external system with... / no effect>
Cleanup if we decide to abort later: <command or procedure>

Options:
- "Proceed"
- "Stop the workflow — do not create yet"
- "Change the name/config first"

What do I do?
```

### Gate B2 — Adaptation Map requires revision

**When**: any of:
- External reality contradicts the mapping (e.g. API does not support multiple bots as the Map assumes)
- Internal reality contradicts the mapping (e.g. a session structure is assumed that does not exist)
- 3 Executor↔Verifier iterations fail

```
[GATE B2 — Adaptation Map requires revision]
Side where the conflict is: <"external" | "internal" | "both">
Specifically: <what the Map says vs what Executor/Verifier discovered>
Connector's proposal: <change to the Map>

Options:
- "Apply the change to the Map and resume"
- "Pause — I want to review manually"
- "Abort — this adaptation requires more design"

What do I do?
```

### Gate B3 — Scope change

```
[GATE B3 — Scope change]
Request: <literal>
Impact on Adaptation Map: <which parts it invalidates>

Options:
- "Apply the change"
- "Defer it"
- "Cancel the request"

What do I do?
```

---

## System agents — Relay (v4.0, 2026-05-22)

```
join coordination room

RELAY PEERS:
├── Connector (OPUS) — central, understands BOTH sides (external + internal), produces Adaptation Map
├── Executor (Sonnet) — works both sides simultaneously, reports to Connector
├── Verifier (Sonnet) — beta tester: real end-to-end flow with REAL data
└── Investigator (Haiku) — standby for querying APIs, external system docs

EPHEMERAL:
└── Scribe (Sonnet) — close + maintenance triggers

LEAD (Prima):
└── Gates, escalation if adaptation requires bridge (workflow-construccion).
```

| Agent | Type | Model | CLAUDE.md | Mode |
|---|---|---|---|---|
| **Connector** | Relay peer | **Opus** | `Designer/CLAUDE.md` | Connector |
| **Executor** | Relay peer | Sonnet | `Executor/CLAUDE.md` | — |
| **Verifier** | Relay peer | Sonnet | `Verifier/CLAUDE.md` | Real end-to-end beta tester |
| **Investigator** | Relay peer | Haiku | `Investigator/CLAUDE.md` | Standby |
| **Scribe** | Ephemeral | Sonnet | `Scribe/CLAUDE.md` | — |

### Direct communication

```
Connector reads external system + internal → produces Adaptation Map → disk
dispatch task to Executor
dispatch task to Connector  # Executor reports back
dispatch task to Verifier
dispatch task to Connector  # Verifier reports back
Connector consolidates → peer dispatch to Prima

If adaptation requires building a bridge:
dispatch task to Prima
```

### Bifurcation: Configuration vs Code (Prima's decision post-Map)

After the Connector delivers the Adaptation Map, Prima evaluates:

```
Does the Map resolve with CONFIGURATION or does it require NEW CODE?

CONFIGURATION (change configs, webhooks, credentials, routing):
  → Executor resolves it within Adaptation
  → Verifier tests end-to-end
  → Normal close

CODE (bridge, wrapper, adapter with its own logic):
  → The Adaptation Map becomes input for workflow-construccion
  → Construction has Opus Supervisor, Adversarials, beta tester,
    production readiness, minimum 2 loops
  → The Connector stays alive as consultant (understands both worlds)
  → When construction closes, Adaptation resumes for final end-to-end test
```

**The key**: the Connector designs the connection. If the connection needs real code, that code is built with all the rigor of construction. Bridges are not built with the lightweight adaptation team.

### Chain of command

- **the user**: gates, scope.
- **Prima**: final decisions, evaluates configuration vs code, escalates to workflow-construccion.
- **Connector (Opus)**: designs the connection, understands both sides. Consultant during construction if escalated.
- **Executor/Verifier**: execute and report (only in configuration path).

**Cost of idle relay peers**: zero tokens.

### Dispatch discipline — no idle Verifier (v4.1, propagated from construction v5.2)

**The Verifier does NOT wait for the full adaptation to complete.** As soon as a mapping step is implemented by the Executor, dispatch the Verifier to independently validate that step — while the Executor continues with the next mapping.

If the Verifier sits idle while completed steps exist unverified, the workflow is broken.

---

## Initial setup

```
$FARO_ROOT/Sesiones\<YYYY-MM-DD>_<tech>_adaptacion\
  ├── ENVIRONMENT.md
  ├── ECOSYSTEM.md     ← internal context, key for the Connector
  ├── CONTRACT.md
  ├── LESSONS.md
  └── orchestration.md

<internal path (e.g. plugin dir, config dir)>\.faro\
  └── reportes_adaptacion\
        ├── adaptation_map.md
        ├── ejecutor_paso_<N>_iter_<M>.md
        ├── verificador_paso_<N>_iter_<M>.md
        └── escribano_cierre.md
```

### Templates

- `$FARO_ROOT/Plantillas\ADAPTATION_MAP_template.md` (new)
- `$FARO_ROOT/Plantillas\ECOSYSTEM_template.md` (new — adaptation-specific)
- `$FARO_ROOT/Plantillas\ENVIRONMENT_template.md` (shared)
- `$FARO_ROOT/Plantillas\CONTRACT_template.md` (shared)
- `$FARO_ROOT/Plantillas\LESSONS_template.md` (shared)

---

## Minimum Adaptation Map schema

```
# Adaptation Map — <external tool> × <internal ecosystem>

## Metadata
- External tool: <name>, API version: <if applicable>
- Official docs: <URL>
- Internal ecosystem affected: <listed agents/projects>
- Date: <YYYY-MM-DD>

## 1. External reality (verified, not assumed)
- API/service capabilities: <list with reference to docs>
- Known limitations: <list>
- Quotas/rate limits: <numbers>
- Authentication: <mechanism + exact credential needed>

## 2. Internal reality (verified, not assumed)
- Active agents in the ecosystem: <list with project paths>
- Relevant dynamic state: <active session, active project, heartbeat, etc.>
- Available internal APIs/MCPs: <list>
- Where credentials live: <specific config file>

## 3. Internal ↔ external mapping
For each internal-agent × external-entity pair:
- **M<N>**: `<internal agent>` ↔ `<external entity>`
  - External representation: <bot_id, channel, webhook URL, etc.>
  - Input flow (external → internal): <how a message/event reaches the right agent>
  - Output flow (internal → external): <how an agent sends to the external system>
  - Dynamic state management: <what happens if the agent changes active session mid-operation>

## 4. Implementation plan (both sides, in order)
Each step:
- P<N>: <action>
  - Side: external | internal | both
  - Command/API call: <exact>
  - Entity created (if applicable): <bot, webhook, file>
  - Functional verification of the step: <command that proves the step did what it should>

## 5. End-to-end flow success criteria
Real cases the Verifier will test:
- [ ] <real case 1>: "<concrete input>" on external side → <correct agent> receives it → responds → external user sees response
- [ ] <real case 2>: if there are multiple agents, messages do NOT mix
- [ ] <real case 3>: system does not break if internal state changes during an operation

## 6. Maintenance triggers
What events in the internal ecosystem will invalidate this adaptation:
- "If a new agent is added, you need to..."
- "If the session structure changes, review..."
- "If the external API deprecates X version, migrate to..."

## 7. Rollback
How to fully unadapt:
- External side: <steps to delete created bots, webhooks, API keys>
- Internal side: <files/configs to revert>
```

---

## Workflow flow (literal prompts — condensed to avoid duplicating patterns)

### Step 0: Faro validates and prepares

1. Receives assignment.
2. Determines level. If critical → workflow-diseño first.
3. Pre-flight checks:
   - External tool accessible (ping/curl to its endpoint)
   - Internal ecosystem stable (MCPs active, EcoDB accessible)
   - External credentials identified (not necessarily obtained yet — that goes in Gate B0)
4. Generates `ECOSYSTEM.md` with current internal ecosystem state.
5. Creates session folder and reports.
6. **Gate B0** — includes list of required credentials.

### Step 1: Designer-Connector

Literal prompt (similar to other workflows, adapted):

```
<Designer/CLAUDE.md>

---

[ASSIGNMENT FOR YOU — Designer-Connector (workflow-adaptacion v4)]

External tool: <name>
Internal ecosystem: read `ECOSYSTEM.md` (path)

Your task:

1. **Understand BOTH sides before proposing mapping** (guiding principle 2 is double).
   - External side: read official docs. Identify capabilities, limitations, rate limits, authentication.
   - Internal side: read `ECOSYSTEM.md`. Identify agents, projects, dynamic state, internal APIs.

2. **Query EcoDB** (`search` tool) with tool tags + "adaptacion" and `autor="*"` — any agent may have documented relevant lessons.

3. **Propose mapping** that respects the limitations of both sides. Do not assume capabilities the API doesn't have. Do not assume internal structure that doesn't exist.

4. **Identify maintenance triggers**: what future events in the internal ecosystem will invalidate this adaptation? This is critical — adaptations break when the ecosystem changes and it is not detected.

5. Write Adaptation Map meeting minimum schema (7 sections).
   - Template: `$FARO_ROOT/Plantillas\ADAPTATION_MAP_template.md`
   - Save it at `<path>\.faro\reportes_adaptacion\adaptation_map.md`

6. If you detect the mapping requires complex architectural decisions → `requiere_escalacion_a_diseño: true`.

Return to me: Map path + summary + pre-commitment.
```

### Step 2: Executor (per each step in the Map, in order)

- If creating a persistent entity in external system → **Gate B1**.
- Prompt similar to integration, adapted: the Executor works both sides on the corresponding step.
- `STATUS: DISAGREEMENT_WITH_MAP` if reality differs from the Map.

### Step 2.5: BLIND Verifier — end-to-end flow

Critical here: verification with **real cases**, not simulated. Guiding principle 2 (double) is tested here.

Examples of functional verification for multi-agent Telegram adaptation:
- Send real message to bot_Eco → confirm Eco receives it in its active session
- Send message to bot_Prima → confirm it does NOT arrive to Eco
- During a conversation with Eco, change the active session → verify what happens

### Step 3: Scribe + Retrospective

Scribe with emphasis on **maintenance triggers** — when the internal ecosystem evolves, what needs to be reviewed in this adaptation. Saves in EcoDB (`save_memory` tool) with tags that allow finding it when an agent is modified.

---

## Reference case: multi-agent Telegram

One bot per agent (Eco, Prima, etc.) where each bot references the active session of the project:

- Bridge: incoming message → identify bot → active project → active session → agent
- Active session: queried at project heartbeat or from EcoDB
- Tokens at: `~/.claude.json` and Telegram plugin

**Maintenance triggers for this case**:
- If a new agent is added: create bot + update bridge + add reference in `~/.claude.json`.
- If "active session" structure changes: review bridge logic.
- If Telegram changes bot API: verify SDK/plugin is still compatible.

---

## Anti-stuck protocols

### Anti-stuck — Designer-Connector

If the Connector delivers a Map without a "maintenance triggers" section or without a verified "internal reality" section:

> *"The Adaptation Map without maintenance triggers is a time bomb. And the 'verified' internal reality cannot be assumed — confirm it by reading ECOSYSTEM.md and/or running queries against the ecosystem. Complete both sections."*

### Anti-stuck — Executor

If the Executor finishes a step without having tested the corresponding side with a real command:

> *"An adaptation step is not complete until you have tested that it works in reality. If the step was 'create bot', do you send a message to the bot and verify it responds?"*

### Anti-stuck — Verifier

If the Verifier tests with mocks/simulations instead of real cases:

> *"Guiding principle 2 is non-negotiable. Use the real system — if it's Telegram, send a real message. If there is risk of bothering users, create test channels/users, do not simulate."*

### Anti-stuck — Faro

In addition to standard rules, adaptation-specific:
- If the Executor already created persistent entities in the external system and the workflow aborts → trigger automatic cleanup (Map section 7) BEFORE closing the session.

---

## Healthy metrics

| Ratio | Target |
|---|---|
| Steps APPROVE in iter 1 | >65% (adaptations usually have surprises) |
| DISAGREEMENT_WITH_MAP / total steps | 10-25% (if 0 → Connector without reading docs; if >40% → premature mapping) |
| Verified end-to-end flows / Map criteria | 100% (non-negotiable) |
| Adaptations that break when ecosystem evolves / total adaptations | <5% per year (if more → poorly documented triggers) |

---

## Cost and performance

| Level | Duration | Tokens |
|---|---|---|
| trivial | <20 min | <40k |
| standard | 60-120 min | 150-300k |
| critical | with prior workflow-diseño — varies |

---

## Input and output dependencies (information routing between workflows)

### Expected inputs (what this workflow consumes)

**Typical optional inputs**:
- **Prior integration report** at `$FARO_ROOT/Informes\Integración\<YYYY-MM-DD>_<technology>.md` if the external technology was installed before — provides context on how it was set up and what credentials/configs exist.
- **Investigation report** at `$FARO_ROOT/Informes\Investigacion\` if adaptation patterns were researched (e.g.: "how others have connected N agents to an external system").
- **Design report** at `$FARO_ROOT/Informes\Diseño\` if the adaptation is critical and there was specific prior design.

For **critical** adaptation: usual precondition — Faro launches prior design if it touches the internal state of multiple agents (Eco, Prima, Hilo) or sensitive credentials.

### Output — final report archived by Scribe

- **Obsidian destination folder**: `$FARO_ROOT/Informes\Adaptación\`
- **File name**: `<YYYY-MM-DD>_<project_slug>.md`
- **Mandatory YAML frontmatter** — schema in `Scribe/CLAUDE.md`. For adaptation:
  ```yaml
  workflow: adaptacion
  version_workflow: "4.0"
  fecha: YYYY-MM-DD
  proyecto: <human name>
  proyecto_slug: <slug>
  tecnologia_externa: <name>
  identidades_internas_conectadas: [<list>]  # Eco, Prima, Hilo, etc.
  sesion_faro: $FARO_ROOT/Sesiones\<session>\
  informe_previo_consumido: "[[Integración/YYYY-MM-DD_tecnología]]"  # or null
  nivel: standard | critical
  adaptation_map: <faro_session_path>/adaptation_map.md
  verificacion_extremo_a_extremo: PASS | PARTIAL | FAIL
  triggers_mantenimiento: [<list>]
  siguiente_workflow_sugerido: ninguno | evolucion
  artefactos_faro:
    adaptation_map: <path>
    ecosystem: <path>/ecosystem.md
    retrospectiva: <path>
  eco_memory_ids: [<ids>]
  eco_graph_origen: Adaptacion_<project>_<date>
  tags: [workflow/adaptacion, estado/cerrado, proyecto/<slug>]
  ```
- **Mandatory "Traceability" section**: links to prior integration/investigation/design report, Adaptation Map, Ecosystem, Faro session, EcoDB, EcoDB graph.

### Typical next workflow

- **none** usually — it is the last link in the external→internal chain.
- **workflow-evolucion** if after real use feedback requires iterating the adaptation.

---

## Version history

- **v1.0**: first version with Designer-Connector, dual external/internal work, multi-agent Telegram reference case.
- **v2.0 (2026-04-18)**: hardening applying v3 methodology. Changes:
  1. **4 explicit guiding principles** (no improvising, double reality > mapping, internal state may change, credentials BEFORE starting).
  2. **4 human gates** with literal options (B0 includes credential list, B1 persistent external entity creation, B2 Map revision, B3 scope).
  3. **Minimum Adaptation Map schema** (7 sections, including mandatory maintenance triggers).
  4. **Explicit physical artifact location**. ECOSYSTEM.md adaptation-specific.
  5. **Literal prompts**.
  6. **Pre-flight checks**.
  7. **Referenced templates** (new ADAPTATION_MAP + ECOSYSTEM; shared ENV/CONTRACT/LESSONS).
  8. **Anti-stuck** per agent.
  9. **APPROVE_WITH_DEBT** from Verifier.
  10. **DOUBLE cross-validation**: external reality AND internal reality > proposed mapping. Verifier tests with real end-to-end flow, not simulated.
  11. **Automatic cleanup of persistent external entities** if workflow aborts after creating them.
  12. **Faro Retrospective** at close.
- **v3.0 (2026-04-26)**: migration to Agent Teams by Prima. Connector Opus, Executor Sonnet, Verifier Sonnet as persistent teammates. Haiku Investigator on standby. Direct communication. Explicit chain of command. Escalation to workflow-construccion for bridges.
- **v4.0 (2026-05-22)**: relay rewrite. Agent Teams → Relay. bisagra → gate. eco_memory/eco_graph → EcoDB. Agent name translations applied. Python spawn blocks removed. All content translated to English.
