---
name: Contrato de sesión (diseño)
type: plantilla
produces: contract
used_by_workflows:
  - diseno
filled_by: Faro (orquestador)
version: "1.0"
tags:
  - plantilla/contract
  - workflow/disenio
  - agente/faro
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_diseno.md
  final_output: $FARO_ROOT/Sesiones/<sesion>/CONTRACT.md
---

# CONTRACT — Sesión <YYYY-MM-DD>_<proyecto>_diseno

Define los entregables exactos por agente en workflow-diseño v2. Cada agente lee este archivo antes de empezar.

---

## Arquitecto

### Paso 1 — Brief de preguntas
**Output**:
```
BRIEF_PREGUNTAS:
Q1: <pregunta>
...
CONTEXTO_TECNICO: <2-3 frases>
ECO_MEMORY_LECCIONES_RELEVANTES: <lista o "ninguna">
ECO_GRAPH_DEPENDENCIAS: <lista o "ninguna">
```

### Paso 3 — Brief v1 (crudo)
**Output**: archivo en `<proyecto>/refactor_v<N>_brief.md` cumpliendo BRIEF_template (6 secciones obligatorias) + pre-commitment.

### Paso 5 — Cierre Loop 1
**Output**:
```
CIERRE_LOOP1:
APPLIED_FIXES: [...]
DEFERRED_AS_DEBT: [...]
ESCALATED_TO_USER: [...]
METRICAS_LOOP1: {observaciones_totales, applied, deferred, escalated}
BRIEF_V2_PATH: <ruta>
```
Guardado en: `<proyecto>/.faro/reportes_diseno/arquitecto_cierre_loop1.md`

### Paso 6 — verification_checkpoint (solo critical)
**Output**: archivo en `<proyecto>/verification_checkpoint.md` cumpliendo template (3 secciones).

### Paso 7 — Spec + Plan (solo critical)
**Output**:
- `<proyecto>/refactor_v<N>_spec.md` cumpliendo SPEC_template (7 secciones)
- `<proyecto>/refactor_v<N>_plan.md` cumpliendo PLAN_template (9 campos por task)
- Pre-commitment

### Paso 9 — Cierre Loop 2 (solo critical)
**Output**: igual que Paso 5 pero para Loop 2. Guardado en `<proyecto>/.faro/reportes_diseno/arquitecto_cierre_loop2.md`.

---

## Investigador

### Paso 2 — Research
**Output**:
```
INVESTIGACION_STATUS: OK | PARTIAL | BLOCKED
HALLAZGOS_CLAVE:
  H1: <hallazgo>
    Fuente primaria: <URL + fecha>
    Fuente confirmatoria: <URL + fecha, o "única fuente">
    Aplica a preguntas: [Q1, Q3]
BLOCKING_QUESTIONS: [] | [preguntas para the user]
NEXT_ACTION: "..."
```
Guardado en: `<proyecto>/.faro/reportes_diseno/investigador_report.md`

---

## Cuestionador (Loop 1)

### Paso 4 — Ataque al Brief
**Output dual**: markdown-INI + JSON.

Markdown-INI:
```
REVIEW_SUMMARY: <...>
VERDICT: APPROVE | REQUEST_CHANGES | NEEDS_REDESIGN

ATAQUES_DIRECTOS: [A1, A2, ...]
CONTRADICCIONES: [C1, ...]
SUPUESTOS_IMPLICITOS: [S1, ...]
LAGUNAS: [L1, ...]
CROSS_REF_RESEARCH: [lista o "sin conflictos"]

REQUIRED_CLARIFICATIONS: [ids]
SOFT_OBJECTIONS: [ids]
```

JSON:
```json
{
  "verdict": "APPROVE | REQUEST_CHANGES | NEEDS_REDESIGN",
  "summary": "...",
  "required_clarifications": ["A1", "C1"],
  "soft_objections": ["S1", "L1"],
  "cross_ref_research_conflicts": [
    {"brief_claim": "...", "research_finding": "...", "severity": "BLOCKER"}
  ]
}
```

**Reglas de consistencia**:
- `required_clarifications` vacío Y `soft_objections` vacío → `verdict = APPROVE`.
- `cross_ref_research_conflicts` con BLOCKER → `verdict = NEEDS_REDESIGN` automático.

Guardado en: `<proyecto>/.faro/reportes_diseno/cuestionador_report.md`

---

## CuestionadorSpec (Loop 2, solo critical)

### Paso 8 — Ataque a Spec + Plan
**Output dual**: markdown-INI + JSON, con 4 tipos de defectos: GAPS_BRIEF_SPEC, SPEC_DEFECTOS, PLAN_DEFECTOS, COHERENCIA + CROSS_REF_REALIDAD (contra verification_checkpoint).

Guardado en: `<proyecto>/.faro/reportes_diseno/cuestionador_spec_report.md`

---

## Escribano

### Paso final — Documentación + memoria
**Outputs (3 lugares obligatorios)**:
1. Obsidian: `$FARO_ROOT/Informes/Diseño/<Proyecto>_<YYYY-MM-DD>.md`
2. eco_memory: 1-2 recuerdos con autor "Escribano" (content < 500 palabras cada uno)
3. eco_graph: tripletas mínimas con origen y autor

**Reporte final a Faro**:
```
DOCUMENTACION_STATUS: OK | PARTIAL
OBSIDIAN_FILE: <ruta>
ECO_MEMORY_RECUERDO_IDS: [...]
ECO_GRAPH_TRIPLETAS_AÑADIDAS: N
TELEMETRIA: {duracion_loops, observaciones_totales, applied/deferred/escalated por loop}
```
