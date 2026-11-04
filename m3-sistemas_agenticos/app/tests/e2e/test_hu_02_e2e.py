"""HU-02: directorio de empleados (listar, buscar y filtrar) de punta a punta.

Los datos se crean por API con un token único (uuid); la interfaz se acota
con ese token cuando el caso lo permite, porque la base es compartida.
"""
import uuid

import httpx
import pytest
from playwright.sync_api import Page, expect


def _token() -> str:
    return uuid.uuid4().hex[:10]


def _crear(url_api: str, nombre: str, correo: str, puesto: str, departamento: str) -> dict:
    r = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": nombre,
            "correo": correo,
            "puesto": puesto,
            "departamento": departamento,
            "fecha_ingreso": "2024-01-15",
        },
    )
    assert r.status_code == 201, r.text
    return r.json()


def _abrir(page: Page, url_web: str) -> None:
    page.goto(url_web)
    expect(page.get_by_test_id("tabla-empleados")).to_be_visible()


def test_cp_02_ver_directorio_completo(page: Page, url_api, url_web):
    """CP-02: Ver el directorio completo."""
    t = _token()
    ana = _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")
    otros = [
        _crear(url_api, f"Luis Pérez {t}", f"luis.{t}@empresa.com", "Vendedor", "Ventas"),
        _crear(url_api, f"Marta Ruiz {t}", f"marta.{t}@empresa.com", "Contadora", "Finanzas"),
        _crear(url_api, f"Carlos Soto {t}", f"carlos.{t}@empresa.com", "Analista", "Recursos Humanos"),
    ]

    _abrir(page, url_web)
    for e in [ana, *otros]:
        fila = page.get_by_test_id(f"fila-empleado-{e['id']}")
        expect(fila).to_be_visible()
        expect(page.get_by_test_id(f"numero-empleado-{e['id']}")).to_have_text(e["numero_empleado"])
        expect(fila).to_contain_text(e["nombre"])
        expect(fila).to_contain_text(e["puesto"])
        expect(fila).to_contain_text(e["departamento"])
        expect(page.get_by_test_id(f"estado-empleado-{e['id']}")).to_have_text("Activo")

    fila_ana = page.get_by_test_id(f"fila-empleado-{ana['id']}")
    expect(fila_ana).to_contain_text("Desarrolladora")
    expect(fila_ana).to_contain_text("Tecnología")


def test_cp_04_empleado_en_baja_aparece_en_directorio(page: Page, url_api, url_web):
    """CP-04: Un empleado dado de baja sigue apareciendo en el directorio."""
    bajas = [e for e in httpx.get(f"{url_api}/api/empleados").json() if e["estado"] == "baja"]
    if not bajas:
        pytest.skip("No existe ningún empleado en baja y la API aún no permite crearlo")
    baja = bajas[0]

    _abrir(page, url_web)
    expect(page.get_by_test_id(f"fila-empleado-{baja['id']}")).to_be_visible()
    expect(page.get_by_test_id(f"numero-empleado-{baja['id']}")).to_have_text(baja["numero_empleado"])
    expect(page.get_by_test_id(f"estado-empleado-{baja['id']}")).to_have_text("Baja")


def test_cp_06_buscar_por_nombre(page: Page, url_api, url_web):
    """CP-06: Buscar por nombre."""
    t = _token()
    luis = _crear(url_api, f"Luis Pérez {t}", f"luis.{t}@empresa.com", "Vendedor", "Ventas")
    _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    _abrir(page, url_web)
    page.get_by_test_id("buscar-empleados").fill(f"Luis Pérez {t}")
    filas = page.get_by_test_id("tabla-empleados").locator("tbody tr")
    expect(filas).to_have_count(1)
    expect(page.get_by_test_id(f"numero-empleado-{luis['id']}")).to_have_text(luis["numero_empleado"])


