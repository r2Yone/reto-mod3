from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from base_datos import obtener_sesion
from esquemas import EmpleadoBaja, EmpleadoCrear, EmpleadoEditar, EmpleadoSalida
from modelos import Empleado

router = APIRouter(prefix="/api/empleados", tags=["empleados"])

MSG_CORREO_DUPLICADO = "El correo ya está registrado"
MSG_EDITAR_BAJA = "No se puede editar a un empleado dado de baja"


def _correo_existe(sesion: Session, correo: str) -> bool:
    return sesion.scalar(select(Empleado.id).where(Empleado.correo == correo)) is not None


@router.get("", response_model=list[EmpleadoSalida])
def listar_empleados(
    q: str | None = None,
    departamento: str | None = None,
    sesion: Session = Depends(obtener_sesion),
):
    consulta = select(Empleado).order_by(Empleado.id)

    # func.lower en ambos lados: SQLite solo ignora mayúsculas en ASCII
    texto = (q or "").strip().lower()
    if texto:
        patron = f"%{texto}%"
        consulta = consulta.where(
            func.lower(Empleado.nombre).like(patron)
            | func.lower(Empleado.correo).like(patron)
        )
    if departamento:
        consulta = consulta.where(Empleado.departamento == departamento)

    return sesion.scalars(consulta).all()


@router.post("", response_model=EmpleadoSalida, status_code=201)
def crear_empleado(datos: EmpleadoCrear, sesion: Session = Depends(obtener_sesion)):
    # La validación (422) ya ocurrió; ahora la regla 1 (409)
    if _correo_existe(sesion, datos.correo):
        raise HTTPException(status_code=409, detail=MSG_CORREO_DUPLICADO)

    # Si dos peticiones chocan en el número consecutivo, se reintenta
    for _ in range(3):
        maximo = sesion.scalar(select(func.max(Empleado.id))) or 0
        empleado = Empleado(
            numero_empleado=f"EMP-{maximo + 1:04d}",
            estado="activo",
            **datos.model_dump(),
        )
        sesion.add(empleado)
        try:
            sesion.commit()
        except IntegrityError:
            sesion.rollback()
            if _correo_existe(sesion, datos.correo):
                raise HTTPException(status_code=409, detail=MSG_CORREO_DUPLICADO)
            continue
        sesion.refresh(empleado)
        return empleado
    raise HTTPException(status_code=409, detail="No se pudo asignar el número de empleado")


def _obtener_o_404(sesion: Session, empleado_id: int) -> Empleado:
    empleado = sesion.get(Empleado, empleado_id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@router.put("/{empleado_id}", response_model=EmpleadoSalida)
def editar_empleado(
    empleado_id: int, datos: EmpleadoEditar, sesion: Session = Depends(obtener_sesion)
):
    # La validación (422) ya ocurrió; ahora la regla 6 (409)
    empleado = _obtener_o_404(sesion, empleado_id)
    if empleado.estado == "baja":
        raise HTTPException(status_code=409, detail=MSG_EDITAR_BAJA)
    empleado.puesto = datos.puesto
    empleado.departamento = datos.departamento
    sesion.commit()
    sesion.refresh(empleado)
    return empleado


@router.post("/{empleado_id}/baja", response_model=EmpleadoSalida)
def dar_de_baja(
    empleado_id: int, datos: EmpleadoBaja, sesion: Session = Depends(obtener_sesion)
):
    empleado = _obtener_o_404(sesion, empleado_id)
    if empleado.estado == "baja":
        raise HTTPException(status_code=409, detail="El empleado ya está dado de baja")
    if datos.fecha_baja < empleado.fecha_ingreso:
        # Depende de la BD, así que no lo valida Pydantic; mantiene la forma {detail, campo}
        return JSONResponse(
            status_code=422,
            content={"detail": "Corrige el campo fecha de baja", "campo": "fecha_baja"},
        )
    empleado.estado = "baja"
    empleado.fecha_baja = datos.fecha_baja
    sesion.commit()
    sesion.refresh(empleado)
    return empleado
