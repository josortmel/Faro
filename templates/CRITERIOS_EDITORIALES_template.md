---
name: Criterios editoriales
type: plantilla
produces: criterios_editoriales
used_by_workflows:
  - periodico
filled_by: Editor
version: "1.0"
tags:
  - plantilla/criterios
  - workflow/periodico
  - agente/editor
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_periodico.md
  final_output: $FARO_ROOT/Sesiones/<sesion>/CRITERIOS.md
---

# CRITERIOS EDITORIALES — snapshot del día

> **Source of truth**: los criterios editoriales de the user viven en `$FARO_ROOT/Agentes\CLAUDE_md_Editor.md`.
> Esta plantilla es un **snapshot** que Faro copia al inicio del workflow-periodico para referencia rápida de los agentes sin tener que releer el CLAUDE.md completo.
> Si the user cambia los criterios, se actualizan en el CLAUDE.md, no aquí — Faro regenera el snapshot al inicio de cada workflow.

## Metadatos del snapshot
- **Fecha de generación**: <YYYY-MM-DD>
- **Hash del CLAUDE_md_Editor.md**: <sha256 abreviado — para detectar si cambió>

---

## Los 3 criterios sagrados (principio rector 4 del workflow)

El Editor **no puede publicar** un periódico que viole alguno de estos 3 criterios. Tras 2 intentos fallidos, Faro escala a the user (Bisagra 1).

### Criterio 1: Perspectivas de ≥3 regiones geográficas distintas
El periódico debe cubrir al menos 3 regiones del mundo. Regiones válidas: ES, EU, US, LATAM, ASIA_CENTRAL, ASIA_ESTE, AFRICA, ORIENTE_MEDIO.

Un periódico con noticias solo de ES y US es **insuficiente** (2 regiones).

### Criterio 2: ≥1 noticia fuera del mainstream
Principio editorial de the user: **contra el filtro burbuja**. Al menos una noticia de cada edición debe venir de una fuente que no sea mainstream occidental.

Fuentes mainstream típicas: CNN, BBC, NYT, Reuters-Occidente, El País, WSJ.
Fuentes que califican como "fuera mainstream": Al Jazeera, TASS, Xinhua, The Conversation, Rest of World, Reuters-Asia, medios locales no-occidentales, publicaciones científicas primarias, blogs técnicos de ingeniería con autor verificable.

### Criterio 3: Cada noticia con fuente verificable
Ninguna noticia entra al periódico sin link a fuente accesible. Si el Crítico no puede verificar la fuente primaria → la noticia no se publica (o se publica con fiabilidad NO_VERIFICABLE y degradación visual del Maquetador).

---

## Las 6 secciones fijas

1. **Lo que no verás en el telediario** — noticias internacionales importantes que los medios mainstream occidentales no cubren
2. **Ciencia** — papers, descubrimientos, publicaciones primarias
3. **Empresas y tecnología** — lanzamientos, rondas, innovación (con énfasis fuera Silicon Valley cuando se pida)
4. **Mercados** — índices, movimientos, 2-3 acciones destacadas
5. **Política y elecciones** — procesos democráticos, regulación, geopolítica
6. **Historia larga** — 1 tema de los 5 anteriores tratado en profundidad (3-5 párrafos)

---

## Reglas adicionales (preservadas de CLAUDE_md_Editor.md)

- **No rankear prominentemente noticias cuya fuente parezca dudosa**: el Editor anticipa lo que el Crítico detectará (principio rector 2 — Crítico > Editor en fiabilidad).
- **Sintetizar preservando lo importante, no resumir a muerte**: las noticias largas merecen espacio si tienen textura relevante.
- **Cross-referenciar noticias relacionadas** entre secciones para que el Analista pueda trabajar sobre relaciones cruzadas.
- **Descartar con razón**: si el Editor descarta una noticia del pool, anotar razón en `descartadas[].razon` del JSON editado.
