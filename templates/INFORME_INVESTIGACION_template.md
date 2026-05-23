---
name: Informe de investigación
type: plantilla
produces: informe
used_by_workflows:
  - investigacion
  - investigacion_profunda
filled_by: Tejedor
version: "1.0"
tags:
  - plantilla/informe
  - workflow/investigacion
  - agente/tejedor
  - proyecto/<slug>
  - estado/borrador
linked_to:
  skills: $FARO_ROOT/Skills/SKILL_md_workflow_investigacion.md
  final_output: $FARO_ROOT/Informes/Investigacion/<YYYY-MM-DD>_<slug>.md
---

# Informe de Investigación — <Tema>

> Plantilla obligatoria del Tejedor en workflow-investigacion v1.
> Las 8 secciones son obligatorias. Faro devuelve el informe al Tejedor si falta alguna.
> Working copy vive en `$FARO_ROOT/Sesiones\<fecha>_<tema>_investigacion\informe_v<N>.md`.
> Copia definitiva (al cierre, por el Escribano): `$FARO_ROOT/Informes\Investigacion\<YYYY-MM-DD>_<tema>.md`

## 1. Metadatos

- **Tema**: <título breve de la investigación>
- **Pregunta raíz de the user (literal)**: <texto>
- **Fecha inicio**: <YYYY-MM-DD HH:MM>
- **Fecha cierre del loop actual**: <YYYY-MM-DD HH:MM>
- **Loop**: <1 | 2 | 3>
- **Tejedor**: Opus
- **Investigadores del loop**: <lista con id + foco asignado>
  - I1 — foco: <texto>
  - I2 — foco: <texto>
  - ...
- **Versiones previas** (si Loop>1): <rutas a informes de loops anteriores>

## 2. Pregunta de investigación

### Pregunta literal de the user
<copiar texto del encargo>

### Clarificaciones acordadas en Bisagra 0
Si hubo clarificaciones, enumerarlas:
- <clarificación 1>
- <clarificación 2>

### Scope confirmado
- **Dentro del scope**: <lista explícita>
- **Fuera del scope**: <lista explícita — deuda consciente>

## 3. Focos temáticos investigados

Tabla-resumen con estado por foco:

| ID | Foco temático | Investigador | Estado | Hallazgos verificables | Hallazgos inaccesibles relevantes |
|---|---|---|---|---|---|
| F1 | <texto breve> | I1 | COMPLETO / PARCIAL / BLOQUEADO | N | M |
| F2 | <texto breve> | I2 | ... | N | M |
| ... | | | | | |

## 4. Hallazgos por foco

Por cada foco, producir su sección con dos categorías de fuentes:

### 4.1 Foco F1 — <título>

**Pregunta del foco**: <la pregunta concreta que debía responder este foco>

#### Hallazgos verificables

Cada hallazgo con id único intra-foco (H1.1, H1.2...):

- **H1.1** — <texto del hallazgo en 1-3 frases>
  - Fuente: <URL>
  - Fecha acceso: <YYYY-MM-DD>
  - Tipo de acceso: WebFetch directo | Playwright navigate+evaluate
  - Cita literal (si aplica): *"<fragmento>"*

- **H1.2** — ...

#### Fuentes inaccesibles relevantes

URLs identificadas (mencionadas en otras fuentes) pero no accesibles por el Investigador. Se conserva su existencia:

- **H1.ir.1** — <qué se supone que contiene>
  - URL: <link>
  - Razón de inaccesibilidad: requiere autenticación / 404 / timeout / bloqueo regional / otra
  - Referenciado en: <URL de fuente verificable que la menciona>
  - Por qué se considera relevante: <1 frase>

#### Dudas del Investigador (no resueltas en este loop)
- <texto>

---

### 4.2 Foco F2 — <título>

(mismo esquema)

---

### (repetir por cada foco)

## 5. Conexiones transversales

