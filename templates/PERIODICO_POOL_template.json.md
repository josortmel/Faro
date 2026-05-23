---
name: Pool de noticias (JSON)
type: plantilla
produces: pool_noticias
used_by_workflows:
  - periodico
filled_by: Investigador de Noticias
version: "1.0"
tags:
  - plantilla/periodico
  - workflow/periodico
  - agente/investigador_de_noticias
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_periodico.md
  final_output: $FARO_ROOT/Sesiones/<sesion>/pool_noticias.json
---

Companion metadata for [[PERIODICO_POOL_template.json]]
