# Decisiones · HU-10

Ejecución final: 4 nov 2026, · estado **LISTA** · 0 ciclos de corrección · 1.43 USD · 111/111 pruebas (HU-02, HU-03 y HU-10).

## 1. ¿Qué pasos son workflow y cuáles son agente?
Son **agentes** los pasos donde el modelo decide qué leer, qué herramienta usar y cuántas vueltas dar: el analista y el diseñador (bucle ReAct de `agentes/base.py`, hasta 15 pasos) y el desarrollador, despliegue y automatizador (Claude Code). Por ejemplo, el desarrollador decidió por su cuenta crear `festivos.py` y `servicios_vacaciones.py` y probar `dias_habiles(2026-12-21, 2026-12-31)` antes de terminar. Todo lo demás es **workflow**: el grafo de LangGraph fija el orden, y el código decide si un paso se cumplió (`validar_gherkin`, `validar_mensajes`, `validar_plan`, `verificar_app`, `verificar_despliegue`, `verificar_pruebas_escritas`, `ejecutar_pruebas`) y si se reintenta. El filtro de seguridad y el triage usan un LLM con salida estructurada, pero son una sola llamada que clasifica o enruta: son pasos de workflow con un LLM, no agentes. Las reglas de vacaciones son fijas y verificables.

## 2. ¿Cómo se validó cada salida estructurada? ¿Qué atrapó algún validador?
- **Criterios:** `validar_gherkin` (estructura) + `validar_mensajes`, que agregué para HU-10. Extrae los 9 mensajes exactos de las tablas de `convenciones_vacaciones.md` y exige cada uno letra por letra, con su código (404, 409, 400), en algún escenario. Resultado: 67 escenarios.
- **Casos:** el esquema Pydantic `PlanPruebas` en `guardar_casos`. `validar_plan` exige un caso por escenario y los mensajes exactos. Resultado: 75 casos (67 de API y 8 E2E), 0 escenarios sin cubrir.
- **Código, despliegue y pruebas:** `verificar_app` (salud en el 8010 + `npm run build`) → «Verificación: OK»; `verificar_despliegue` (8000, 8080 y proxy `/api`); `verificar_pruebas_escritas`, que limité a `test_hu_10*.py`.
- **Lo que atraparon los hooks** (`auditoria.jsonl`): el automatizador intentó escribir un generador en `%TEMP%\gen_hu10.py` y `confinar_escritura` lo bloqueó (el archivo no existe), así que escribió directamente en `tests/`. Despliegue intentó `grep`, `head` y `tail`; `comandos_permitidos` los negó y el agente repitió los comandos solo con programas permitidos.
- **Lo que ningún validador atrapó:** CP-54 pide un ingreso futuro (`2027-06-01`) que la API rechaza. El automatizador lo cambió por la fecha de hoy, pero así el test ya no prueba que el año se valide antes que la antigüedad. 

## 3. ¿Dónde intervine como persona y qué vi para decidir?
- **Preguntas abiertas del analista:** 
29 de febrero: la regla del aniversario del 29 de febrero no se puede probar con datos concretos dentro de 2026 y 2027.
- **Empleado inexistente en la consulta de saldo:** asume que responde 404 con «Empleado no encontrado», porque el contexto no lo detalla la respuesta específica para el post. Respondí `si`. Las dos eran legítimas: la regla del 29 de febrero no se puede probar con ingresos válidos dentro de 2026-2027, y el 404 del GET no estaba escrito explícitamente para esa ruta. Continué porque `Empleado no encontrado` es el 404 estándar de la app (HU-03) y la tabla de errores es común a ambos endpoints.
- **Revisión de criterios:** comprobé los 9 mensajes con su código y calculé los días hábiles de cada escenario contra la tabla de festivos: 0 diferencias.
- **Plan:** «Plan aprobado por humano» al primer intento. ✏️ *Se comprobo router nuevo sin tocar `empleados.py`, festivos y conteo en el backend (`festivos.py`, `servicios_vacaciones.py`), orden 404 → 409 → 400, `dias_restantes` y `dias_disponibles`, `data-testid` de vacaciones.*
- **Conflicto de fuentes:** la guía dice 422 y otros `data-testid`; `convenciones_vacaciones.md` dice 400/409 y `vacaciones-abrir-{id}`. Decidí que manda el contexto, porque las pruebas ocultas se construyen con él.

## 4. ¿Qué arquitectura de orquestación usa la fábrica y por qué no otra?
Un **orquestador con flujo fijo** en LangGraph (`flujo_s4`), que combina cinco patrones:
- **encadenamiento**: criterios → casos → plan → código;
- **evaluador-optimizador / reflexión**: cada validador devuelve sus problemas al mismo agente;
- **humano en el bucle**: `interrupt` en las preguntas y en el plan;
- **paralelización**: despliegue ‖ automatización, unidos en `listo`;
- **enrutamiento por triage**: en el ciclo E2E, el triage elige quién corrige, hasta 2 ciclos.

No elegí un **supervisor LLM**: el orden de las etapas no cambia entre historias, y un supervisor añadiría costo y variación sin aportar nada. Tampoco una **red** ni una **pizarra**: los agentes no necesitan negociar, y cada uno tiene una salida y una carpeta propias, lo que permite confinar sus permisos. El único punto donde hace falta decidir dinámicamente (quién corrige una falla) usa un router acotado con tres salidas.

## 5. Si algo falló: ¿qué corregí en el agente y por qué no en su resultado?
En la ejecución final no falló ninguna etapa (0 ciclos). Las correcciones fueron **preventivas** y todas en la fábrica, antes de ejecutar:
- **contexto:** agregué las reglas y convenciones de vacaciones, y quité la línea envenenada del Lab 4 (`secretos_demo.txt`) de `convenciones_app.md`;
- **analista y diseñador:** el validador de mensajes exactos, más instrucciones para límites y precondiciones;
- **desarrollador:** extender sin romper, cálculos en el backend y orden de validación;
- **automatizador:** un empleado nuevo por test y comparaciones exactas;
- **trazabilidad por historia** en `verificacion.py`.

No edité `app/` ni `salida/` (salvo este archivo que está leyendo), porque corregir el resultado arregla una sola ejecución, mientras que corregir al agente arregla todas, y la auditoría lo puede demostrar.
