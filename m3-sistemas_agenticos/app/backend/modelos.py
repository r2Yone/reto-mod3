"""Modelos SQLAlchemy 2."""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from base_datos import Base


class Empleado(Base):
    __tablename__ = "empleados"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero_empleado: Mapped[str] = mapped_column(String(10), unique=True)
    nombre: Mapped[str] = mapped_column(String(80))
    correo: Mapped[str] = mapped_column(String(254), unique=True)
    puesto: Mapped[str] = mapped_column(String(60))
    departamento: Mapped[str] = mapped_column(String(30))
    fecha_ingreso: Mapped[date] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(10), default="activo")
    fecha_baja: Mapped[date | None] = mapped_column(Date, default=None)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Vacacion(Base):
    __tablename__ = "vacaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    empleado_id: Mapped[int] = mapped_column(ForeignKey("empleados.id"))
    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_fin: Mapped[date] = mapped_column(Date)
    dias_habiles: Mapped[int]
