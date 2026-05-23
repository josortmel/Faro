---
name: Reporte de auditoría
type: plantilla
produces: audit_report
used_by_workflows:
  - evolucion
filled_by: Auditor
version: "1.0"
tags:
  - plantilla/audit
  - workflow/evolucion
  - agente/auditor
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_evolucion.md
  final_output: $FARO_ROOT/Informes/Construcción/<YYYY-MM-DD>_<slug>.md
---

# Audit Report — <sistema/proyecto>

> Plantilla obligatoria del Auditor en workflow-evolucion v2.
> Las 6 secciones son obligatorias. Faro devuelve el Report al Auditor si falta alguna.

## Metadatos
- **Sistema auditado**: <ruta absoluta>
- **Fecha auditoría**: <YYYY-MM-DD HH:MM>
- **Versión actual leída**: <git hash | mtime | N líneas>
- **Auditor**: Diseñador-Opus modo Auditor
- **Encargo de the user (literal)**: <texto>

## 1. Estado actual verificado

### Qué funciona (NO se debe perder — principio rector 2)
Lista concreta con comando/test que lo valida:
- <funcionalidad 1>: verificada con `<comando>` → output: <literal>
- <funcionalidad 2>: verificada con `<comando>`
- ...

### Cómo se usa hoy
- Integraciones conocidas: <lista>
- Usuarios/consumidores del sistema: <lista>
- Endpoints/APIs públicas: <lista>

### Métricas actuales (si aplica)
- Performance baseline: <...>
- Contadores: <...>
- Recursos consumidos: <...>

## 2. Problemas detectados

Cada problema con evidencia concreta:

- **P1**: <descripción>
  - Evidencia: <comando/observación>
  - Severidad: critical | medium | low
  - Impacto si no se resuelve: <qué pasa>

- **P2**: ...

## 3. Cambios propuestos

- **C1**: <descripción>
  - Resuelve: [P1, P2]
  - Archivos a tocar: <lista de rutas>
  - Tipo: refactor | optimización | limpieza | fix | feature
  - Riesgo: bajo | medio | alto
  - Tests de regresión necesarios: <comandos concretos>
  - Rollback: `<comando>` o "restaurar desde archive/"

- **C2**: ...

## 4. Orden sugerido de aplicación

[C3, C1, C2, ...] — con razón del orden:
- C3 primero porque <...>
- Luego C1 porque depende de C3
- Finalmente C2 porque <...>

## 5. Qué NO tocar

Lista explícita de código/archivos intocables — aunque tengan aspecto mejorable:

- <archivo/función>: razón — usado por <quién>, revisar solo tras coordinar con the user
- <...>

## 6. Criterios de éxito global

Bullets verificables que el Verificador usará al final:

- [ ] <criterio 1> — verificable con `<comando>`
- [ ] <criterio 2> — verificable con `<comando>`
- [ ] Todos los tests de regresión listados en los cambios pasan

---

## Flags especiales

- **requiere_escalacion_a_diseño**: <true | false>
  Si true, el Auditor detectó que la complejidad real excede una evolución simple → Faro disparará Bisagra 2 con propuesta de lanzar workflow-diseño.
