---
name: Especificación técnica
type: plantilla
produces: spec
used_by_workflows:
  - diseno
filled_by: Arquitecto
version: "1.0"
tags:
  - plantilla/spec
  - workflow/disenio
  - agente/arquitecto
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_diseno.md
  final_output: <proyecto>/refactor_v<N>_spec.md
---

# Spec — <Nombre del refactor/feature>

> Plantilla obligatoria para Specs producidos por el Arquitecto en workflow-diseño v2 (nivel critical).
> Las 7 secciones son obligatorias. El CuestionadorSpec rechaza el Spec si falta alguna.

## Metadatos
- **Proyecto**: <ruta absoluta>
- **Fecha**: <YYYY-MM-DD>
- **Versión**: v<N>
- **Brief de referencia**: <ruta + fecha>
- **verification_checkpoint de referencia**: <ruta + fecha>

---

## 1. Cita a Brief y verification_checkpoint

- Este Spec implementa las decisiones del Brief `<ruta>` (versión <N>, fecha <...>).
- Está alineado con la realidad capturada en `<ruta verification_checkpoint>` (fecha <...>).
- Si hay drift entre Brief/verification_checkpoint y lo que este Spec propone, está documentado en la sección 8 "Drift consciente".

---

## 2. Schema / DDL (si aplica)

SQL literal, ejecutable, tal cual se aplicará. No pseudocódigo.

```sql
-- Ejemplo
BEGIN;

ALTER TABLE <tabla> ADD COLUMN <columna> <tipo>;

CREATE INDEX IF NOT EXISTS <idx> ON <tabla>(<columna>);

COMMIT;
```

Si no aplica (el refactor no toca schema), escribir literal: "No aplica — este refactor no toca schema."

---

## 3. Signatures de funciones / tools / endpoints

Tipos explícitos, no descripciones. Si es Python, con `typing`. Si es SQL, con tipos PostgreSQL. Si es REST, con shape JSON.

### Ejemplo Python:
```python
def guardar_tripleta(
    sujeto: str,
    predicado: str,
    objeto: str | None = None,
    peso: float = 1.0,
    fecha: str | None = None,
    origen: str | None = None,
    autor: str | None = None,
) -> str:
    """..."""
```

### Ejemplo SQL function:
```sql
CREATE FUNCTION vecinos(nodo TEXT, profundidad INT DEFAULT 1) RETURNS TABLE(...) ...
```

### Ejemplo REST endpoint:
```
POST /api/v2/tripletas
Request: {"sujeto": str, "predicado": str, "objeto": str | null, ...}
Response 200: {"id": int, "created_at": str}
Response 400: {"error": str, "field": str}
```

---

## 4. Ejemplos reales (no placeholders)

Al menos 3 casos de uso reales con inputs/outputs literales. No "ejemplo genérico X/Y/Z" — casos que the user/Eco usarían mañana.

### Ejemplo 1:
```python
buscar_tripletas(sujeto="Eco", autor="Prima", fecha_desde="2026-04-01")
# Returns: [
#   {"id": 645, "sujeto": "Eco", "predicado": "es prima de", "objeto": "Prima", ...},
#   ...
# ]
```

### Ejemplo 2:
```python
canonizar_predicados_estricto(max_distancia=2, confirmar=False)
# Returns preview JSON: {"modo": "preview", "candidatos": [["vive en", "vive_en", 1, 45, 12, "vive en"]], ...}
```

### Ejemplo 3: ...

---

## 5. Dependencias externas

Versión exacta. Link a documentación oficial.

| Dependencia | Versión | Link docs | Nota |
|---|---|---|---|
| PostgreSQL | 17.9 | https://www.postgresql.org/docs/17/ | Usa pgvector extension |
| pgvector | 0.8.2 | https://github.com/pgvector/pgvector | HNSW index requiere >=0.7 |
| rustworkx | 0.17.1 | https://www.rustworkx.org/ | Wheel cp39-abi3 disponible |
| psycopg2 | 2.9.11 | https://www.psycopg.org/docs/ | — |
| Ollama | - | https://ollama.com/ | Modelo `mxbai-embed-large` |

---

## 6. Handling de errores

Por cada función/tool/endpoint público: qué errores puede devolver y cómo.

### `<función 1>`:
- **Caso**: `<condición de error>` → **Comportamiento**: `<devuelve error X | raise excepción Y | log warning y sigue>`
- **Caso**: `<otra condición>` → **Comportamiento**: ...

### `<función 2>`:
- ...

---

## 7. Criterios de éxito por componente (se traducen a tests en el Plan)

Bullets verificables con comando concreto. Estos criterios son el contrato que el Verificador validará en workflow-construccion.

### Componente: `<módulo 1>`
- [ ] Tests unitarios: `<ruta/test_X.py>` pasa N/N
- [ ] Smoke test funcional: `<comando>` devuelve `<output esperado>`
- [ ] Integración con `<sistema>`: `<query>` retorna `<resultado>`

### Componente: `<módulo 2>`
- [ ] ...

---

## 8. Drift consciente (si aplica)

Si el Spec se aleja intencionadamente del Brief o de verification_checkpoint, documentarlo aquí con justificación:

- **Drift 1**: Brief dice `<X>`, Spec hace `<Y>` — razón: <...>

Si no hay drift, escribir literal: "No hay drift consciente. Spec alineado con Brief y verification_checkpoint."
