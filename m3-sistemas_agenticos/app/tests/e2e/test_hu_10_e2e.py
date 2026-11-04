"""HU-10: solicitar vacaciones (nivel e2e).

Los datos se crean por API con correo único (uuid); la interfaz se acota
buscando por ese token porque la base es compartida.
"""
import uuid
from datetime import date

import httpx
import pytest
from playwright.sync_api import Page, expect

# El formulario consulta el saldo del año en curso: los casos que lo leen suponen 2026
solo_2026 = pytest.mark.skipif(
    date.today().year != 2026, reason="El caso supone que el año en curso es 2026"
)

ING = "2024-03-10"
P4 = ("2026-06-01", "2026-06-04")  # 4 días hábiles


def _crear(url_api: str, fecha_ingreso: str = ING, baja: bool = False) -> tuple[dict, str]:
    t = uuid.uuid4().hex[:10]
    r = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "Laura Vega",
            "correo": f"laura.vega.{t}@empresa.com",
            "puesto": "Analista",
            "departamento": "Ventas",
            "fecha_ingreso": fecha_ingreso,
        },
    )
    assert r.status_code == 201, r.text
    emp = r.json()
    if baja:
        rb = httpx.post(
            f"{url_api}/api/empleados/{emp['id']}/baja",
            json={"fecha_baja": date.today().isoformat()},
        )
        assert rb.status_code == 200, rb.text
        emp = rb.json()
    return emp, t


def _previa(url_api: str, id_: int, inicio: str, fin: str) -> None:
    r = httpx.post(
        f"{url_api}/api/empleados/{id_}/vacaciones",
        json={"fecha_inicio": inicio, "fecha_fin": fin},
    )
    assert r.status_code == 201, r.text


def _abrir(page: Page, url_web: str, token: str) -> None:
    page.goto(url_web)
    expect(page.get_by_test_id("tabla-empleados")).to_be_visible()
    page.get_by_test_id("buscar-empleados").fill(token)


def _abrir_formulario(page: Page, url_web: str, emp: dict, token: str) -> None:
    _abrir(page, url_web, token)
    page.get_by_test_id(f"vacaciones-abrir-{emp['id']}").click()


def _enviar(page: Page, inicio: str, fin: str) -> None:
    page.get_by_test_id("vacaciones-fecha-inicio").fill(inicio)
    page.get_by_test_id("vacaciones-fecha-fin").fill(fin)
    page.get_by_test_id("vacaciones-enviar").click()


def test_cp_68(page: Page, url_api, url_web):
    """CP-68: Un empleado activo tiene el botón Solicitar vacaciones."""
    emp, t = _crear(url_api)
    _abrir(page, url_web, t)
    fila = page.get_by_test_id(f"fila-empleado-{emp['id']}")
    expect(fila).to_be_visible()
    boton = fila.get_by_test_id(f"vacaciones-abrir-{emp['id']}")
    expect(boton).to_be_visible()
    expect(boton).to_have_text("Solicitar vacaciones")


def test_cp_69(page: Page, url_api, url_web):
    """CP-69: Un empleado dado de baja no tiene el botón Solicitar vacaciones."""
    emp, t = _crear(url_api, baja=True)
    _abrir(page, url_web, t)
    expect(page.get_by_test_id(f"fila-empleado-{emp['id']}")).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{emp['id']}")).to_have_text("Baja")
    expect(page.get_by_test_id(f"vacaciones-abrir-{emp['id']}")).to_have_count(0)


@solo_2026
def test_cp_70(page: Page, url_api, url_web):
    """CP-70: El formulario muestra 12 días disponibles para un empleado sin vacaciones en el año."""
    emp, t = _crear(url_api)
    _abrir_formulario(page, url_web, emp, t)
    expect(page.get_by_test_id("vacaciones-disponibles")).to_have_text("12")


@solo_2026
def test_cp_71(page: Page, url_api, url_web):
    """CP-71: El formulario muestra 8 días disponibles para un empleado con 4 días usados."""
    emp, t = _crear(url_api)
    _previa(url_api, emp["id"], *P4)
    _abrir_formulario(page, url_web, emp, t)
    expect(page.get_by_test_id("vacaciones-disponibles")).to_have_text("8")


def test_cp_72(page: Page, url_api, url_web):
    """CP-72: Enviar una solicitud válida muestra el mensaje de éxito."""
    emp, t = _crear(url_api)
    _abrir_formulario(page, url_web, emp, t)
    _enviar(page, "2026-07-06", "2026-07-10")
    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solicitud registrada: 5 días hábiles. Te quedan 7 días hábiles en 2026."
    )


def test_cp_73(page: Page, url_api, url_web):
    """CP-73: Enviar una solicitud que excede el saldo muestra el detail exacto."""
    emp, t = _crear(url_api)
    _previa(url_api, emp["id"], *P4)
    _abrir_formulario(page, url_web, emp, t)
    _enviar(page, "2026-07-06", "2026-07-16")
    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "La solicitud excede los días disponibles: quedan 8 días hábiles"
    )


def test_cp_74(page: Page, url_api, url_web):
    """CP-74: Enviar una solicitud de un empleado con poca antigüedad muestra el detail exacto."""
    emp, t = _crear(url_api, fecha_ingreso="2026-01-15")
    _abrir_formulario(page, url_web, emp, t)
    _enviar(page, "2026-07-06", "2026-07-10")
    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Se requiere al menos un año de antigüedad a la fecha de inicio"
    )


def test_cp_75(page: Page, url_api, url_web):
    """CP-75: Enviar un periodo sin días hábiles muestra el detail exacto."""
    emp, t = _crear(url_api)
    _abrir_formulario(page, url_web, emp, t)
    _enviar(page, "2026-07-11", "2026-07-12")
    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "El periodo no incluye días hábiles"
    )
