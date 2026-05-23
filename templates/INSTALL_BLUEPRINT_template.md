---
name: Blueprint de instalación
type: plantilla
produces: blueprint
used_by_workflows:
  - integracion
filled_by: Diseñador
version: "1.0"
tags:
  - plantilla/blueprint
  - workflow/integracion
  - agente/disenador
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_integracion.md
  final_output: $FARO_ROOT/Informes/Integración/<YYYY-MM-DD>_<slug>.md
---

# Install Blueprint — <tecnología + versión>

> Plantilla obligatoria del Diseñador en workflow-integracion v2.
> Las 6 secciones son obligatorias. Énfasis en **verificación funcional, no declarativa** (principio rector 3).

## Metadatos
- **Tecnología**: <nombre oficial>
- **Versión objetivo**: <exacta>
- **Documentación oficial**: <URL + fecha consulta>
- **Fecha blueprint**: <YYYY-MM-DD>
- **Diseñador**: Opus modo genérico
- **Encargo de the user**: <literal>

## 1. Consulta a base de conocimiento

- **eco_memory consultada** con tags: <lista>
- **Hallazgos previos relevantes**: <lista o "ninguno">
- **Base de conocimiento de errores** (sección del SKILL workflow-integracion) revisada: sí/no
- **Warnings previos sin resolver para esta tech**: <lista o "ninguno">

## 2. Dependencias

| Dependencia | Versión exacta | URL docs | Nota de compatibilidad |
|---|---|---|---|
| <dep1> | <ver> | <url> | <incompatibilidad conocida con X, requiere Y instalado> |
| ... | | | |

## 3. Plan de instalación (pasos ordenados)

- **P1**: <acción descriptiva>
  - Comando exacto: `<cmd>`
  - Output esperado: <literal o regex>
  - Alternativa si falla: `<plan B comando>` (mantener si conocido; null si ninguna)
  - **Verificación funcional del paso** (principio rector 3): `<comando que prueba que el paso hizo lo que debía>`
    Ejemplo MAL: "pip dice installed" → declarativo
    Ejemplo BIEN: `python -c "import X; X.func()"` → funcional

- **P2**: ...

## 4. Criterios de éxito FUNCIONALES

**NO** vale "instalado sin errores". Vale pruebas de uso real.

- [ ] <criterio 1>: `<comando>` → output esperado: `<valor literal>`
- [ ] <criterio 2>: `<comando>` → output esperado: `<valor literal>`
- [ ] Adversarial: `<comando con input inválido>` → debe fallar con `<error esperado>` (graceful degradation)

## 5. Advertencias conocidas

- <warning>: origen <base conocimiento | docs oficiales | inferencia>
- ...

## 6. Rollback

Comando(s) exacto(s) para desinstalar completamente y volver al estado pre-integración:

```bash
# Desinstalar paquete
<comando>

# Revertir config si aplica
<comando>

# Limpiar servicios/procesos
<comando>
```

---

## Flags

- **requiere_escalacion_a_diseño**: <true | false>
