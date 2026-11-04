from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from base_datos import obtener_sesion
from esquemas import ItemSolicitud, RespuestaSolicitud, SaldoVacaciones, SolicitudVacaciones
from festivos import ANIOS_PERMITIDOS
from modelos import Empleado, Vacacion
from servicios_vacaciones import TOPE_ANUAL, cumple_antiguedad, dias_habiles, dias_usados

router = APIRouter(prefix="/api/empleados/{empleado_id}/vacaciones", tags=["vacaciones"])

MSG_NO_EXISTE = "Empleado no encontrado"
MSG_BAJA = "No se pueden solicitar vacaciones para un empleado dado de baja"
MSG_FIN_ANTERIOR = "La fecha de fin no puede ser anterior a la fecha de inicio"
MSG_OTRO_ANIO = "Las vacaciones deben estar dentro de un mismo año calendario"
MSG_ANIO_TABLA = "Solo se pueden solicitar vacaciones en 2026 y 2027"
MSG_ANTIGUEDAD = "Se requiere al menos un año de antigüedad a la fecha de inicio"
MSG_SIN_HABILES = "El periodo no incluye días hábiles"


def _obtener_empleado(sesion: Session, empleado_id: int) -> Empleado:
    empleado = sesion.get(Empleado, empleado_id)
    if empleado is None:
        raise HTTPException(status_code=404, detail=MSG_NO_EXISTE)
    return empleado


@router.post("", status_code=201, response_model=RespuestaSolicitud)
def solicitar_vacaciones(
    empleado_id: int,
    datos: SolicitudVacaciones,
    sesion: Session = Depends(obtener_sesion),
):
    empleado = _obtener_empleado(sesion, empleado_id)
    if empleado.estado == "baja":
        raise HTTPException(status_code=409, detail=MSG_BAJA)
    if datos.fecha_fin < datos.fecha_inicio:
        raise HTTPException(status_code=400, detail=MSG_FIN_ANTERIOR)
    if datos.fecha_inicio.year != datos.fecha_fin.year:
        raise HTTPException(status_code=400, detail=MSG_OTRO_ANIO)
    anio = datos.fecha_inicio.year
    if anio not in ANIOS_PERMITIDOS:
        raise HTTPException(status_code=400, detail=MSG_ANIO_TABLA)
    if not cumple_antiguedad(empleado.fecha_ingreso, datos.fecha_inicio):
        raise HTTPException(status_code=400, detail=MSG_ANTIGUEDAD)
    habiles = dias_habiles(datos.fecha_inicio, datos.fecha_fin)
    if habiles == 0:
        raise HTTPException(status_code=400, detail=MSG_SIN_HABILES)
    quedan = TOPE_ANUAL - dias_usados(sesion, empleado_id, anio)
    if habiles > quedan:
        raise HTTPException(
            status_code=400,
            detail=f"La solicitud excede los días disponibles: quedan {quedan} días hábiles",
        )

    vacacion = Vacacion(
        empleado_id=empleado_id,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        dias_habiles=habiles,
    )
    sesion.add(vacacion)
    sesion.commit()
    sesion.refresh(vacacion)
    return RespuestaSolicitud(
        id=vacacion.id,
        empleado_id=empleado_id,
        fecha_inicio=vacacion.fecha_inicio,
        fecha_fin=vacacion.fecha_fin,
        dias_habiles=habiles,
        dias_restantes=quedan - habiles,
    )


@router.get("", response_model=SaldoVacaciones)
def consultar_saldo(
    empleado_id: int,
    anio: int | None = None,
    sesion: Session = Depends(obtener_sesion),
):
    _obtener_empleado(sesion, empleado_id)
    anio = anio or date.today().year
    solicitudes = sesion.scalars(
        select(Vacacion)
        .where(
            Vacacion.empleado_id == empleado_id,
            Vacacion.fecha_inicio >= date(anio, 1, 1),
            Vacacion.fecha_inicio <= date(anio, 12, 31),
        )
        .order_by(Vacacion.id)
    ).all()
    usados = sum(s.dias_habiles for s in solicitudes)
    return SaldoVacaciones(
        empleado_id=empleado_id,
        anio=anio,
        dias_usados=usados,
        dias_disponibles=TOPE_ANUAL - usados,
        solicitudes=[ItemSolicitud.model_validate(s) for s in solicitudes],
    )
