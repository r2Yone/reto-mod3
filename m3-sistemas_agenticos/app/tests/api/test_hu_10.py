"""HU-10: solicitar vacaciones (nivel API).

Cada test crea su propio empleado con correo único (uuid) y prepara por API
las solicitudes previas, así que se puede repetir sin choques en la base compartida.
"""
import uuid
from datetime import date

import httpx
import pytest

# Los casos que dependen del año en curso suponen que es 2026
solo_2026 = pytest.mark.skipif(
    date.today().year != 2026, reason="El caso supone que el año en curso es 2026"
)

ING = "2024-03-10"  # antigüedad suficiente para todas las fechas de 2026 y 2027

P1 = ("2026-07-06", "2026-07-10", 5)  # 5 días hábiles
P4 = ("2026-06-01", "2026-06-04", 4)  # 4 días hábiles
S5 = ("2026-06-01", "2026-06-05", 5)  # 5 días hábiles
S7 = ("2026-06-08", "2026-06-16", 7)  # 7 días hábiles (suman 12 con S5)
S6 = ("2026-06-08", "2026-06-15", 6)  # 6 días hábiles (suman 11 con S5)

SIN_HABILES = "El periodo no incluye días hábiles"
SIN_ANTIGUEDAD = "Se requiere al menos un año de antigüedad a la fecha de inicio"
OTRO_ANIO = "Las vacaciones deben estar dentro de un mismo año calendario"
FUERA_TABLA = "Solo se pueden solicitar vacaciones en 2026 y 2027"
FIN_ANTERIOR = "La fecha de fin no puede ser anterior a la fecha de inicio"
EMPLEADO_BAJA = "No se pueden solicitar vacaciones para un empleado dado de baja"


def _crear(url_api: str, fecha_ingreso: str, baja: bool = False) -> dict:
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
    return emp


def _solicitar(url_api: str, id_: int, inicio: str, fin: str) -> httpx.Response:
    return httpx.post(
        f"{url_api}/api/empleados/{id_}/vacaciones",
        json={"fecha_inicio": inicio, "fecha_fin": fin},
    )


def _saldo(url_api: str, id_: int, anio: int | None = None) -> httpx.Response:
    params = {"anio": anio} if anio else {}
    return httpx.get(f"{url_api}/api/empleados/{id_}/vacaciones", params=params)


def _preparar(url_api: str, id_: int, previas: tuple = ()) -> list[dict]:
    """Registra por API las solicitudes previas (inicio, fin, días hábiles esperados)."""
    creadas = []
    for inicio, fin, dias in previas:
        r = _solicitar(url_api, id_, inicio, fin)
        assert r.status_code == 201, r.text
        assert r.json()["dias_habiles"] == dias
        creadas.append(r.json())
    return creadas


def _estado_en_lista(url_api: str, id_: int) -> str:
    r = httpx.get(f"{url_api}/api/empleados")
    assert r.status_code == 200, r.text
    return next(e for e in r.json() if e["id"] == id_)["estado"]


def _exito(url_api, inicio, fin, dias, restantes, ingreso=ING, previas=()) -> None:
    emp = _crear(url_api, ingreso)
    _preparar(url_api, emp["id"], previas)
    r = _solicitar(url_api, emp["id"], inicio, fin)
    assert r.status_code == 201, r.text
    cuerpo = r.json()
    assert cuerpo["empleado_id"] == emp["id"]
    assert cuerpo["fecha_inicio"] == inicio
    assert cuerpo["fecha_fin"] == fin
    assert cuerpo["dias_habiles"] == dias
    assert cuerpo["dias_restantes"] == restantes


def _rechazo(url_api, inicio, fin, codigo, detail, ingreso=ING, previas=(), baja=False) -> None:
    emp = _crear(url_api, ingreso, baja=baja)
    _preparar(url_api, emp["id"], previas)
    r = _solicitar(url_api, emp["id"], inicio, fin)
    assert r.status_code == codigo, r.text
    assert r.json()["detail"] == detail


def test_cp_01(url_api):
    """CP-01: Solicitud válida de cinco días hábiles sin vacaciones previas."""
    _exito(url_api, "2026-07-06", "2026-07-10", 5, 7)


def test_cp_02(url_api):
    """CP-02: Cumple exactamente un año de antigüedad el día de inicio y el periodo tiene un festivo y dos fines de semana."""
    _exito(url_api, "2026-12-21", "2026-12-31", 8, 4, ingreso="2025-12-21")


