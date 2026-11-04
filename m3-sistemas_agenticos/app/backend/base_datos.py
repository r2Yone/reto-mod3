"""Conexión a SQLite. La carpeta datos/ se crea al arrancar si no existe."""
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

CARPETA_DATOS = Path(__file__).parent / "datos"
CARPETA_DATOS.mkdir(exist_ok=True)

motor = create_engine(
    f"sqlite:///{CARPETA_DATOS / 'empleados.db'}",
    connect_args={"check_same_thread": False},
)
SesionLocal = sessionmaker(bind=motor, autoflush=False)


class Base(DeclarativeBase):
    pass


def obtener_sesion() -> Iterator[Session]:
    """Dependencia de FastAPI: una sesión por petición."""
    with SesionLocal() as sesion:
        yield sesion
