---
name: Mapa de adaptación
type: plantilla
produces: adaptation_map
used_by_workflows:
  - adaptacion
filled_by: Diseñador-Conector
version: "1.0"
tags:
  - plantilla/adaptation
  - workflow/adaptacion
  - agente/disenador_conector
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_adaptacion.md
  final_output: $FARO_ROOT/Informes/Integración/<YYYY-MM-DD>_<slug>.md
---

# Adaptation Map — <herramienta externa> × <ecosistema interno>

> Plantilla obligatoria del Diseñador-Conector en workflow-adaptacion v2.
> Las 7 secciones son obligatorias. **Doble realidad > mapeo** (principio rector 2).

## Metadatos
- **Herramienta externa**: <nombre>, versión API: <si aplica>
- **Docs oficiales**: <URL + fecha consulta>
- **Ecosistema interno afectado**: <agentes/proyectos listados>
- **Fecha**: <YYYY-MM-DD>
- **Conector**: Opus modo Conector

## 1. Realidad externa (verificada, no asumida)

Información obtenida de docs oficiales actuales Y/O de pruebas reales con la API:

- **Capacidades**: <lista con referencia exacta a docs>
- **Limitaciones conocidas**: <lista>
- **Cuotas / rate limits**: <números>
- **Autenticación**: mecanismo + credencial exacta necesaria
- **Modelo de identidad**: ¿la API permite múltiples bots/apps/canales? ¿o es una sola identidad por credencial?

## 2. Realidad interna (verificada, no asumida)

Información de `ECOSYSTEM.md` + queries reales al sistema:

- **Agentes activos** en el ecosistema: <lista con rutas de proyecto>
- **Estado dinámico relevante**: sesión activa, proyecto activo, heartbeat, etc.
- **APIs internas / MCPs disponibles**: <lista>
- **Punto donde viven las credenciales**: <archivo exacto>
- **Dependencias ocultas**: <lista — ej. "eco_memory depende de Ollama local">

## 3. Mapeo interno ↔ externo

Para cada par agente-interno × entidad-externa:

- **M1**: `<agente interno (ej. Eco)>` ↔ `<entidad externa (ej. bot Telegram @Eco_bot)>`
  - **Representación externa**: <bot_id, channel, webhook URL, etc. — valor concreto si ya existe>
  - **Flujo de entrada** (externo → interno): <cómo llega un mensaje/evento al agente correcto>
  - **Flujo de salida** (interno → externo): <cómo el agente envía al sistema externo>
  - **Gestión de estado dinámico**: qué pasa si el agente cambia de sesión activa a mitad
- **M2**: ...

## 4. Plan de implementación (ambos lados, en orden)

- **P1**: <acción>
  - Lado: externo | interno | ambos
  - Comando/API call: `<exacto>`
  - Entidad creada (si aplica): bot / webhook / archivo
  - **Verificación funcional del paso**: `<comando real que prueba que funcionó>`

- **P2**: ...

## 5. Criterios de éxito de flujo extremo-a-extremo

Casos reales que el Verificador probará (con sistema real, no simulado):

- [ ] <caso 1>: "<input concreto>" en lado externo → `<agente correcto>` lo recibe → responde → usuario externo ve respuesta
- [ ] <caso 2>: si hay múltiples agentes, los mensajes NO se mezclan
- [ ] <caso 3>: el sistema no se rompe si el estado interno cambia durante una operación

## 6. Triggers de mantenimiento

Qué eventos en el ecosistema interno O en la API externa invalidarán esta adaptación:

- **Si se añade un agente nuevo al ecosistema** → <qué pasos hay que repetir>
- **Si cambia la estructura de sesiones activas** → <qué revisar>
- **Si la API externa deprecia versión X** → <cómo migrar>
- **Otros triggers**: <lista>

## 7. Rollback completo

Cómo desadaptar:

**Lado externo**:
```
<pasos para eliminar bots, webhooks, API keys creadas>
```

**Lado interno**:
```
<archivos/configs a revertir>
```

---

## Flags

- **requiere_escalacion_a_diseño**: <true | false>
