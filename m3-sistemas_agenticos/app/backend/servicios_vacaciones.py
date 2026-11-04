"""Reglas de negocio y cálculos de vacaciones (HU-10)."""
from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from festivos import FESTIVOS
from modelos import Vacacion

TOPE_ANUAL = 12


def dias_habiles(inicio: date, fin: date) -> int:
    """Cuenta los días del periodo (ambos extremos) que no son fin de semana ni festivo."""
    total = 0
    dia = inicio
    while dia <= fin:
        if dia.weekday() < 5 and dia not in FESTIVOS.get(dia.year, set()):
            total += 1
        dia += timedelta(days=1)
    return total


def cumple_antiguedad(ingreso: date, inicio: date) -> bool:
    """Exige un año cumplido a la fecha de inicio; un 29 de febrero cumple el 1 de marzo."""
    try:
        aniversario = ingreso.replace(year=ingreso.year + 1)
    except ValueError:
        aniversario = date(ingreso.year + 1, 3, 1)
    return inicio >= aniversario


def dias_usados(sesion: Session, empleado_id: int, anio: int) -> int:
    total = sesion.scalar(
        select(func.coalesce(func.sum(Vacacion.dias_habiles), 0)).where(
            Vacacion.empleado_id == empleado_id,
            Vacacion.fecha_inicio >= date(anio, 1, 1),
            Vacacion.fecha_inicio <= date(anio, 12, 31),
        )
    )
    return int(total or 0)
