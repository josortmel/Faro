---
name: Plan de ejecución
type: plantilla
produces: plan
used_by_workflows:
  - diseno
filled_by: Arquitecto
version: "1.0"
tags:
  - plantilla/plan
  - workflow/disenio
  - agente/arquitecto
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_diseno.md
  final_output: <proyecto>/refactor_v<N>_plan.md
---

# Plan — <NOMBRE_PROYECTO>

> Plantilla para tareas **standard** sin workflow-diseño previo.
> Para **critical**, el Plan lo produce workflow-diseño y debe cumplir este mismo esquema.
> Faro valida el esquema antes de despachar al Supervisor — si falta algún campo, **se para**.

## Metadatos

- **Proyecto**: <ruta absoluta del proyecto>
- **Encargo de the user**: <copia literal del mensaje original>
- **Nivel**: standard
- **Origen del Plan**: <"Faro genera desde template" | "the user lo pasó">
- **Fecha**: <YYYY-MM-DD>
- **Spec asociado**: <ruta o "no aplica para standard">

## Resumen del trabajo

<2-4 frases — qué se va a construir, no cómo>

## Tasks

### Task 1: <título corto, imperativo>

- **objetivo**: <1-2 frases — qué se consigue al completarla>
- **archivos_a_tocar**:
  - <ruta absoluta>
  - <ruta absoluta>
- **accion**: |
  <código literal, SQL, comando, o pseudocódigo si la implementación admite variantes>
- **pre_condiciones**:
  - <estado verificable del sistema antes>
- **post_condiciones**:
  - <estado verificable del sistema después>
- **tests**:
  - `<comando exacto>` → debe devolver `<output esperado>`
  - `<comando exacto>` → debe devolver `<output esperado>`
- **criterio_de_exito**:
  - <bullet verificable, no "funciona bien">
  - <bullet verificable>
- **rollback**: `<comando exacto>` | `no_destructiva`
- **depende_de**: [] | [Task N, Task M]

### Task 2: <título>

<misma estructura>

### Task N: <título>

<misma estructura>

---

## Notas

- Tasks marcadas como destructivas (rollback != "no_destructiva") dispararán **Bisagra 1** antes de ejecutarse.
- Si una task agota 3 iteraciones Ejecutor↔Verificador, el Supervisor disparará **Bisagra 2** con propuesta de modificación.
- Los tests deben ser ejecutables tal cual (rutas absolutas, sin variables sin resolver).
