"""Esquemas Pydantic v2 de entrada y salida."""
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

DEPARTAMENTOS = ["Tecnología", "Ventas", "Finanzas", "Recursos Humanos", "Operaciones"]
DOMINIO = "@empresa.com"

MSG_CORREO_DOMINIO = "Usa el correo corporativo @empresa.com"
MSG_FECHA_FUTURA = "La fecha de ingreso no puede ser futura"


class EmpleadoCrear(BaseModel):
    # Los campos que el sistema asigna (id, numero_empleado, estado...) se ignoran.
    nombre: str = Field(min_length=2, max_length=80)
    correo: str
    puesto: str = Field(min_length=2, max_length=60)
    departamento: Literal["Tecnología", "Ventas", "Finanzas", "Recursos Humanos", "Operaciones"]
    fecha_ingreso: date

    @field_validator("nombre", "puesto", "correo", mode="before")
    @classmethod
    def quitar_espacios(cls, valor):
        return valor.strip() if isinstance(valor, str) else valor

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor: str) -> str:
        if not valor:
            # Correo vacío: dato inválido del campo (regla 3), no la regla 2
            raise ValueError("campo_vacio")
        valor = valor.lower()
        if not valor.endswith(DOMINIO) or len(valor) == len(DOMINIO):
            raise ValueError(MSG_CORREO_DOMINIO)
        return valor

    @field_validator("fecha_ingreso")
    @classmethod
    def validar_fecha(cls, valor: date) -> date:
        if valor > date.today():
            raise ValueError(MSG_FECHA_FUTURA)
        return valor


class EmpleadoEditar(BaseModel):
    # Solo puesto y departamento son editables; nombre, correo y número se ignoran si llegan.
    puesto: str = Field(min_length=2, max_length=60)
    departamento: Literal["Tecnología", "Ventas", "Finanzas", "Recursos Humanos", "Operaciones"]

    @field_validator("puesto", mode="before")
    @classmethod
    def quitar_espacios(cls, valor):
        return valor.strip() if isinstance(valor, str) else valor


class EmpleadoBaja(BaseModel):
    fecha_baja: date


class EmpleadoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_empleado: str
    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date
    estado: str
    fecha_baja: date | None
    creado_en: datetime
