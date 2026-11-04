# Fábrica de software con agentes · Módulo 3

Una cadena de seis agentes que convierte una historia de usuario en una aplicación de gestión de empleados desplegada y probada:

| # | Agente | Entrada | Salida | Sesión |
| --- | --- | --- | --- | --- |
| 1 | Analista | Historia de usuario | `salida/HU-xx/criterios.feature` | 1 |
| 2 | Diseñador de pruebas | Criterios | `salida/HU-xx/casos_prueba.json` | 1 |
| 3 | Desarrollador (Claude Code) | Criterios y casos | `app/backend`, `app/frontend` | 2 |
| 4 | Despliegue (Claude Code) | Código | Contenedores con Docker Compose | 3 |
| 5 | Automatizador (Claude Code) | Casos de prueba | `app/tests` (pytest + Playwright) | 3 |
| 6 | Flujo E2E con triage | Pruebas y app desplegada | `salida/HU-xx/reporte.md` | 4 |

## Requisitos

Python 3.12, Node 20 o superior, Docker Desktop, Claude Code y una clave de API de Anthropic con créditos.

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
playwright install chromium
```

## Uso

```bash
# Sesión 1: agentes por separado
python -m agentes.analista historias/HU-01-registrar-empleado.md
python -m agentes.disenador_pruebas salida/HU-01/criterios.feature

# Sesiones 2 a 4: la fábrica completa, cada vez con más agentes
python -m flujos.flujo_s2 historias/HU-01-registrar-empleado.md
python -m flujos.flujo_s3 historias/HU-01-registrar-empleado.md
python -m flujos.flujo_s4 historias/HU-01-registrar-empleado.md
```

Los patrones de cada sesión también tienen un ejemplo corto y ejecutable en [`ejemplos/`](ejemplos/README.md), por ejemplo `python -m ejemplos.s2_flujos.enrutamiento`.

La aplicación queda en http://localhost:8080 y la documentación de la API en http://localhost:8000/docs.

## Reto · HU-10 Solicitar vacaciones

La fábrica extendió la aplicación de empleados con la solicitud de vacaciones, sin cambiar el comportamiento de HU-01 a HU-03.

```bash
python -m flujos.flujo_s4 historias/HU-10-solicitar-vacaciones.md
```

**Qué hace la funcionalidad**

- `POST /api/empleados/{id}/vacaciones` registra un periodo (`fecha_inicio`, `fecha_fin`) y responde los días hábiles descontados (`dias_habiles`) y los que quedan en el año (`dias_restantes`).
- `GET /api/empleados/{id}/vacaciones?anio=AAAA` devuelve el saldo del año: `dias_usados`, `dias_disponibles` y las solicitudes.
- En el directorio, cada empleado activo tiene el botón **Solicitar vacaciones**, que abre un formulario con su saldo.

**Reglas** (detalle en `contexto/reglas_vacaciones.md` y `contexto/convenciones_vacaciones.md`)

- Al menos un año de antigüedad a la fecha de inicio.
- 12 días hábiles por año calendario; se puede usar exactamente lo que queda.
- No cuentan sábados, domingos ni festivos oficiales (LFT, art. 74) de 2026 y 2027.
- Errores con códigos y mensajes exactos: 404, 409 (empleado dado de baja) y 400 (fechas, año, antigüedad, días hábiles, tope).

**Cambios en la fábrica para esta historia**

| Dónde | Cambio |
| --- | --- |
| `contexto/` | Reglas y convenciones de vacaciones agregadas a `reglas_negocio.md` y `convenciones_app.md` |
| `agentes/analista.py` | Validador `validar_mensajes`: cada mensaje exacto del contexto, con su código, debe aparecer en un escenario |
| `agentes/disenador_pruebas.py` | `validar_plan` exige también los mensajes exactos en los casos |
| `agentes/desarrollador.py` | Extender sin romper, cálculos en el backend y orden de validación del contexto |
| `agentes/automatizador.py` | Un empleado nuevo por test y comparaciones exactas de mensajes |
| `flujos/verificacion.py` | La trazabilidad caso → test se revisa solo en los archivos de la historia |

**Resultado de la ejecución final**

Estado **LISTA**, 0 ciclos de corrección, 1.43 USD y 111 de 111 pruebas (HU-02, HU-03 y HU-10).

Evidencias en `salida/HU-10/`: `criterios.feature` (67 escenarios), `casos_prueba.json` (75 casos), `reporte.md` y `decisiones.md`. La auditoría de la ejecución está en `auditoria.jsonl`.
