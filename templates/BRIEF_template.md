---
name: Brief de diseño
type: plantilla
produces: brief
used_by_workflows:
  - diseno
filled_by: Arquitecto
version: "1.0"
tags:
  - plantilla/brief
  - workflow/disenio
  - agente/arquitecto
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_diseno.md
  final_output: $FARO_ROOT/Informes/Diseño/<YYYY-MM-DD>_<slug>.md
---

# Brief — <Nombre del refactor/feature>

> Plantilla obligatoria para Briefs producidos por el Arquitecto en workflow-diseño v2.
> Las 6 secciones son obligatorias. El Cuestionador rechaza el Brief si falta alguna.

## Metadatos
- **Proyecto**: <ruta absoluta>
- **Fecha**: <YYYY-MM-DD>
- **Versión**: v<N>
- **Nivel**: standard | critical
- **Encargo de the user (literal)**: <copia textual del mensaje original>

---

## 1. Contexto y motivación

- **Qué problema resuelve**: <1-3 frases>
- **Por qué ahora**: <1-2 frases>
- **Usuarios afectados**: <Eco, the user, Prima, Faro, usuarios finales, etc.>

## 2. Decisiones de diseño (con trazabilidad)

Cada decisión lleva etiqueta de origen:
- `[research]` — viene del Investigador, con URL de fuente
- `[user-brief]` — viene literal de the user
- `[my-inference]` — inferencia del Arquitecto basada en contexto conocido

**Regla dura**: si no puedes etiquetar una decisión, no la pongas — es señal de que te la estás inventando.

### Formato por decisión:

- **D1**: <decisión>
  - Origen: [research | user-brief | my-inference]
  - Razón: <1-2 frases>
  - Trade-off consciente: <qué se sacrifica>
  - Alternativas descartadas: <lista corta con razón de descarte>
  - Fuente (si research): <URL + fecha>

- **D2**: ...

---

## 3. Scope

### Dentro del scope (lista explícita)
- <item 1>
- <item 2>

### Fuera del scope (deuda consciente)
- <item excluido>: razón de exclusión
- <item 2>: razón

---

## 4. Criterios de éxito (verificables)

Bullets operacionales, **no** "funciona bien". Cada criterio debe ser verificable con comando/query concreto.

- <criterio 1>: verificable con `<comando o query>`
- <criterio 2>: verificable con `<comando o query>`
- <criterio 3>: verificable con `<comando o query>`

---

## 5. Deuda explícita

Lista de items que quedan conscientemente sin resolver y por qué:

- **DD1**: <qué queda pendiente> — justificación: <por qué no ahora>
  - Trigger de revisión: <cuándo volver a mirar esto>
- **DD2**: ...

---

## 6. Preguntas que el Cuestionador debería preguntar

El Arquitecto anticipa sus propios puntos débiles aquí. **NO los responde** — eso es turno del Cuestionador. Solo los enumera honestamente.

- ¿<pregunta>?
- ¿<pregunta>?
- ¿<pregunta>?

---

## Referencias

- Reporte del Investigador: `<ruta>`
- eco_memory consultadas: `<tags>`
- eco_graph consultado: `<sujetos>`
