---
name: workflow-frontend
description: |
  Orchestrated workflow to build frontend interfaces, dashboards, and visual components. Use it when the user wants to create or iterate on a UI that does not exist yet — a dashboard, a landing page, a component library, a visual feature. Also activates when the user says "build the dashboard", "we need a frontend for X", "make the UI for Y". The difference from workflow-construccion is that this workflow has a design authority (Lienzo) who reviews visual quality and brand compliance at every stage, and a visual adversarial that reviews against DESIGN.md.
metadata:
  version: "1.0"
  created: 2026-06-01
  autor: Lienzo
  based_on: workflow-construccion v5.2
invocation: relay session (separate Claude Code instances via Frontend.bat)
tags:
  - agent/lienzo
  - agent/frontend-builder
  - agent/code_adversarial
  - agent/security_adversarial
  - agent/visual_adversarial
  - agent/verifier
  - workflow/frontend
  - proyecto/faro
  - estado/activo
---

# Workflow: Frontend (v1 — Relay)

Orchestrates the construction of frontend interfaces. **Lienzo** is the Faro agent: orchestrates execution, makes design decisions, and reviews visual quality. The Frontend Builder implements. Three adversarials and a verifier validate. Lienzo reviews twice per task — once as senior guidance after the build, once as final validation after adversarial review.

> **Guiding principle 1 — Do not improvise**: every step, prompt, path, and format must be explicit. If you read this skill and think "here I need to decide how X is done" — stop and consult the user (gate). Do not improvise.
>
> **Guiding principle 2 — DESIGN.md is the governing visual authority**: if the Frontend Builder or any adversarial proposes something that contradicts DESIGN.md (colors, typography, spacing, motion, components), **DESIGN.md wins**. Lienzo detects the conflict and corrects. This is the frontend equivalent of "Spec is superior authority" in workflow-construccion.
>
> **Guiding principle 3 — Lienzo is the senior, not the adversarial**: Lienzo's two review gates are senior guidance (approve, feedback, or reject), not adversarial attack. The adversarial role belongs to the three adversarials. Lienzo guides the mid (Frontend Builder), the adversarials stress-test the output.

---

## When it activates

Lienzo launches this workflow when:
1. the user asks to build a frontend that does not exist (dashboard, UI, visual component).
2. And the task has been previously classified as trivial / standard / critical.