Esta sección es **el valor diferencial del Tejedor**. Aquí se detectan patrones cruzados que los Investigadores aislados no podían ver.

### 5.1 Patrones compartidos
Cosas que aparecen en múltiples focos con semántica relacionada:

- **PAT1** — <descripción>
  - Presente en: F1 (H1.3), F3 (H3.1), F4 (H4.2)
  - Interpretación: <qué significa que aparezca en estos 3 focos juntos>

### 5.2 Contradicciones entre fuentes
Cuando fuentes de focos distintos (o del mismo foco) dicen cosas incompatibles:

- **CONT1** — <texto descriptivo>
  - Fuente A dice: <afirmación> (H1.2)
  - Fuente B dice: <afirmación opuesta> (H3.4)
  - Evaluación del Tejedor: <cuál parece más fiable y por qué — o explícitamente "no puedo decidir, queda en hipótesis"> 

### 5.3 Dependencias cruzadas
Cuando un foco presupone un hallazgo de otro:

- **DEP1** — Foco F2 asume <X> que solo respondió Foco F4
  - Implicación: <qué cambia si esa dependencia no se cumple>

## 6. Hipótesis de diseño derivadas

Hipótesis accionables que el Tejedor extrae del conjunto. Cada una numerada:

### H1 — <título de la hipótesis>

- **Hipótesis**: <texto de 1-3 frases describiendo lo que se podría construir/cambiar/integrar>
- **Evidencia que la soporta**: hallazgos F1 (H1.2, H1.5), F3 (H3.1)
- **Contra-hipótesis** (si alguna fuente la desafía): <texto o "ninguna fuente contradice">
- **Workflow sugerido para materializarla**:
  - `workflow-diseno` → produce Spec+Plan antes de ejecutar
  - `workflow-construccion` → si es suficientemente simple
  - `workflow-evolucion` → si es modificación de algo existente
  - `workflow-integracion` → si es traer tecnología externa
  - `workflow-adaptacion` → si es conectar algo con el ecosistema interno
- **Esfuerzo estimado**: bajo / medio / alto (cualitativo)

### H2 — ...

(mínimo 2 hipótesis esperadas; si el informe no genera ninguna, el Tejedor debe escribir "NINGUNA HIPÓTESIS EXTRAÍBLE" con justificación de por qué la investigación fue puramente exploratoria)

## 7. Preguntas abiertas

Lo que sigue sin saberse tras este loop. Cada una con sugerencia accionable:

- **Q1** — <pregunta concreta>
  - Por qué no se cerró: <texto>
  - Qué la cerraría: <foco de investigación adicional / fuente concreta / experimento real / input de the user>
- **Q2** — ...

Si el Loop actual es Loop 2 y hay preguntas abiertas serias, el Tejedor puede marcar algunas como **[RECOMIENDA_LOOP_3]** — Faro las expondrá en Bisagra 2.

## 8. Anexo de fuentes

Lista completa de **todas** las URLs consumidas en este informe, agrupadas por loop:

### Loop 1
- <URL> — acceso: WebFetch — fecha: <YYYY-MM-DD> — citada en: H1.2, H3.1
- <URL> — acceso: Playwright — fecha: <YYYY-MM-DD> — citada en: H2.4
- ...

### Loop 2 (si aplica)
- <URL> — ...

### Fuentes inaccesibles relevantes (todas, cualquier loop)
- <URL> — razón: <...> — referenciada por: <URL fuente verificable>

---

## Flags especiales

Al final del informe, opcionalmente:

- **requiere_decision_de_pepe_para_proceder**: <true | false>
  Si true, el Tejedor detectó que hay contradicciones o dilemas de scope que bloquean cualquier hipótesis accionable. Faro disparará Bisagra 2 con las cuestiones.
- **loop_3_recomendado**: <true | false>
  Si true, hay al menos 1 pregunta abierta marcada [RECOMIENDA_LOOP_3].
