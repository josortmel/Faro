---
name: Snapshot del ecosistema
type: plantilla
produces: ecosystem
used_by_workflows:
  - adaptacion
filled_by: Faro (orquestador)
version: "1.0"
tags:
  - plantilla/ecosystem
  - workflow/adaptacion
  - agente/faro
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_adaptacion.md
  final_output: $FARO_ROOT/Sesiones/<sesion>/ECOSYSTEM.md
---

# ECOSYSTEM — contexto interno del ecosistema (snapshot)

> Plantilla para el archivo que el Diseñador-Conector lee al inicio de workflow-adaptacion v2.
> Faro lo genera consultando el estado real del ecosistema al arrancar el workflow.

## Metadatos
- **Fecha snapshot**: <YYYY-MM-DD HH:MM>
- **Generado por**: Faro al inicio del workflow-adaptacion
- **Workflow**: <nombre de la adaptación en curso>

---

## 1. Agentes activos

| Agente | Proyecto (ruta) | Rol | Claude model |
|---|---|---|---|
| Eco | `$WORKSPACE/Eco` | AI partner de the user | Claude Sonnet 4.6 |
| Prima | `$WORKSPACE/Prima` | Jefa I+D+I Eco Consulting | Claude Opus 4.6 |
| Faro | orquestador paralelo | Coordina workflows | Claude Opus 4.7 |
| ... | | | |

## 2. Sistema de memoria

- **eco_memory**: MCP en `$HOME/Desktop\eco_memory\scripts\eco_mcp.py`
  - Backend: ChromaDB + Ollama (mxbai-embed-large)
  - Tools disponibles: <lista desde MCP>
- **eco_graph**: MCP en `$HOME/Desktop\eco_graph_mcp\eco_graph_mcp.py`
  - Backend: PostgreSQL 17.9 + pgvector 0.8.2
  - Tools disponibles: <lista desde MCP>
- **utility-tools**: MCP en `$HOME/Desktop\utility-tools\utility-tools.py`
  - Utilidades (temporales, aleatoriedad, conversiones)

## 3. Sesiones

- **Identificación**: por heartbeat en cada proyecto (`<proyecto>\.session_heartbeat`)
- **Sesión activa** (al momento del snapshot): <proyecto actualmente activo o "ninguno">
- **Cómo consultar sesión activa**: `<comando>` o query a eco_memory

## 4. MCPs instalados

| MCP | Ruta config | Estado | Notas |
|---|---|---|---|
| eco_memory | `claude_desktop_config.json` | activo | |
| eco_graph | `claude_desktop_config.json` | activo | requiere env var `ECO_GRAPH_DB_PASSWORD` |
| utility-tools | `claude_desktop_config.json` | activo | |
| ... | | | |

## 5. Credenciales / secretos (ubicación, no valor)

- **claude_desktop_config.json**: tokens de MCPs y plugins
- **~/.claude.json**: tokens personales de plugins específicos
- **<otros>**: <archivos donde viven credenciales>

## 6. Configuraciones dinámicas

- **Proyecto activo detectado por**: <heartbeat | env var | query>
- **Triggers de cambio de estado**: <qué eventos cambian el estado del ecosistema>

## 7. Adaptaciones previas (si aplica)

Si ya hay adaptaciones en marcha con otras herramientas externas, listarlas para evitar conflictos:

- **Telegram**: bots para Eco, Prima. Bridge en `C:\<ruta>`. Triggers de mantenimiento documentados en `<obsidian>\Adaptaciones\Telegram_<fecha>.md`.
- **The Commons**: credenciales de Prima disponibles. Acceso manual por the user.
- ...