Lienzo **does not** launch this workflow for:
- Modifying existing frontend code → workflow-evolucion
- Backend work → workflow-construccion (Hilo's domain)
- Visual assets only (banner, diagram, social image) → direct work, no workflow
- RRSS content → eco-social skill

---

## Complexity levels

| Level | Criteria (one is enough) | Action |
|-------|--------------------------|--------|
| **trivial** | Single component <100 lines, no state management, no API integration, well-established pattern | Frontend Builder + quick verification (no formal workflow) |
| **standard** | Multiple components, integrates with existing API, no new backend, no auth changes | Full workflow with all agents |
| **critical** | Touches auth UI, data visualization, multi-page architecture, deploy to production | **Spec+Plan from Prima first**, then this workflow |

If ambiguous → Lienzo asks the user before choosing.

---

## The 4 human gates (mandatory)

Options are always presented with **full literal text**, never A/B/C labels.

### Gate F0 — Workflow load confirmation

**When**: immediately after Lienzo receives the assignment.

```
[GATE F0 — Load confirmation]
I have loaded workflow-frontend v1.

Assignment received: <1-2 sentence summary>
Classified level: <trivial | standard | critical>
Plan origin: <prior workflow-design | Lienzo template | the user provided it>
Plan path: <absolute path>
Spec path: <absolute path or "not applicable for standard">

Visual context:
- DESIGN.md: <path and status — exists/missing>
- Voice Guide: <path and status — exists/missing>
- Visual handoff: <list of approved iterations, screenshots, or "first build — no prior work">

Orchestration plan:
- Session folder: $FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>/
- Project folder: <project path>
- Agents (in order):
    1. Lienzo (Opus 4.8) — orchestrator + design authority + senior reviewer
    2. Frontend Builder (Opus 4.8) — builder
    3. Code Adversarial (Sonnet) — code review
    4. Security Adversarial (Sonnet) — security review
    5. Visual Adversarial (Sonnet) — design review against DESIGN.md
    6. Verificador (Sonnet) — functional testing
- Flow per task: BUILD → LIENZO REVIEW → PARALLEL ATTACK+TEST → LIENZO FINAL → next
- Subsequent gates: F1 (destructive), F2 (plan modification), F3 (scope change)

Options:
- "Proceed" — start with setup and dispatch.
- "Adjust X" — describe what to modify before proceeding.
- "Do not proceed" — cancel without touching anything.

What do I do?
```

### Gate F1 — Before any destructive task

Same as workflow-construccion Gate B1. Before deploying, deleting files, or modifying production.

### Gate F2 — Proposed modification of Plan

Same as workflow-construccion Gate B2. After 3 failed iterations or when a prompt contradicts the Spec/DESIGN.md.

### Gate F3 — Scope change during execution

Same as workflow-construccion Gate B3. When the user expands or modifies scope mid-workflow.

---

## System agents — Relay

### Team structure

```
join coordination room

RELAY PEERS (persistent, bidirectional via peer dispatch):
├── Lienzo (Opus 4.8) — Faro agent: orchestrates, reviews design, makes aesthetic decisions,
│                        handles architectural frontend decisions, WCAG validation
├── frontend-builder (Opus 4.8) — builder: implements components, pages, state management
├── adv-code (Sonnet) — senior dev: code patterns, performance, dead code, bundle size
├── adv-seg (Sonnet) — hacker: XSS, injection, auth bypass, data exposure
├── adversarial-visual (Sonnet) — design reviewer: DESIGN.md compliance, anti-slop, WCAG contrast
└── verificador (Sonnet) — beta tester: functional, responsive, cross-browser, user flow
```

### Agent table

| Agent | Model | Key responsibilities | CLAUDE.md |
|-------|-------|---------------------|-----------|
| **Lienzo** | Opus 4.8 | Orchestration, design authority, senior review (2 gates per task), architectural decisions, WCAG tools | Project CLAUDE.md |
| **Frontend Builder** | Opus 4.8 | Component implementation, state management, API integration, styling per DESIGN.md | `Frontend_Builder/CLAUDE.md` |
| **Code Adversarial** | Sonnet | Code quality, patterns, performance, bundle analysis, dead code | `Code_Adversarial/CLAUDE.md` |
| **Security Adversarial** | Sonnet | XSS, CSRF, auth token handling, data exposure, input sanitization | `Security_Adversarial/CLAUDE.md` |
| **Visual Adversarial** | Sonnet | DESIGN.md compliance, anti-slop, color contrast, typography hierarchy, spacing rhythm | `Visual_Adversarial/CLAUDE.md` |
| **Verificador** | Sonnet | Functional testing, responsive behavior, user flows, regression, accessibility | `Verifier/CLAUDE.md` |

### Chain of command

- **the user**: product decisions (gates, scope, UX direction).
- **Lienzo (Faro agent)**: design decisions, visual authority, architectural decisions, final approval. Prevails over all agents on aesthetic and structural matters.
- **Frontend Builder**: implementation decisions within Lienzo's brief. Reports deviations.
- **Adversarials/Verificador**: review and report. Do not decide design direction or architecture.

### What "architectural decisions" means (Lienzo's domain)

These decisions belong to Lienzo, not to the Frontend Builder. The builder implements them, not decides them:

- **Component tree**: which components exist, their hierarchy, where state lives
- **State management**: local state vs context vs Zustand store — which pattern for which data
- **Routing**: page structure, URL design, navigation flow
- **Data fetching**: where API calls happen (component, hook, store), caching strategy
- **Shared vs local styles**: what goes in design tokens vs component-scoped CSS
- **Responsive strategy**: mobile-first or desktop-first, breakpoint philosophy
- **Motion plan**: which elements animate, on what triggers, with what easing

The builder can PROPOSE alternatives if they see a better path — but Lienzo decides. If the builder disagrees strongly, they use `STATUS = DISAGREEMENT_WITH_ARCHITECTURE` in their report. Lienzo evaluates and either accepts (with reasoning) or maintains the decision (with reasoning). Both logged in `orquestacion.md`.

### DESIGN.md + Visual handoff (mandatory context)

**Both Lienzo and Frontend Builder must have DESIGN.md + visual handoff in their context at all times.** This is enforced bidirectionally:

- **In Frontend Builder's CLAUDE.md**: "Before starting any task, verify you have DESIGN.md path and visual handoff. If Lienzo did not include them in the dispatch, ASK before building."
- **In Lienzo's dispatch prompt**: always includes DESIGN.md path, Voice Guide path, and visual state of prior work.
- **In consecutive sessions**: Lienzo loads approved iterations from EcoDB (`search(tags=["status:approved", "<project>"], max_images=10)`) and includes them in the dispatch as visual handoff.

If either skips it, the other asks for it. No code touches disk without visual context.

#### Visual handoff procedure (for consecutive sessions)

When starting a session that continues prior work:

```
1. Load DESIGN.md (always — it may have been updated).
2. Search EcoDB: search shared memory
3. From results, extract:
   - Latest approved iteration per component/page (not all 50 — just the current state)
   - Any design decisions tagged with the project
4. Format as a HANDOFF BLOCK in the dispatch prompt:

   VISUAL HANDOFF:
   - Component A: approved at iter03 (screenshot: <EcoDB memory_id or file path>)
     Key decisions: dark header, 24px grid, Geist Mono for data
   - Component B: approved at iter05 (screenshot: <path>)
     Key decisions: split layout, graph on left, controls on right
   - Open issues from last session: <list or "none">

5. Include this block in EVERY dispatch to Frontend Builder.
6. Include DESIGN.md path + this block in EVERY dispatch to Visual Adversarial.
```

**Why this matters**: without visual handoff, the builder re-invents decisions from scratch. With it, the builder knows what exists, what's approved, and what the visual language is. This is the difference between continuity and "new Lienzo, who dis?"

---

## ZERO IDLE PEERS — adapted for frontend

Same principle as workflow-construccion: **no peer sits idle while completed work exists unreviewed.**

The difference is the Lienzo quick review gate between BUILD and ATTACK. This is fast (read the output, check it matches the brief, give feedback or approve) — not a deep review. The deep review comes after adversarials.

### POST-TASK FLOW (per task)

```
1. Frontend Builder completes task N
2. Lienzo QUICK REVIEW (mandatory, fast):
   - Does the output match the brief?
   - Does it look right against DESIGN.md? (visual sanity, not deep audit)
   - Any obvious structural issues?
   → APPROVE: proceed to parallel dispatch
   → FEEDBACK: specific notes back to Frontend Builder (counts as iteration)
   → REJECT: fundamental misunderstanding, re-dispatch with clarified brief
3. If approved → ATOMIC DISPATCH (all in same turn):
   peer dispatch → adv-code:          review task N code
   peer dispatch → adv-seg:           review task N security
   peer dispatch → adversarial-visual: review task N design (DESIGN.md + Voice Guide included)
   peer dispatch → verificador:       test task N
   peer dispatch → frontend-builder:  build task N+1
4. Adversarials + verificador report back
5. Lienzo FINAL REVIEW:
   - Consolidate all findings
   - Accept/reject each finding with justification
   - Run WCAG contrast check if visual changes
   → APPROVE: task N complete, move on
   → FIX: consolidated fixes back to Frontend Builder
6. If fixes → back to step 1 (max 3 iterations per task)
```

### Mandatory checklist after each task

```
Task N COMPLETED — POST-TASK DISPATCH:
  [x] Lienzo quick review done (approve/feedback/reject)
  [x] adv-code dispatched on task N
  [x] adv-seg dispatched on task N
  [x] adversarial-visual dispatched on task N (with DESIGN.md + Voice Guide)
  [x] verificador dispatched on task N
  [x] frontend-builder dispatched on task N+1
  All 5 in same message batch? YES/NO
  WCAG check run? YES/NO/NOT_APPLICABLE
```

---

## Workflow flow (step by step)

### Step 0: Lienzo validates and prepares

1. Receives assignment from the user.
2. Determines level (trivial/standard/critical). If uncertain → asks.
3. If critical and no Spec+Plan exists → escalates to Prima for workflow-design. Returns here when done.
4. Locates Plan + Spec. Validates minimum schema (same as construction).
5. **Visual context check**:
   - DESIGN.md exists and is current? If missing → `/marca` first.
   - Voice Guide exists? If missing → warn (soft block).
   - Prior approved iterations? Load from EcoDB for visual handoff.
6. Creates session folder and project report structure.
7. **Gate F0** — waits for the user's confirmation.

### Step 1: Join room and dispatch relay peers

```
join coordination room

# Dispatch Frontend Builder (Opus 4.8) — persistent builder
send message to frontend-builder

# Dispatch adversarials + verificador — await their turn
send message to adv-code
send message to adv-seg
send message to adversarial-visual
send message to verificador
```

### Step 2: Lienzo kickoff

Before dispatching the first task, Lienzo:

1. Confirms Plan meets minimum schema.
2. Searches EcoDB for prior knowledge: search shared memory
3. Pre-flight checks:
   - Node.js/npm version matches project requirements
   - Dependencies installed (`npm ls` or equivalent)
   - Dev server starts without errors
   - DESIGN.md readable and current
   - Required assets exist (fonts, images, icons)
4. Identifies destructive tasks (deploy, file deletion). Lists their numbers for Gate F1.
5. Creates task list with work delegation (same as construction — mandatory first deliverable).

### Step 3: Main loop — BUILD → REVIEW → ATTACK → DECIDE → FIX

#### BUILD PHASE

Lienzo dispatches task to Frontend Builder:

```
[TASK FOR YOU — Frontend Builder]

Session: <path>
Iteration: <M> of maximum 3

Before touching anything:
1. Read DESIGN.md: <path> — colors, typography, spacing, motion, components
2. Read visual handoff: <paths to approved screenshots/iterations or "first build">
3. Search EcoDB: search shared memory

Task to implement:
<literal task block from Plan>

Visual requirements:
- Follow DESIGN.md for all visual decisions (colors, fonts, spacing)
- If DESIGN.md does not cover a specific case, note it and use your best judgment — Lienzo will review
- Run the dev server and verify your work renders correctly before reporting

When done:
1. Verify the component/page renders without console errors
2. Take a screenshot or describe the visual result
3. Generate BUILDER_REPORT:
   - Files created/modified
   - Visual decisions made (with DESIGN.md reference or "judgment call" flag)
   - Any deviations from the brief with justification
   - Console errors: none / list
4. Return the report.

If you believe the task brief is unclear or conflicts with DESIGN.md:
- STATUS = NEEDS_CLARIFICATION
- Describe the conflict. Do NOT guess — ask Lienzo.
```

#### LIENZO QUICK REVIEW (senior gate — mandatory, cannot be skipped)

This is NOT optional and NOT "vibes." Lienzo runs this 6-point checklist on every task before dispatch. If any check fails, the task does not advance to adversarials.

```
QUICK REVIEW CHECKLIST — task N:
  [x] 1. BRIEF MATCH: output implements what the task asked for (not more, not less)
  [x] 2. DESIGN.MD SPOT CHECK: pick 3 visual tokens (a color, a font size, a spacing value)
         and verify they match DESIGN.md. If any mismatch → FEEDBACK.
  [x] 3. RENDERS CLEAN: open in browser or read builder's screenshot. No broken layout,
         no missing assets, no console errors.
  [x] 4. ARCHITECTURE: component structure makes sense for future tasks. No god components,
         no state in the wrong place, no prop drilling when context exists.
  [x] 5. JUDGMENT CALLS: if builder flagged any "judgment call" decisions, validate each one.
         Accept with reasoning or correct with DESIGN.md reference.
  [x] 6. DEPENDENCY CHECK: does task N+1 depend on task N's output? If yes, mark it.
         Adversarial CRITICALs on task N will block task N+1 fixes.
```

Outcomes:
- **APPROVE** → proceed to parallel dispatch. Log checklist result in `orquestacion.md`.
- **FEEDBACK** → specific notes back to Frontend Builder. Counts as an iteration. "Change the card spacing from 16px to 24px per DESIGN.md §spacing" — not vague, not subjective. Reference the source.
- **REJECT** → fundamental misunderstanding of the brief. Re-dispatch with clarified instructions. Rare — if this happens twice, the brief is the problem, not the builder.

**Enforcement**: if Lienzo dispatches adversarials without logging the quick review checklist in `orquestacion.md`, the workflow is in violation. The checklist IS the proof that the review happened.

#### PARALLEL ATTACK + TEST (all dispatched in same turn)

```
# ALL FIVE IN THE SAME TURN — atomic
peer dispatch → adv-code:           "Review task N. Files: <list of files touched>. Focus: component patterns,
                                  performance, bundle impact, dead code."
peer dispatch → adv-seg:            "Review task N. Files: <list of files touched>. Focus: XSS, input sanitization,
                                  auth token handling, data exposure."
peer dispatch → adversarial-visual: "Review task N. Files: <list of files touched>.
                                  DESIGN.md: <absolute path>. Voice Guide: <absolute path>.
                                  Focus: color compliance, typography hierarchy, spacing rhythm, anti-slop,
                                  WCAG contrast."
peer dispatch → verificador:        "Test task N at <dev server URL or file path>.
                                  Checks: 1. [component renders at <URL>] 2. [responsive at 375/768/1440]
                                  3. [user flow: <specific steps>] 4. [no console errors] 5. [a11y basics]"
peer dispatch → frontend-builder:   "Build task N+1: <next task>"
                                  (ONLY if task N+1 does NOT depend on task N — see dependency check below)
```

#### TASK DEPENDENCY HANDLING

If Lienzo's quick review checklist item #6 identified that task N+1 depends on task N:

- **Do NOT dispatch task N+1 until adversarials report on task N.**
- Frontend Builder waits. This is the ONE exception to ZERO IDLE PEERS — a builder building on top of a potentially broken foundation wastes more time than waiting.
- Once task N is APPROVED by Lienzo final review → dispatch task N+1 immediately.
- If task N needs FIXES → fix first, re-review, then dispatch N+1.

Log the dependency hold in `orquestacion.md`: `"Task N+1 held — depends on task N. Builder idle until N approved."`

#### LIENZO FINAL REVIEW (consolidation + validation)

After all adversarials and verificador report:

1. Read all reports
2. For each finding:
   - **ACCEPT** → include in fix list for Frontend Builder
   - **REJECT with justification** → "The adversarial says use 14px body text, but DESIGN.md specifies 16px. DESIGN.md wins."
   - **DEFER as debt** → acceptable but not blocking
3. Run WCAG contrast check: `node scripts/check-contrast.mjs <url>`
4. Consolidated verdict:
   - **APPROVE** → task N complete
   - **FIX** → send consolidated fix list to Frontend Builder

**Handling contradictions between adversarials**: if adv-code and adversarial-visual disagree (e.g., adv-code says "extract to utility class", adversarial-visual says "needs unique spacing"), Lienzo decides. The rule: **DESIGN.md wins on visual matters, code patterns win on architecture matters.** If the contradiction is genuinely at the boundary, Lienzo picks one, documents the reasoning in `orquestacion.md`, and moves on. Do not loop trying to satisfy both.

If FIX → Lienzo sends consolidated fix list to Frontend Builder with the re-iteration prompt:

```
[FIXES FOR YOU — Frontend Builder, iteration <M+1>]

Previous iteration: FIXES REQUIRED
Consolidated findings to resolve (ONLY these — do not touch anything else):

<for each accepted finding:>
  [FINDING_ID] <source: adv-code | adv-seg | adversarial-visual | verificador>
  <description of the problem>
  <specific fix instruction>
  <DESIGN.md reference if visual>

Files you may touch: <explicit list — same as task N archivos_a_tocar>

Do NOT:
- Fix warnings, nits, or deferred findings (those go to debt backlog)
- Refactor beyond the fix scope
- Touch files not in the list above

When done: same BUILDER_REPORT format. Run dev server and verify the fix renders correctly.
```

Back to Lienzo quick review → iterate. Max 3 iterations per task. On 3rd failure → Gate F2.

#### NEEDS_CLARIFICATION HANDLING

If Frontend Builder responds with `STATUS = NEEDS_CLARIFICATION`:

1. Lienzo reads the conflict description.
2. If Lienzo can resolve (DESIGN.md interpretation, brief ambiguity) → respond directly with the clarification + updated brief.
3. If Lienzo cannot resolve (product decision, UX direction) → escalate to the user immediately. Do not guess.
4. Clarification does NOT count as an iteration — the builder hasn't built anything yet.
5. After clarification, re-dispatch the same task with the updated brief.

#### CLOSE PHASE — Production Readiness

When Lienzo determines the build is complete, run this checklist BEFORE declaring done:

```
PRODUCTION READINESS — <project>:
  VISUAL INTEGRITY:
  [ ] 1. Open every page/route in browser at 1440px. Screenshot each one.
  [ ] 2. Compare each screenshot against DESIGN.md: colors, typography, spacing, motion.
  [ ] 3. Check visual consistency ACROSS pages (not just each page in isolation).
         Same header, same nav, same footer, same spacing rhythm, same color balance.
  [ ] 4. Verify no orphaned styles (components from earlier tasks broken by later tasks).

  WCAG:
  [ ] 5. Run `node scripts/check-contrast.mjs <url>` on every page. All PASS.
  [ ] 6. Keyboard navigation: Tab through every interactive element. Focus visible? Order logical?

  RESPONSIVE:
  [ ] 7. Check 375px (mobile), 768px (tablet), 1440px (desktop) on at least the main page.
  [ ] 8. No horizontal scrollbar at any breakpoint.

  FUNCTIONAL:
  [ ] 9. Run test suite (if exists). All pass.
  [ ] 10. No console errors or warnings on any page.
  [ ] 11. All API integrations return data (not mocked, unless Plan explicitly allows mocks).

  CLEAN:
  [ ] 12. No TODO/FIXME/HACK comments left in code.
  [ ] 13. No console.logs left.
  [ ] 14. No unused imports or dead components.
```

If any item fails → fix before closing. If the fix is trivial (< 5 min) → Lienzo fixes directly. If non-trivial → dispatch to Frontend Builder as a final fix task.

Only after all 14 checks pass → proceed to closure documentation.

---

## Initial setup — file structure

### Session folder

```
$FARO_ROOT/Sesiones/<YYYY-MM-DD>_<project>/
  ├── orquestacion.md         ← append-only Lienzo log
  ├── retrospectiva.md        ← what worked, what didn't, pain metrics
  └── backlog_deuda.md        ← documented debt items
```

### Project reports

```
<project_path>/.faro/
  └── reportes/
        ├── lienzo_kickoff.md
        ├── builder_task_<N>_iter_<M>.md
        ├── adversarial_visual_task_<N>.md
        ├── adversarial_code_task_<N>.md
        ├── adversarial_security_task_<N>.md
        ├── verifier_task_<N>.md
        └── lienzo_close.md
```

---

## Closure — 5 mandatory documents

When the workflow ends (completed or aborted), Lienzo produces all 5 before closing:

### 1. Orchestration log (`orquestacion.md`)

Append-only timeline of the session. What was dispatched, when, to whom. Decisions taken. Gates fired.

### 2. Retrospective (`retrospectiva.md`)

```markdown
# Retrospective workflow-frontend — <project> — <date>

## What worked

## What didn't work

## Pain metrics
- Tasks passing on first Lienzo review: N/M
- Adversarial findings accepted vs rejected: N/M
- WCAG failures caught: N
- Gates fired: [list]
- Total iterations: N
- Duration: Xh

## For v+1
```

### 3. Debt backlog (`backlog_deuda.md`)

Items deferred during the workflow. Each with task reference, description, and severity.

### 4. Construction report (`Faro/Informes/Construcción/<date>_<project>.md`)

```yaml
---
workflow: frontend
version_workflow: "1.0"
date: YYYY-MM-DD
project: <human name>
project_slug: <slug>
faro_agent: Lienzo
faro_session: $FARO_ROOT/Sesiones/<session>/
prior_report_consumed: "<link to Spec+Plan or null>"
level: standard | critical
tasks_completed: N/M
tasks_approved: N
tasks_approved_with_debt: N
tasks_rejected: 0
design_md_version: <hash or date of DESIGN.md used>
wcag_status: PASS | PARTIAL | NOT_CHECKED
next_workflow_suggested: evolucion | none
faro_artifacts:
  code_deployed: <project_path>
  tests_passing: <list>
  debt_backlog: <session_path>/backlog_deuda.md
  retrospective: <session_path>/retrospectiva.md
tags: [workflow/frontend, status/deployed, project/<slug>]
---

# Construction Report — <project>

## What was built
## How to run
## Where it lives
## Systems it touches
## Tasks completed (table)
## Team and roles
## Adversarial findings (summary by severity)
## WCAG validation results
## Visual decisions made (with DESIGN.md references)
## Traceability (links to Spec, Plan, DESIGN.md, EcoDB memories)
```

### 5. EcoDB memories

Save learnings to EcoDB with `agent_identifier="Lienzo"`:
- One memory per significant learning (not one giant dump)
- Tag with project name + `workflow/frontend`
- If approved visual iterations exist, save screenshots with `file_path`

---

## Anti-stuck protocols

### Anti-stuck — Frontend Builder

If the builder responds without structured output:
> *"Your report does not meet BUILDER_REPORT format. Include: files modified, visual decisions with DESIGN.md reference, console errors, screenshot or description. No approval without structured report."*

If the builder ignores DESIGN.md:
> *"You did not reference DESIGN.md in your visual decisions. Read <path> and verify your implementation matches. Report which sections you followed."*

### Anti-stuck — Visual Adversarial

If visual adversarial returns 0 findings:
> *"New frontend code always has visual findings. Check: color values match DESIGN.md tokens? Typography scale correct? Spacing rhythm consistent? Anti-slop (no generic card grids, no gratuitous gradients)? WCAG contrast? Return at least 3 findings."*

### Anti-stuck — Code Adversarial

If adv-code returns 0 findings:
> *"New frontend code always has code findings. Check: component size (<200 lines?), prop types, re-render triggers, CSS specificity, dead imports, error boundaries, loading/error states. Return at least 3 findings."*

### Anti-stuck — Security Adversarial

If adv-seg returns 0 findings:
> *"Frontend code always has a security surface. Check: user input rendered without sanitization? Auth tokens in localStorage? Sensitive data in React state (visible in DevTools)? API keys in client bundle? Form action targets? Return at least 3 findings."*

### Anti-stuck — Lienzo (self)

If Lienzo has been reviewing for more than 2 iterations without clear direction:
> Stop. Tell the user where you're stuck. Two heads think better than one.

### Anti-stuck — General (pipeline stall)

If any peer has not responded in 5+ minutes and has received a dispatch:
> Check if the peer is alive (peer discovery). If offline → re-dispatch. If online but silent → send a nudge: *"Status check — are you working on the task I sent? Reply with current progress or blockers."*

---

## Frontend-specific review criteria

### Visual Adversarial must check

- Color values match DESIGN.md tokens (exact OKLCH values, not "close enough")
- Typography: correct font families, weights, sizes per hierarchy
- Spacing: rhythm follows DESIGN.md grid/spacing system
- Anti-slop: no generic card grids, no gratuitous gradients, no emoji icons, no left-border accents
- WCAG contrast: body text ≥ 4.5:1, headings ≥ 3:1
- Motion: follows DESIGN.md motion spec (easing, duration, triggers)
- Voice Guide compliance: copy matches tone, no anti-pattern phrases

### Code Adversarial must check

- Component architecture (proper separation, no god components)
- State management patterns (appropriate for complexity)
- Performance (unnecessary re-renders, bundle impact, image optimization)
- CSS specificity wars, !important abuse, inline styles vs design tokens
- Accessibility: semantic HTML, ARIA labels, keyboard navigation
- Dead code, unused imports, console.logs left behind

### Security Adversarial must check

- XSS: innerHTML, dangerouslySetInnerHTML, user input rendering
- Auth token handling: storage (httpOnly cookies vs localStorage), transmission
- Data exposure: sensitive data in client state, console, network tab
- Input sanitization: forms, URL parameters, query strings
- CORS configuration if applicable
- CSP headers if applicable

### Verificador must check

- Functional: components render, interactions work, state updates correctly
- Responsive: 375px (mobile), 768px (tablet), 1440px (desktop) minimum
- Cross-browser: if specified in Plan
- User flows: complete happy path + key error states
- Accessibility: screen reader basics, keyboard navigation, focus management
- No console errors or warnings

---

## Cost and performance (reference)

| Level | Estimated duration | Estimated tokens |
|-------|-------------------|------------------|
| trivial | <15 min | <30k |
| standard | 30-90 min | 100-200k |
| critical (with prior Spec+Plan) | 2-4h execution | 300-600k |

---

## Healthy metrics

| Ratio | Target |
|-------|--------|
| Tasks passing Lienzo quick review on iteration 1 | >70% |
| Tasks passing all adversarials on iteration 1 | >50% |
| Visual adversarial findings accepted by Lienzo | >60% |
| WCAG failures caught before delivery | 100% |
| Gate F2 fired / total tasks | <5% |

---

## When NOT to use this workflow

- Backend work → workflow-construccion
- Modifying existing frontend → workflow-evolucion
- Visual assets only (banner, diagram) → direct Lienzo work
- RRSS content → eco-social skill
- Design system creation → `/marca` command
- Isolated CSS fix → direct fix, no workflow

---

## Version history

- **v1.0 (2026-06-01)**: first version, adapted from workflow-construccion v5.2. Key differences: Lienzo as Faro agent (orchestrator + design authority), Frontend Builder as executor, Visual Adversarial as new parallel reviewer, DESIGN.md as governing visual authority, two Lienzo review gates (quick review + final validation), WCAG validation integrated, visual handoff protocol for consecutive sessions.