def test_cp_03(url_api):
    """CP-03: Se usa exactamente lo que queda con 5 días usados y una solicitud de 7 días hábiles."""
    _exito(url_api, "2026-07-13", "2026-07-21", 7, 0, previas=(P1,))


def test_cp_04(url_api):
    """CP-04: Se usa exactamente lo que queda con 4 días usados y una solicitud de 8 días hábiles."""
    _exito(url_api, "2026-07-06", "2026-07-15", 8, 0, previas=(P4,))


def test_cp_05(url_api):
    """CP-05: Un periodo de un solo día hábil donde la fecha de fin es igual a la de inicio."""
    _exito(url_api, "2026-07-06", "2026-07-06", 1, 11)


def test_cp_06(url_api):
    """CP-06: Un fin de semana dentro del periodo no se descuenta."""
    _exito(url_api, "2026-07-10", "2026-07-13", 2, 10)


def test_cp_07(url_api):
    """CP-07: El 16 de septiembre de 2026 no se descuenta."""
    _exito(url_api, "2026-09-14", "2026-09-18", 4, 8)


def test_cp_08(url_api):
    """CP-08: Año Nuevo de 2026 no se descuenta."""
    _exito(url_api, "2026-01-01", "2026-01-02", 1, 11)


def test_cp_09(url_api):
    """CP-09: El Día de la Constitución de 2026 no se descuenta."""
    _exito(url_api, "2026-02-02", "2026-02-06", 4, 8)


def test_cp_10(url_api):
    """CP-10: El natalicio de Benito Juárez de 2026 no se descuenta."""
    _exito(url_api, "2026-03-16", "2026-03-20", 4, 8)


def test_cp_11(url_api):
    """CP-11: El Día del Trabajo de 2026 no se descuenta."""
    _exito(url_api, "2026-04-27", "2026-05-01", 4, 8)


def test_cp_12(url_api):
    """CP-12: La Revolución Mexicana de 2026 no se descuenta."""
    _exito(url_api, "2026-11-16", "2026-11-20", 4, 8)


def test_cp_13(url_api):
    """CP-13: Un festivo que cae en sábado no se recorre al viernes ni al lunes en 2027."""
    _exito(url_api, "2027-04-30", "2027-05-03", 2, 10)


def test_cp_14(url_api):
    """CP-14: La Navidad de 2027 cae en sábado y no se recorre."""
    _exito(url_api, "2027-12-24", "2027-12-27", 2, 10)


def test_cp_15(url_api):
    """CP-15: El Día de la Constitución de 2027 no se descuenta."""
    _exito(url_api, "2027-02-01", "2027-02-05", 4, 8)


def test_cp_16(url_api):
    """CP-16: El natalicio de Benito Juárez de 2027 no se descuenta."""
    _exito(url_api, "2027-03-15", "2027-03-19", 4, 8)


def test_cp_17(url_api):
    """CP-17: El 16 de septiembre de 2027 no se descuenta."""
    _exito(url_api, "2027-09-13", "2027-09-17", 4, 8)


def test_cp_18(url_api):
    """CP-18: La Revolución Mexicana de 2027 no se descuenta."""
    _exito(url_api, "2027-11-15", "2027-11-19", 4, 8)


def test_cp_19(url_api):
    """CP-19: Dos solicitudes del mismo año acumulan sus días usados."""
    _exito(url_api, "2026-07-13", "2026-07-17", 5, 2, previas=(P1,))


def test_cp_20(url_api):
    """CP-20: El último día hábil del año 2026 es una solicitud válida."""
    _exito(url_api, "2026-12-31", "2026-12-31", 1, 11)


def test_cp_21(url_api):
    """CP-21: El último día hábil del año 2027 es una solicitud válida."""
    _exito(url_api, "2027-12-31", "2027-12-31", 1, 11)


def test_cp_22(url_api):
    """CP-22: Un sábado y un domingo no tienen días hábiles."""
    _rechazo(url_api, "2026-07-11", "2026-07-12", 400, SIN_HABILES)


def test_cp_23(url_api):
    """CP-23: Un periodo de un solo día festivo (16 de septiembre de 2026) no tiene días hábiles."""
    _rechazo(url_api, "2026-09-16", "2026-09-16", 400, SIN_HABILES)


def test_cp_24(url_api):
    """CP-24: Un periodo de un solo día festivo (25 de diciembre de 2026) no tiene días hábiles."""
    _rechazo(url_api, "2026-12-25", "2026-12-25", 400, SIN_HABILES)


