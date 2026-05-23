---
name: Contrato de sesión (construcción)
type: plantilla
produces: contract
used_by_workflows:
  - construccion
  - evolucion
filled_by: Faro (orquestador)
version: "1.0"
tags:
  - plantilla/contract
  - workflow/construccion
  - agente/faro
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_construccion.md
  final_output: $FARO_ROOT/Sesiones/<sesion>/CONTRACT.md
---

# CONTRACT — Sesión <YYYY-MM-DD>_<proyecto>

Define los entregables exactos por agente. Cada agente lee este archivo antes de empezar.

---

## Supervisor

### Input que recibe (de Faro)
- CLAUDE_md_Supervisor.md inyectado
- Encargo con: rutas de Plan, Spec, ENVIRONMENT, CONTRACT, LESSONS
- Nivel (standard | critical)

### Output garantizado: KICKOFF_REPORT

```
KICKOFF_STATUS: OK | BLOCKED
PLAN_VALIDADO: true | false (si false, listar campos faltantes por task)
PRE_FLIGHT_CHECKS:
  - python_version: <salida real> | esperado: <de ENVIRONMENT.md> | OK | FAIL
  - dependencias_clave: [<lib>: OK | FAIL]
  - servicios: [<servicio>: UP | DOWN | N/A]
  - rutas_existen: [<ruta>: OK | FAIL]
TASKS_DESTRUCTIVAS: [<numeros de task que dispararán Bisagra 1>]
ECO_MEMORY_LECCIONES_RELEVANTES: [<resumen breve por lección encontrada>] | "ninguna"
ECO_GRAPH_DEPENDENCIAS: [<tripletas relevantes>] | "ninguna"
BLOCKING_QUESTIONS: [] | [pregunta concreta para the user]
NEXT_ACTION: "Despachar Ejecutor con Task 1"
```

### Output por iteración (despacho/recepción)
Después de cada VERIFICADOR_REPORT, el Supervisor decide y reporta:
```
DECISION_SUPERVISOR:
  task: <N>
  iteracion: <M>
  verdict_recibido: <APPROVE | REQUEST_CHANGES | REJECT>
  accion: <"siguiente_task" | "redespachar_ejecutor" | "bisagra_2" | "escalar">
```

---

## Ejecutor

### Input que recibe (de Faro, despachado por Supervisor)
- CLAUDE_md_Ejecutor.md inyectado
- Una task del Plan (literal)
- Iteración M
- En iteración 1: la task completa
- En iteración M>1: solo `required_fixes` de la iteración previa

### Output garantizado: EJECUTOR_REPORT
Guardado en: `<proyecto>/.faro/reportes/ejecutor_task_<N>_iter_<M>.md`

```
STATUS: OK | NEEDS_VERIFIER | DISAGREEMENT_WITH_PLAN
TASK: <N>
ITERACION: <M>
ARCHIVOS_MODIFICADOS:
  - <ruta>: <lineas_antes> -> <lineas_despues>
ACCIONES_EJECUTADAS:
  - <comando o cambio literal>
TESTS_OUTPUT:
  - <comando>: <output literal>
POST_CONDICIONES_VERIFICADAS:
  - <condicion>: <comando usado> -> <resultado>
LESSONS_NUEVAS: [<texto de lección a añadir a LESSONS.md>] | "ninguna"
DISAGREEMENT: <solo si STATUS == DISAGREEMENT_WITH_PLAN>
  - descripcion: <conflicto detectado>
  - propuesta: <qué creo que debería decir el Plan>
```

---

## Verificador (CIEGO)

### Input que recibe (de Faro, despachado por Supervisor)
- CLAUDE_md_Verificador.md inyectado
- Solo: objetivo, post_condiciones, tests, criterio_de_exito, archivos_a_tocar de la task
- ENVIRONMENT.md
- Acceso al código actual

**NO recibe**: EJECUTOR_REPORT, iteraciones previas, resto del Plan, LESSONS.md.

### Output garantizado: VERIFICADOR_REPORT
Guardado en: `<proyecto>/.faro/reportes/verificador_task_<N>_iter_<M>.md`

Formato dual — markdown-INI legible + JSON estricto:

```
REVIEW_SUMMARY: <1-2 frases del veredicto>
VERDICT: APPROVE | APPROVE_WITH_DEBT | REQUEST_CHANGES | REJECT

BLOCKERS:
  B1 [critical] <archivo>:<linea> — <descripción>
WARNINGS:
  W1 [medium] <archivo>:<linea> — <descripción> | impact_analysis: {files_that_need_update: []}
NITS:
  N1 [low] <archivo>:<linea> — <descripción>
DEBT_ITEMS: (solo cuando verdict = APPROVE_WITH_DEBT)
  D1 [medium] <archivo>:<linea> — <descripción> | triggers_revision: <condición para revisitar>

COVERAGE:
  - <criterio_de_exito 1>: <pass | fail | partial> — evidence: "<comando + output>"
  - <criterio_de_exito 2>: <...>

SPEC_DRIFT: [<diferencias respecto a objetivo del Plan>] | "ninguna"
ASSERTS_FRAGILES: [<asserts que pasarían aunque el código estuviera roto>] | "ninguno"
```

```json
{
  "verdict": "APPROVE | APPROVE_WITH_DEBT | REQUEST_CHANGES | REJECT",
  "summary": "...",
  "required_fixes": ["B1"],
  "blockers": [{"id": "B1", "severity": "critical", "location": "archivo.py:42", "message": "..."}],
  "warnings": [{"id": "W1", "severity": "medium", "location": "...", "message": "...", "impact_analysis": {"files_that_need_update": []}}],
  "nits": [{"id": "N1", "severity": "low", "location": "...", "message": "..."}],
  "debt_items": [{"id": "D1", "severity": "medium", "location": "...", "message": "...", "triggers_revision": "..."}],
  "coverage": [{"criterio": "...", "estado": "pass|fail|partial", "evidence": "..."}],
  "spec_drift": [],
  "asserts_fragiles": []
}
```

**Invariantes duras** (actualizadas v3):
- `required_fixes` vacío Y `debt_items` vacío → `verdict = APPROVE`.
- `required_fixes` vacío Y `debt_items` no vacío → `verdict = APPROVE_WITH_DEBT`.
- `verdict = REQUEST_CHANGES` → `required_fixes` tiene al menos un id.
- `debt_items` nunca coexiste con `REQUEST_CHANGES` o `REJECT` (si algo bloquea, va en blockers).

---

## Escribano

### Input que recibe (de Faro)
- CLAUDE_md_Escribano.md inyectado
- Estado final del workflow (COMPLETADO / ABORTADO_EN_TASK_N / MODIFICADO_TRAS_BISAGRA_2)
- Acceso a todos los reportes en `.faro/reportes/`
- Acceso a Obsidian, eco_memory, eco_graph

### Output garantizado: ESCRIBANO_REPORT
```
DOCUMENTACION_STATUS: OK | PARTIAL
OBSIDIAN_FILE: <ruta>
ECO_MEMORY_RECUERDO_ID: <id>
ECO_GRAPH_TRIPLETAS_AÑADIDAS: <numero>
TELEMETRIA:
  duracion_total_min: <N>
  tasks_completadas: <N>/<M>
  iteraciones_totales: <N>
  bugs_detectados_verificador: <N>
  disagreements_ejecutor: <N>
  bisagras_disparadas: [B0, B1_x_N, B2_x_M]
```