def test_cp_08_buscar_por_correo(page: Page, url_api, url_web):
    """CP-08: Buscar por correo."""
    t = _token()
    correo = f"carlos.soto.{t}@empresa.com"
    carlos = _crear(url_api, f"Carlos Soto {t}", correo, "Analista", "Recursos Humanos")
    _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    _abrir(page, url_web)
    page.get_by_test_id("buscar-empleados").fill(correo)
    filas = page.get_by_test_id("tabla-empleados").locator("tbody tr")
    expect(filas).to_have_count(1)
    expect(page.get_by_test_id(f"numero-empleado-{carlos['id']}")).to_have_text(carlos["numero_empleado"])


def test_cp_10_busqueda_nombre_sin_distinguir_mayusculas(page: Page, url_api, url_web):
    """CP-10: La búsqueda por nombre no distingue mayúsculas de minúsculas."""
    t = _token()
    ana = _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    _abrir(page, url_web)
    page.get_by_test_id("buscar-empleados").fill(f"ANA GARCÍA {t}".upper())
    filas = page.get_by_test_id("tabla-empleados").locator("tbody tr")
    expect(filas).to_have_count(1)
    expect(page.get_by_test_id(f"numero-empleado-{ana['id']}")).to_have_text(ana["numero_empleado"])


def test_cp_13_filtrar_por_departamento(page: Page, url_api, url_web):
    """CP-13: Filtrar por departamento."""
    t = _token()
    luis = _crear(url_api, f"Luis Pérez {t}", f"luis.{t}@empresa.com", "Vendedor", "Ventas")
    _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    _abrir(page, url_web)
    # El token acota el resultado a los empleados de este test
    page.get_by_test_id("buscar-empleados").fill(t)
    page.get_by_test_id("filtro-departamento").select_option("Ventas")
    filas = page.get_by_test_id("tabla-empleados").locator("tbody tr")
    expect(filas).to_have_count(1)
    expect(page.get_by_test_id(f"numero-empleado-{luis['id']}")).to_have_text(luis["numero_empleado"])
    expect(page.get_by_test_id(f"fila-empleado-{luis['id']}")).to_contain_text("Ventas")


def test_cp_16_filtrar_departamento_sin_empleados(page: Page, url_api, url_web):
    """CP-16: Filtrar por un departamento sin empleados."""
    t = _token()
    _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    _abrir(page, url_web)
    page.get_by_test_id("buscar-empleados").fill(t)
    page.get_by_test_id("filtro-departamento").select_option("Operaciones")
    expect(page.get_by_test_id("tabla-empleados").locator("tbody tr")).to_have_count(0)
    expect(page.get_by_test_id("sin-resultados")).to_be_visible()


def test_cp_18_busqueda_sin_resultados(page: Page, url_web):
    """CP-18: Búsqueda sin resultados."""
    _abrir(page, url_web)
    page.get_by_test_id("buscar-empleados").fill(f"Zacarías Inexistente {_token()}")
    expect(page.get_by_test_id("tabla-empleados").locator("tbody tr")).to_have_count(0)
    expect(page.get_by_test_id("sin-resultados")).to_be_visible()


def test_cp_20_quitar_busqueda_restablece_listado(page: Page, url_api, url_web):
    """CP-20: Quitar la búsqueda restablece el listado."""
    t = _token()
    creados = [
        _crear(url_api, f"{n} {t}", f"{n.split()[0].lower()}.{t}@empresa.com", "Analista", d)
        for n, d in (("Ana García", "Tecnología"), ("Luis Pérez", "Ventas"),
                     ("Marta Ruiz", "Finanzas"), ("Carlos Soto", "Recursos Humanos"))
    ]

    _abrir(page, url_web)
    buscar = page.get_by_test_id("buscar-empleados")
    buscar.fill(f"Luis Pérez {t}")
    expect(page.get_by_test_id("tabla-empleados").locator("tbody tr")).to_have_count(1)

    buscar.fill("")
    for e in creados:
        expect(page.get_by_test_id(f"fila-empleado-{e['id']}")).to_be_visible()