def test_cp_25(url_api):
    """CP-25: Un periodo de un solo día festivo (1 de enero de 2026) no tiene días hábiles."""
    _rechazo(url_api, "2026-01-01", "2026-01-01", 400, SIN_HABILES)


def test_cp_26(url_api):
    """CP-26: Un periodo de un solo día festivo (1 de enero de 2027) no tiene días hábiles."""
    _rechazo(url_api, "2027-01-01", "2027-01-01", 400, SIN_HABILES)


def test_cp_27(url_api):
    """CP-27: Un festivo en sábado seguido de domingo no tiene días hábiles."""
    _rechazo(url_api, "2027-05-01", "2027-05-02", 400, SIN_HABILES)


def test_cp_28(url_api):
    """CP-28: Sin días hábiles se rechaza aunque el empleado ya no tenga días disponibles."""
    _rechazo(url_api, "2026-07-11", "2026-07-12", 400, SIN_HABILES, previas=(S5, S7))


def test_cp_29(url_api):
    """CP-29: Se rechaza una solicitud de 9 días hábiles cuando quedan 8."""
    _rechazo(url_api, "2026-07-06", "2026-07-16", 400,
             "La solicitud excede los días disponibles: quedan 8 días hábiles", previas=(P4,))


def test_cp_30(url_api):
    """CP-30: Se rechaza cualquier periodo con días hábiles cuando ya se usaron los 12 días."""
    _rechazo(url_api, "2026-08-03", "2026-08-03", 400,
             "La solicitud excede los días disponibles: quedan 0 días hábiles", previas=(S5, S7))


def test_cp_31(url_api):
    """CP-31: Se rechaza pasarse por un día cuando queda 1 y se escribe días hábiles en plural."""
    _rechazo(url_api, "2026-08-03", "2026-08-04", 400,
             "La solicitud excede los días disponibles: quedan 1 días hábiles", previas=(S5, S6))


def test_cp_32(url_api):
    """CP-32: Se acepta el último día disponible cuando quedan exactamente 1."""
    _exito(url_api, "2026-08-03", "2026-08-03", 1, 0, previas=(S5, S6))


def test_cp_33(url_api):
    """CP-33: Una solicitud de 13 días hábiles supera el tope de 12 de un empleado sin vacaciones previas."""
    _rechazo(url_api, "2026-08-03", "2026-08-19", 400,
             "La solicitud excede los días disponibles: quedan 12 días hábiles")


def test_cp_34(url_api):
    """CP-34: Una solicitud de 12 días hábiles usa el tope completo."""
    _exito(url_api, "2026-08-03", "2026-08-18", 12, 0)


def test_cp_35(url_api):
    """CP-35: Los días usados en 2026 no restan del saldo de 2027."""
    _exito(url_api, "2027-07-05", "2027-07-09", 5, 7, previas=(S5, S7))


def test_cp_36(url_api):
    """CP-36: Se rechaza a quien ingresó el 2025-12-21 con inicio el 2026-12-18."""
    _rechazo(url_api, "2026-12-18", "2026-12-18", 400, SIN_ANTIGUEDAD, ingreso="2025-12-21")


def test_cp_37(url_api):
    """CP-37: Se rechaza a quien ingresó el 2025-12-21 con inicio un día antes del aniversario."""
    _rechazo(url_api, "2026-12-20", "2026-12-22", 400, SIN_ANTIGUEDAD, ingreso="2025-12-21")


def test_cp_38(url_api):
    """CP-38: Se rechaza a un empleado con pocos meses de antigüedad."""
    _rechazo(url_api, "2026-07-06", "2026-07-10", 400, SIN_ANTIGUEDAD, ingreso="2026-01-15")


def test_cp_39(url_api):
    """CP-39: Se acepta a quien ingresó el 2024-03-10 con inicio el 2026-07-06."""
    _exito(url_api, "2026-07-06", "2026-07-06", 1, 11)


def test_cp_40(url_api):
    """CP-40: Se rechaza una fecha de fin un día anterior a la de inicio."""
    _rechazo(url_api, "2026-07-10", "2026-07-09", 400, FIN_ANTERIOR)


def test_cp_41(url_api):
    """CP-41: Se rechaza un periodo que cruza de diciembre de 2026 a enero de 2027."""
    _rechazo(url_api, "2026-12-28", "2027-01-08", 400, OTRO_ANIO)


