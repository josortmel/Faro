---
name: Checkpoint de verificación
type: plantilla
produces: verification_checkpoint
used_by_workflows:
  - diseno
filled_by: Arquitecto
version: "1.0"
tags:
  - plantilla/verification
  - workflow/disenio
  - agente/arquitecto
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_diseno.md
  final_output: <proyecto>/verification_checkpoint.md
---

# verification_checkpoint — <fecha YYYY-MM-DD HH:MM>

> Plantilla obligatoria para verification_checkpoint producido por el Arquitecto en workflow-diseño v2 (nivel critical).
> Las 3 secciones son obligatorias. Este archivo captura la **realidad** del sistema en un momento concreto, que el Spec y el Plan citan.
> Propósito: el Brief es teoría; verification_checkpoint son hechos.

## Metadatos
- **Proyecto**: <ruta absoluta>
- **Fecha y hora exacta**: <YYYY-MM-DD HH:MM timezone>
- **Autor**: Arquitecto
- **Brief de referencia**: <ruta del Brief v<N>>

---

## 1. Estado real del sistema (comandos ejecutados)

Por cada prereq técnico: comando + output literal. Sin resumir, sin interpretar.

### Python
```bash
$ python --version
<output literal>

$ pip list | grep -E "psycopg2|pgvector|rustworkx|ollama"
<output literal>
```

### PostgreSQL
```bash
$ PGPASSWORD=... psql -h localhost -p <puerto> -U postgres -d <bd> -c "SELECT version();"
<output literal>

$ PGPASSWORD=... psql -... -c "SELECT extversion FROM pg_extension WHERE extname='vector';"
<output literal>
```

### Servicios externos (Ollama, APIs, etc.)
```bash
$ curl -s http://localhost:11434/api/tags | grep <modelo>
<output literal>
```

### Rutas críticas existen
```bash
$ ls -la <ruta1>
<output>
$ ls -la <ruta2>
<output>
```

---

## 2. Contadores reales (BDs, configs)

Valores exactos al momento de la verificación. Incluir timestamp al lado para que si hay drift después se pueda diagnosticar.

### Base de datos `<nombre>`
- Tabla `<tabla1>`: <N> filas (verificado <HH:MM>)
- Tabla `<tabla2>`: <N> filas (verificado <HH:MM>)
- Índices existentes: <lista>
- Extensiones activas: <lista>

### Archivos de config actuales
- `<ruta/archivo.json>`: <hash SHA256 o mtime>
- `<ruta/config.yml>`: <...>

### Procesos en memoria (si aplica)
- <servicio>: running since <timestamp> | stopped

---

## 3. Hallazgos concretos que el Spec debe citar

Cada hallazgo enumerado con referencia explícita al archivo/BD verificado. El Spec **cita** estos hallazgos por número.

- **H1**: <hallazgo concreto> — fuente: <archivo/query/comando>
  - Implicación para el Spec: <qué obliga a tener en cuenta>
- **H2**: <hallazgo>
  - Fuente: ...
  - Implicación: ...
- **H3**: ...

### Ejemplos de hallazgos válidos
- "La tabla `tripletas` tiene 2571 filas a las 11:22 del 2026-04-18. El Spec §3 debe asumir este volumen para los tests de rendimiento."
- "`psql` NO está en el PATH del Git Bash. Todos los comandos SQL del Plan deben usar ruta absoluta `/c/Program Files/PostgreSQL/17/bin/psql.exe`."
- "La columna actual se llama `fuente_id`, no `autor`. La migración tiene que hacer `RENAME COLUMN`, no `ADD COLUMN`."

### Ejemplos de hallazgos INVÁLIDOS (muy vagos)
- ~~"La BD parece estar bien"~~ — no es un hallazgo, es una impresión
- ~~"Revisé las dependencias"~~ — ¿cuáles? ¿qué encontraste?
