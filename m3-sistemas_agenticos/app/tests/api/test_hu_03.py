"""HU-03: editar y dar de baja empleados (nivel API)."""
import uuid

import httpx


def _crear(url_api: str, fecha_ingreso: str = "2023-03-01") -> dict:
    t = uuid.uuid4().hex[:10]
    r = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": "Ana Torres",
            "correo": f"ana.torres.{t}@empresa.com",
            "puesto": "Analista",
            "departamento": "Ventas",
            "fecha_ingreso": fecha_ingreso,
        },
    )
    assert r.status_code == 201, r.text
    return r.json()


def _editar(url_api: str, id_: int, puesto: str, departamento: str) -> httpx.Response:
    return httpx.put(
        f"{url_api}/api/empleados/{id_}",
        json={"puesto": puesto, "departamento": departamento},
    )


def _baja(url_api: str, id_: int, fecha_baja: str) -> httpx.Response:
    return httpx.post(f"{url_api}/api/empleados/{id_}/baja", json={"fecha_baja": fecha_baja})


def _consultar(url_api: str, id_: int) -> dict:
    lista = httpx.get(f"{url_api}/api/empleados").json()
    return next(e for e in lista if e["id"] == id_)


def test_cp_01_cambiar_puesto_y_departamento(url_api):
    """CP-01: Cambiar el puesto y el departamento de un empleado activo."""
    emp = _crear(url_api)
    r = _editar(url_api, emp["id"], "Líder de Finanzas", "Finanzas")
    assert r.status_code == 200, r.text
    actual = _consultar(url_api, emp["id"])
    assert actual["numero_empleado"] == emp["numero_empleado"]
    assert actual["puesto"] == "Líder de Finanzas"
    assert actual["departamento"] == "Finanzas"
    assert actual["estado"] == "activo"


def test_cp_03_numero_y_correo_permanecen(url_api):
    """CP-03: El número de empleado y el correo permanecen iguales tras editar."""
    emp = _crear(url_api)
    r = _editar(url_api, emp["id"], "Líder de Finanzas", "Finanzas")
    assert r.status_code == 200, r.text
    actual = _consultar(url_api, emp["id"])
    assert actual["numero_empleado"] == emp["numero_empleado"]
    assert actual["correo"] == emp["correo"]
    assert actual["puesto"] == "Líder de Finanzas"
    assert actual["departamento"] == "Finanzas"


def _rechazo_puesto(url_api: str, puesto: str) -> None:
    emp = _crear(url_api)
    r = _editar(url_api, emp["id"], puesto, "Ventas")
    assert r.status_code == 422, r.text
    assert "puesto" in r.text
    actual = _consultar(url_api, emp["id"])
    assert actual["puesto"] == "Analista"


def test_cp_04_rechazar_puesto_de_1_caracter(url_api):
    """CP-04: Rechazar un puesto de 1 carácter."""
    _rechazo_puesto(url_api, "A")


def test_cp_06_rechazar_puesto_de_61_caracteres(url_api):
    """CP-06: Rechazar un puesto de 61 caracteres."""
    puesto = "A" * 61
    assert len(puesto) == 61
    _rechazo_puesto(url_api, puesto)


def test_cp_07_rechazar_puesto_vacio(url_api):
    """CP-07: Rechazar un puesto vacío."""
    _rechazo_puesto(url_api, "")


def test_cp_08_rechazar_departamento_fuera_de_lista(url_api):
    """CP-08: Rechazar un departamento que no está en la lista."""
    assert "Marketing" not in httpx.get(f"{url_api}/api/departamentos").json()
    emp = _crear(url_api)
    r = _editar(url_api, emp["id"], "Analista", "Marketing")
    assert r.status_code == 422, r.text
    assert "departamento" in r.text
    assert _consultar(url_api, emp["id"])["departamento"] == "Ventas"


def test_cp_09_dar_de_baja_empleado_activo(url_api):
    """CP-09: Dar de baja a un empleado activo."""
    emp = _crear(url_api)
    r = _baja(url_api, emp["id"], "2024-06-30")
    assert r.status_code == 200, r.text
    actual = _consultar(url_api, emp["id"])
    assert actual["estado"] == "baja"
    assert actual["fecha_baja"] == "2024-06-30"


def test_cp_11_empleado_en_baja_sigue_en_directorio(url_api):
    """CP-11: El empleado dado de baja sigue apareciendo en el directorio."""
    emp = _crear(url_api)
    assert _baja(url_api, emp["id"], "2024-06-30").status_code == 200
    lista = httpx.get(f"{url_api}/api/empleados").json()
    encontrado = [e for e in lista if e["numero_empleado"] == emp["numero_empleado"]]
    assert len(encontrado) == 1
    assert encontrado[0]["nombre"] == "Ana Torres"
    assert encontrado[0]["estado"] == "baja"
    assert encontrado[0]["fecha_baja"] == "2024-06-30"


def test_cp_13_baja_con_fecha_igual_a_ingreso(url_api):
    """CP-13: Dar de baja con fecha igual a la fecha de ingreso."""
    emp = _crear(url_api, fecha_ingreso="2023-03-01")
    r = _baja(url_api, emp["id"], "2023-03-01")
    assert r.status_code == 200, r.text
    actual = _consultar(url_api, emp["id"])
    assert actual["estado"] == "baja"
    assert actual["fecha_baja"] == "2023-03-01"


def test_cp_14_rechazar_baja_anterior_a_ingreso(url_api):
    """CP-14: Rechazar una fecha de baja anterior a la fecha de ingreso."""
    emp = _crear(url_api, fecha_ingreso="2023-03-01")
    r = _baja(url_api, emp["id"], "2023-02-28")
    assert r.status_code == 422, r.text
    assert "fecha de baja" in r.json()["detail"].lower() or "fecha_baja" in r.text
    actual = _consultar(url_api, emp["id"])
    assert actual["estado"] == "activo"
    assert actual["fecha_baja"] is None


def test_cp_16_no_editar_empleado_en_baja(url_api):
    """CP-16: No se puede editar a un empleado dado de baja."""
    emp = _crear(url_api)
    assert _baja(url_api, emp["id"], "2024-06-30").status_code == 200
    r = _editar(url_api, emp["id"], "Gerente", "Operaciones")
    assert r.status_code == 409, r.text
    assert r.json()["detail"] == "No se puede editar a un empleado dado de baja"
    actual = _consultar(url_api, emp["id"])
    assert actual["puesto"] == "Analista"
    assert actual["departamento"] == "Ventas"
