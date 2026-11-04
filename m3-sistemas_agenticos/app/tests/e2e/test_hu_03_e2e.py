"""HU-03: editar y dar de baja empleados (nivel e2e).

Los datos se crean por API con correo único (uuid); la interfaz se acota
buscando por ese token porque la base es compartida.
"""
import uuid

import httpx
from playwright.sync_api import Page, expect


def _crear(url_api: str) -> tuple[dict, str]:
    t = uuid.uuid4().hex[:10]
    r = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "Ana Torres",
            "correo": f"ana.torres.{t}@empresa.com",
            "puesto": "Analista",
            "departamento": "Ventas",
            "fecha_ingreso": "2023-03-01",
        },
    )
    assert r.status_code == 201, r.text
    return r.json(), t


def _abrir(page: Page, url_web: str, token: str) -> None:
    page.goto(url_web)
    expect(page.get_by_test_id("tabla-empleados")).to_be_visible()
    page.get_by_test_id("buscar-empleados").fill(token)


def _baja_ui(page: Page, emp: dict, fecha: str) -> None:
    page.get_by_test_id(f"baja-empleado-{emp['id']}").click()
    page.get_by_test_id("empleado-fecha-baja").fill(fecha)
    page.get_by_test_id("confirmar-baja").click()


def test_cp_02_cambiar_puesto_y_departamento(page: Page, url_api, url_web):
    """CP-02: Cambiar el puesto y el departamento de un empleado activo."""
    emp, t = _crear(url_api)
    _abrir(page, url_web, t)
    page.get_by_test_id(f"editar-empleado-{emp['id']}").click()
    page.get_by_test_id("empleado-puesto").fill("Líder de Finanzas")
    page.get_by_test_id("empleado-departamento").select_option("Finanzas")
    page.get_by_test_id("empleado-guardar").click()
    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    fila = page.get_by_test_id(f"fila-empleado-{emp['id']}")
    expect(fila).to_contain_text("Líder de Finanzas")
    expect(fila).to_contain_text("Finanzas")
    expect(page.get_by_test_id(f"estado-empleado-{emp['id']}")).to_have_text("Activo")


def test_cp_05_rechazar_puesto_de_1_caracter(page: Page, url_api, url_web):
    """CP-05: Rechazar un puesto de 1 carácter."""
    emp, t = _crear(url_api)
    _abrir(page, url_web, t)
    page.get_by_test_id(f"editar-empleado-{emp['id']}").click()
    page.get_by_test_id("empleado-puesto").fill("A")
    page.get_by_test_id("empleado-departamento").select_option("Ventas")
    page.get_by_test_id("empleado-guardar").click()
    expect(page.get_by_test_id("mensaje-error")).to_contain_text("puesto")
    expect(page.get_by_test_id("tabla-empleados")).to_contain_text("Analista")
    expect(page.get_by_test_id(f"fila-empleado-{emp['id']}")).to_contain_text("Analista")


def test_cp_10_dar_de_baja_empleado_activo(page: Page, url_api, url_web):
    """CP-10: Dar de baja a un empleado activo."""
    emp, t = _crear(url_api)
    _abrir(page, url_web, t)
    _baja_ui(page, emp, "2024-06-30")
    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{emp['id']}")).to_have_text("Baja")


def test_cp_12_empleado_en_baja_sigue_en_tabla(page: Page, url_api, url_web):
    """CP-12: El empleado dado de baja sigue apareciendo en el directorio."""
    emp, t = _crear(url_api)
    _abrir(page, url_web, t)
    _baja_ui(page, emp, "2024-06-30")
    expect(page.get_by_test_id("tabla-empleados")).to_be_visible()
    expect(page.get_by_test_id(f"fila-empleado-{emp['id']}")).to_be_visible()
    expect(page.get_by_test_id(f"fila-empleado-{emp['id']}")).to_contain_text("Ana Torres")
    expect(page.get_by_test_id(f"numero-empleado-{emp['id']}")).to_have_text(emp["numero_empleado"])
    expect(page.get_by_test_id(f"estado-empleado-{emp['id']}")).to_have_text("Baja")


def test_cp_15_rechazar_baja_anterior_a_ingreso(page: Page, url_api, url_web):
    """CP-15: Rechazar una fecha de baja anterior a la fecha de ingreso."""
    emp, t = _crear(url_api)
    _abrir(page, url_web, t)
    _baja_ui(page, emp, "2023-02-28")
    expect(page.get_by_test_id("mensaje-error")).to_contain_text("fecha de baja")
    expect(page.get_by_test_id(f"estado-empleado-{emp['id']}")).to_have_text("Activo")
