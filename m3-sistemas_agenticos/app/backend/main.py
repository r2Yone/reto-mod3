"""Aplicación FastAPI. Cada recurso nuevo se agrega como un router más."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import modelos  # noqa: F401  (registra las tablas en Base)
from base_datos import Base, motor
from routers import departamentos, empleados, vacaciones

Base.metadata.create_all(motor)

app = FastAPI(title="Gestión de empleados")
app.include_router(empleados.router)
app.include_router(departamentos.router)
app.include_router(vacaciones.router)


@app.get("/api/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}


@app.exception_handler(RequestValidationError)
async def error_validacion(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Convierte el error de Pydantic en {"detail": "mensaje en español"}."""
    error = exc.errors()[0]
    campo = str(error["loc"][-1]) if error["loc"] else "cuerpo"
    mensaje = str(error.get("msg", ""))
    if mensaje.startswith("Value error, ") and mensaje[13:] != "campo_vacio":
        detalle = mensaje[13:]  # mensaje propio (correo corporativo, fecha futura)
    else:
        detalle = f"Corrige el campo {campo}"
    return JSONResponse(status_code=422, content={"detail": detalle, "campo": campo})