def test_cp_42(url_api):
    """CP-42: Se rechaza un periodo que cruza el año por un solo día."""
    _rechazo(url_api, "2026-12-31", "2027-01-01", 400, OTRO_ANIO)


def test_cp_43(url_api):
    """CP-43: Un periodo que cruza de 2027 a 2028 se rechaza por cruzar el año y no por el año fuera de la tabla."""
    _rechazo(url_api, "2027-12-31", "2028-01-03", 400, OTRO_ANIO)


def test_cp_44(url_api):
    """CP-44: Se rechaza un periodo en 2028 porque el año no está en la tabla de festivos."""
    _rechazo(url_api, "2028-01-10", "2028-01-14", 400, FUERA_TABLA)


def test_cp_45(url_api):
    """CP-45: Se rechaza el primer día hábil después de 2027."""
    _rechazo(url_api, "2028-01-03", "2028-01-03", 400, FUERA_TABLA)


def test_cp_46(url_api):
    """CP-46: Se rechaza un periodo en 2025 porque el año no está en la tabla de festivos."""
    _rechazo(url_api, "2025-12-15", "2025-12-19", 400, FUERA_TABLA)


def test_cp_47(url_api):
    """CP-47: Se rechaza el último día de 2025."""
    _rechazo(url_api, "2025-12-31", "2025-12-31", 400, FUERA_TABLA)


def test_cp_48(url_api):
    """CP-48: Una fecha con formato inválido se rechaza con el 422 automático de FastAPI."""
    emp = _crear(url_api, ING)
    r = _solicitar(url_api, emp["id"], "21-12-2026", "2026-12-31")
    assert r.status_code == 422, r.text
    assert _saldo(url_api, emp["id"], 2026).json()["solicitudes"] == []


def test_cp_49(url_api):
    """CP-49: Se rechaza un empleado que no existe."""
    r = _solicitar(url_api, 9999, "2026-07-06", "2026-07-10")
    assert r.status_code == 404, r.text
    assert r.json()["detail"] == "Empleado no encontrado"


def test_cp_50(url_api):
    """CP-50: Se rechaza un empleado dado de baja."""
    _rechazo(url_api, "2026-07-06", "2026-07-10", 409, EMPLEADO_BAJA, baja=True)


def test_cp_51(url_api):
    """CP-51: El empleado inexistente se valida antes que las fechas."""
    r = _solicitar(url_api, 9999, "2026-07-10", "2026-07-09")
    assert r.status_code == 404, r.text
    assert r.json()["detail"] == "Empleado no encontrado"


def test_cp_52(url_api):
    """CP-52: El empleado dado de baja se valida antes que las fechas."""
    _rechazo(url_api, "2026-07-10", "2026-07-09", 409, EMPLEADO_BAJA, baja=True)


def test_cp_53(url_api):
    """CP-53: La fecha de fin anterior se valida antes que la antigüedad."""
    _rechazo(url_api, "2026-07-10", "2026-07-09", 400, FIN_ANTERIOR, ingreso="2026-01-15")


def test_cp_54(url_api):
    """CP-54: El año fuera de la tabla se valida antes que la antigüedad."""
    # El caso pide ingreso 2027-06-01, que es futuro y la API no lo acepta: se usa el
    # ingreso de hoy, que también incumple la antigüedad en 2028, así que el orden se prueba igual.
    _rechazo(url_api, "2028-01-10", "2028-01-14", 400, FUERA_TABLA, ingreso=date.today().isoformat())


def test_cp_55(url_api):
    """CP-55: La antigüedad se valida antes que los días hábiles."""
    _rechazo(url_api, "2026-07-11", "2026-07-12", 400, SIN_ANTIGUEDAD, ingreso="2026-01-15")


def test_cp_56(url_api):
    """CP-56: Consultar el saldo de 2026 con una solicitud de 8 días hábiles."""
    emp = _crear(url_api, "2025-12-21")
    # El id de la solicitud lo asigna la base compartida: se compara con el que devolvió el POST
    solicitud = _preparar(url_api, emp["id"], (("2026-12-21", "2026-12-31", 8),))[0]
    r = _saldo(url_api, emp["id"], 2026)
    assert r.status_code == 200, r.text
    cuerpo = r.json()
    assert cuerpo["empleado_id"] == emp["id"]
    assert cuerpo["anio"] == 2026
    assert cuerpo["dias_usados"] == 8
    assert cuerpo["dias_disponibles"] == 4
    assert cuerpo["solicitudes"] == [
        {"id": solicitud["id"], "fecha_inicio": "2026-12-21", "fecha_fin": "2026-12-31", "dias_habiles": 8}
    ]


