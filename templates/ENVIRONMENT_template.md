---
name: Entorno de ejecución
type: plantilla
produces: environment
used_by_workflows:
  - construccion
  - evolucion
  - integracion
  - adaptacion
filled_by: Faro (orquestador)
version: "1.0"
tags:
  - plantilla/environment
  - workflow/construccion
  - agente/faro
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_construccion.md
  final_output: $FARO_ROOT/Sesiones/<sesion>/ENVIRONMENT.md
---

# ENVIRONMENT — Sesión <YYYY-MM-DD>_<proyecto>

Inyectado como preamble a todos los agentes. Define el entorno físico de ejecución.

## Sistema operativo
- **OS**: Windows (versión: <ej. Windows 11>)
- **Shell por defecto**: bash (Git Bash) — comandos Unix-like funcionan
- **Path separator interpretado**: `/` o `\` (los agentes usan `/` por convención excepto rutas Windows nativas que usan `\`)

## Encoding
- **Default stdout**: cp1252 — **rompe con emojis y caracteres no-ASCII**
- **Workaround obligatorio**: ejecutar siempre con `PYTHONIOENCODING=utf-8` cuando el script imprima texto con caracteres especiales
- **Ficheros**: leer/escribir SIEMPRE con `encoding="utf-8"` explícito

## Python
- **Versión**: <python --version, ej. 3.14.3>
- **Ruta del intérprete**: <ej. C:\Python314\python.exe>
- **Venv del proyecto**: <ruta al venv del proyecto, o "no usa venv">
- **Activación**: <comando>

## Dependencias clave del proyecto
- <librería>: <versión>
- <librería>: <versión>

## Servicios externos requeridos
- <servicio>: <cómo verificar que está arriba>
  - Ejemplo: PostgreSQL 17.9 → `psql -U postgres -c "SELECT version();"` debe devolver fila
  - Ejemplo: Ollama → `ollama list` debe devolver al menos un modelo
  - Ejemplo: ChromaDB → puerto 8000 abierto

## Rutas base del proyecto
- **Repo**: <ruta absoluta>
- **Scripts**: <ruta>
- **Tests**: <ruta>
- **BD/datos**: <ruta o config>
- **Configs**: <ruta>

## Comandos útiles del proyecto
- Run tests: `<comando exacto>`
- Run script: `<comando exacto>`
- Lint/format: `<comando o "no aplica">`

## Reglas duras del entorno
- No instalar dependencias nuevas sin pedirle a the user (modifica `requirements.txt` solo si es parte del Plan).
- No tocar configuración global del sistema.
- No modificar Path de Windows.
- Cualquier comando que pueda tardar >30s, lanzarlo con timeout explícito y reportar duración.
