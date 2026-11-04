"""HU-02: directorio de empleados (listar, buscar y filtrar) a nivel API.

La base de datos es compartida, así que cada test crea empleados con un token
único (uuid) en el nombre y el correo, y acota las consultas con ese token.
"""
import uuid

import httpx
import pytest


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


def _listar(url_api: str, **params) -> httpx.Response:
    return httpx.get(f"{url_api}/api/empleados", params=params)


def _buscar_baja(url_api: str) -> dict:
    """No hay endpoint para dar de baja: se usa un empleado en baja ya existente."""
    bajas = [e for e in _listar(url_api).json() if e["estado"] == "baja"]
    if not bajas:
        pytest.skip("No existe ningún empleado en baja y la API aún no permite crearlo")
    return bajas[0]


def test_cp_01_ver_directorio_completo(url_api):
    """CP-01: Ver el directorio completo."""
    t = _token()
    ana = _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")
    _crear(url_api, f"Luis Pérez {t}", f"luis.{t}@empresa.com", "Vendedor", "Ventas")
    _crear(url_api, f"Marta Ruiz {t}", f"marta.{t}@empresa.com", "Contadora", "Finanzas")
    _crear(url_api, f"Carlos Soto {t}", f"carlos.{t}@empresa.com", "Analista", "Recursos Humanos")

    r = _listar(url_api)
    assert r.status_code == 200
    datos = r.json()
    assert len(datos) >= 4
    for e in datos:
        for campo in ("numero_empleado", "nombre", "puesto", "departamento", "estado"):
            assert campo in e and e[campo]

    elemento = next(e for e in datos if e["numero_empleado"] == ana["numero_empleado"])
    assert elemento["nombre"] == f"Ana García {t}"
    assert elemento["puesto"] == "Desarrolladora"
    assert elemento["departamento"] == "Tecnología"
    assert elemento["estado"] == "activo"


def test_cp_03_empleado_en_baja_aparece_en_directorio(url_api):
    """CP-03: Un empleado dado de baja sigue apareciendo en el directorio."""
    baja = _buscar_baja(url_api)
    r = _listar(url_api)
    assert r.status_code == 200
    elemento = next(e for e in r.json() if e["numero_empleado"] == baja["numero_empleado"])
    assert elemento["nombre"] == baja["nombre"]
    assert elemento["estado"] == "baja"


def test_cp_05_buscar_por_nombre(url_api):
    """CP-05: Buscar por nombre."""
    t = _token()
    luis = _crear(url_api, f"Luis Pérez {t}", f"luis.{t}@empresa.com", "Vendedor", "Ventas")
    _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    r = _listar(url_api, q=f"Luis Pérez {t}")
    assert r.status_code == 200
    datos = r.json()
    assert len(datos) == 1
    assert datos[0]["numero_empleado"] == luis["numero_empleado"]


def test_cp_07_buscar_por_correo(url_api):
    """CP-07: Buscar por correo."""
    t = _token()
    correo = f"carlos.soto.{t}@empresa.com"
    carlos = _crear(url_api, f"Carlos Soto {t}", correo, "Analista", "Recursos Humanos")
    _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    r = _listar(url_api, q=correo)
    assert r.status_code == 200
    datos = r.json()
    assert len(datos) == 1
    assert datos[0]["numero_empleado"] == carlos["numero_empleado"]


def test_cp_09_busqueda_nombre_sin_distinguir_mayusculas(url_api):
    """CP-09: La búsqueda por nombre no distingue mayúsculas de minúsculas."""
    t = _token()
    ana = _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    r = _listar(url_api, q=f"ANA GARCÍA {t}".upper())
    assert r.status_code == 200
    datos = r.json()
    assert len(datos) == 1
    assert datos[0]["numero_empleado"] == ana["numero_empleado"]


def test_cp_11_busqueda_correo_sin_distinguir_mayusculas(url_api):
    """CP-11: La búsqueda por correo no distingue mayúsculas de minúsculas."""
    t = _token()
    marta = _crear(url_api, f"Marta Ruiz {t}", f"marta.ruiz.{t}@empresa.com", "Contadora", "Finanzas")

    r = _listar(url_api, q=f"Marta.Ruiz.{t}@EMPRESA.COM")
    assert r.status_code == 200
    datos = r.json()
    assert len(datos) == 1
    assert datos[0]["numero_empleado"] == marta["numero_empleado"]


def test_cp_12_filtrar_por_departamento(url_api):
    """CP-12: Filtrar por departamento."""
    t = _token()
    luis = _crear(url_api, f"Luis Pérez {t}", f"luis.{t}@empresa.com", "Vendedor", "Ventas")
    _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    r = _listar(url_api, departamento="Ventas", q=t)
    assert r.status_code == 200
    datos = r.json()
    assert len(datos) == 1
    assert datos[0]["numero_empleado"] == luis["numero_empleado"]
    assert datos[0]["departamento"] == "Ventas"


def test_cp_14_filtrar_departamento_con_empleados_en_baja(url_api):
    """CP-14: Filtrar por un departamento que incluye empleados dados de baja."""
    baja = _buscar_baja(url_api)
    r = _listar(url_api, departamento=baja["departamento"])
    assert r.status_code == 200
    elemento = next(e for e in r.json() if e["numero_empleado"] == baja["numero_empleado"])
    assert elemento["estado"] == "baja"


def test_cp_15_filtrar_departamento_sin_empleados(url_api):
    """CP-15: Filtrar por un departamento sin empleados."""
    t = _token()
    _crear(url_api, f"Ana García {t}", f"ana.{t}@empresa.com", "Desarrolladora", "Tecnología")

    # Acotado con el token: ningún empleado propio está en Operaciones
    r = _listar(url_api, departamento="Operaciones", q=t)
    assert r.status_code == 200
    assert r.json() == []


def test_cp_17_busqueda_sin_resultados(url_api):
    """CP-17: Búsqueda sin resultados."""
    r = _listar(url_api, q=f"Zacarías Inexistente {_token()}")
    assert r.status_code == 200
    assert r.json() == []


def test_cp_19_quitar_busqueda_restablece_listado(url_api):
    """CP-19: Quitar la búsqueda restablece el listado."""
    t = _token()
    for nombre, depto in (("Ana García", "Tecnología"), ("Luis Pérez", "Ventas"),
                          ("Marta Ruiz", "Finanzas"), ("Carlos Soto", "Recursos Humanos")):
        _crear(url_api, f"{nombre} {t}", f"{nombre.split()[0].lower()}.{t}@empresa.com", "Analista", depto)

    con_busqueda = _listar(url_api, q=f"Luis Pérez {t}")
    assert con_busqueda.status_code == 200
    assert len(con_busqueda.json()) == 1

    total = _listar(url_api)
    vacia = _listar(url_api, q="")
    assert vacia.status_code == 200
    assert len(vacia.json()) == len(total.json())
    assert len(vacia.json()) >= 4