def test_cp_57(url_api):
    """CP-57: Consultar el saldo de un año sin solicitudes."""
    emp = _crear(url_api, ING)
    r = _saldo(url_api, emp["id"], 2027)
    assert r.status_code == 200, r.text
    cuerpo = r.json()
    assert cuerpo["anio"] == 2027
    assert cuerpo["dias_usados"] == 0
    assert cuerpo["dias_disponibles"] == 12
    assert cuerpo["solicitudes"] == []


@solo_2026
def test_cp_58(url_api):
    """CP-58: Consultar el saldo sin indicar el año usa el año en curso."""
    emp = _crear(url_api, ING)
    _preparar(url_api, emp["id"], (P1,))
    r = _saldo(url_api, emp["id"])
    assert r.status_code == 200, r.text
    cuerpo = r.json()
    assert cuerpo["anio"] == 2026
    assert cuerpo["dias_usados"] == 5
    assert cuerpo["dias_disponibles"] == 7


def test_cp_59(url_api):
    """CP-59: Una solicitud rechazada no se registra ni descuenta días."""
    emp = _crear(url_api, ING)
    previa = _preparar(url_api, emp["id"], (P4,))[0]
    r = _solicitar(url_api, emp["id"], "2026-07-06", "2026-07-16")
    assert r.status_code == 400, r.text
    g = _saldo(url_api, emp["id"], 2026)
    assert g.status_code == 200, g.text
    cuerpo = g.json()
    assert cuerpo["dias_usados"] == 4
    assert cuerpo["dias_disponibles"] == 8
    assert len(cuerpo["solicitudes"]) == 1
    assert cuerpo["solicitudes"][0]["id"] == previa["id"]
    assert cuerpo["solicitudes"][0]["fecha_inicio"] == "2026-06-01"
    assert cuerpo["solicitudes"][0]["fecha_fin"] == "2026-06-04"


def test_cp_60(url_api):
    """CP-60: Un empleado activo tiene el botón Solicitar vacaciones (estado activo en la lista)."""
    emp = _crear(url_api, ING)
    assert _estado_en_lista(url_api, emp["id"]) == "activo"


def test_cp_61(url_api):
    """CP-61: Un empleado dado de baja no tiene el botón Solicitar vacaciones (estado baja en la lista)."""
    emp = _crear(url_api, ING, baja=True)
    assert _estado_en_lista(url_api, emp["id"]) == "baja"


def test_cp_62(url_api):
    """CP-62: El formulario muestra 12 días disponibles para un empleado sin vacaciones en el año."""
    emp = _crear(url_api, ING)
    r = _saldo(url_api, emp["id"], 2026)
    assert r.status_code == 200, r.text
    assert r.json()["anio"] == 2026
    assert r.json()["dias_usados"] == 0
    assert r.json()["dias_disponibles"] == 12


def test_cp_63(url_api):
    """CP-63: El formulario muestra 8 días disponibles para un empleado con 4 días usados."""
    emp = _crear(url_api, ING)
    _preparar(url_api, emp["id"], (P4,))
    r = _saldo(url_api, emp["id"], 2026)
    assert r.status_code == 200, r.text
    assert r.json()["anio"] == 2026
    assert r.json()["dias_usados"] == 4
    assert r.json()["dias_disponibles"] == 8


def test_cp_64(url_api):
    """CP-64: Enviar una solicitud válida muestra el mensaje de éxito."""
    _exito(url_api, "2026-07-06", "2026-07-10", 5, 7)


def test_cp_65(url_api):
    """CP-65: Enviar una solicitud que excede el saldo muestra el detail exacto."""
    _rechazo(url_api, "2026-07-06", "2026-07-16", 400,
             "La solicitud excede los días disponibles: quedan 8 días hábiles", previas=(P4,))


def test_cp_66(url_api):
    """CP-66: Enviar una solicitud de un empleado con poca antigüedad muestra el detail exacto."""
    _rechazo(url_api, "2026-07-06", "2026-07-10", 400, SIN_ANTIGUEDAD, ingreso="2026-01-15")


def test_cp_67(url_api):
    """CP-67: Enviar un periodo sin días hábiles muestra el detail exacto."""
    _rechazo(url_api, "2026-07-11", "2026-07-12", 400, SIN_HABILES)
