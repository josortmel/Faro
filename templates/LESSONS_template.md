---
name: Lecciones de sesión
type: plantilla
produces: lessons
used_by_workflows:
  - construccion
  - evolucion
  - integracion
  - adaptacion
filled_by: Todos los agentes
version: "1.0"
tags:
  - plantilla/lessons
  - workflow/construccion
  - agente/todos
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_construccion.md
  final_output: $FARO_ROOT/Sesiones/<sesion>/LESSONS.md
---

# LESSONS — Sesión <YYYY-MM-DD>_<proyecto>

Lecciones compartidas entre agentes en esta sesión. Append-only.

**Formato de cada lección**:
```
[<Agente> - <YYYY-MM-DD HH:MM>]: <lección breve, accionable, con tags entre corchetes>
```

**Reglas**:
- Cada agente lee este archivo antes de empezar su tarea (excepto Verificador, que NO lo lee para no sesgarse).
- Cada agente añade lecciones al final cuando descubre algo nuevo.
- No se borran lecciones — la sesión es un registro completo.
- Al cierre, el Escribano consolida las lecciones más generales en eco_memory.

---

## Lecciones acumuladas

<!-- Ejemplos del histórico — se borran al inicio de cada sesión nueva -->

[Ejecutor - 2026-04-17 14:32]: En Windows cp1252 peta con emojis al imprimir en stdout → usar `PYTHONIOENCODING=utf-8` antes del comando. [windows] [encoding]

[Verificador - 2026-04-17 15:01]: `assert "X" not in output` da falso verde si el test no ejecuta el path que produce X — verificar primero que el path se ejecutó. [tests] [asserts-fragiles]

[Supervisor - 2026-04-17 16:45]: Migraciones con BEGIN/COMMIT literales fallan con psycopg2 — usar `psql -f script.sql` con `ON_ERROR_STOP=1`. [postgres] [migraciones]

---

<!-- Empieza aquí las lecciones de esta sesión -->
