# language: es
Característica: Solicitar vacaciones
  Como empleado de la empresa
  Quiero solicitar días de vacaciones indicando una fecha de inicio y una de fin
  Para que mi solicitud quede registrada y sepa cuántos días me quedan en el año

  # ============================================================
  # Camino feliz y conteo de días hábiles
  # ============================================================

  Escenario: Solicitud válida de cinco días hábiles sin vacaciones previas
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-10"
    Entonces la API responde 201
    Y la respuesta trae empleado_id 7, fecha_inicio "2026-07-06", fecha_fin "2026-07-10", dias_habiles 5 y dias_restantes 7

  Escenario: Cumple exactamente un año de antigüedad el día de inicio y el periodo tiene un festivo y dos fines de semana
    Dado un empleado activo con id 8 y fecha_ingreso "2025-12-21"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/8/vacaciones con fecha_inicio "2026-12-21" y fecha_fin "2026-12-31"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 8 y dias_restantes 4

  Escenario: Se usa exactamente lo que queda con 5 días usados y una solicitud de 7 días hábiles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene una solicitud registrada del "2026-07-06" al "2026-07-10" de 5 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-13" y fecha_fin "2026-07-21"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 7 y dias_restantes 0

  Escenario: Se usa exactamente lo que queda con 4 días usados y una solicitud de 8 días hábiles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene una solicitud registrada del "2026-06-01" al "2026-06-04" de 4 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-15"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 8 y dias_restantes 0

  Escenario: Un periodo de un solo día hábil donde la fecha de fin es igual a la de inicio
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-06"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 1 y dias_restantes 11

  Escenario: Un fin de semana dentro del periodo no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-10" y fecha_fin "2026-07-13"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 2 y dias_restantes 10

  Escenario: El 16 de septiembre de 2026 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-09-14" y fecha_fin "2026-09-18"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: Año Nuevo de 2026 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-01-01" y fecha_fin "2026-01-02"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 1 y dias_restantes 11

  Escenario: El Día de la Constitución de 2026 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-02-02" y fecha_fin "2026-02-06"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: El natalicio de Benito Juárez de 2026 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-03-16" y fecha_fin "2026-03-20"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: El Día del Trabajo de 2026 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-04-27" y fecha_fin "2026-05-01"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: La Revolución Mexicana de 2026 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-11-16" y fecha_fin "2026-11-20"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: Un festivo que cae en sábado no se recorre al viernes ni al lunes en 2027
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-04-30" y fecha_fin "2027-05-03"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 2 y dias_restantes 10

  Escenario: La Navidad de 2027 cae en sábado y no se recorre
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-12-24" y fecha_fin "2027-12-27"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 2 y dias_restantes 10

  Escenario: El Día de la Constitución de 2027 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-02-01" y fecha_fin "2027-02-05"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: El natalicio de Benito Juárez de 2027 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-03-15" y fecha_fin "2027-03-19"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: El 16 de septiembre de 2027 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-09-13" y fecha_fin "2027-09-17"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: La Revolución Mexicana de 2027 no se descuenta
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-11-15" y fecha_fin "2027-11-19"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 4 y dias_restantes 8

  Escenario: Dos solicitudes del mismo año acumulan sus días usados
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene una solicitud registrada del "2026-07-06" al "2026-07-10" de 5 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-13" y fecha_fin "2026-07-17"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 5 y dias_restantes 2

  Escenario: El último día hábil del año 2026 es una solicitud válida
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-12-31" y fecha_fin "2026-12-31"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 1 y dias_restantes 11

  Escenario: El último día hábil del año 2027 es una solicitud válida
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-12-31" y fecha_fin "2027-12-31"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 1 y dias_restantes 11

  # ============================================================
  # Regla 3: periodo sin días hábiles
  # ============================================================

  Escenario: Un sábado y un domingo no tienen días hábiles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-11" y fecha_fin "2026-07-12"
    Entonces la API responde 400
    Y el detail es "El periodo no incluye días hábiles"

  Escenario: Un periodo de un solo día festivo (16 de septiembre de 2026) no tiene días hábiles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-09-16" y fecha_fin "2026-09-16"
    Entonces la API responde 400
    Y el detail es "El periodo no incluye días hábiles"

  Escenario: Un periodo de un solo día festivo (25 de diciembre de 2026) no tiene días hábiles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-12-25" y fecha_fin "2026-12-25"
    Entonces la API responde 400
    Y el detail es "El periodo no incluye días hábiles"

  Escenario: Un periodo de un solo día festivo (1 de enero de 2026) no tiene días hábiles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-01-01" y fecha_fin "2026-01-01"
    Entonces la API responde 400
    Y el detail es "El periodo no incluye días hábiles"

  Escenario: Un periodo de un solo día festivo (1 de enero de 2027) no tiene días hábiles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-01-01" y fecha_fin "2027-01-01"
    Entonces la API responde 400
    Y el detail es "El periodo no incluye días hábiles"

  Escenario: Un festivo en sábado seguido de domingo no tiene días hábiles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-05-01" y fecha_fin "2027-05-02"
    Entonces la API responde 400
    Y el detail es "El periodo no incluye días hábiles"

  Escenario: Sin días hábiles se rechaza aunque el empleado ya no tenga días disponibles
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene solicitudes registradas en 2026 que suman 12 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-11" y fecha_fin "2026-07-12"
    Entonces la API responde 400
    Y el detail es "El periodo no incluye días hábiles"

  # ============================================================
  # Regla 2: tope anual
  # ============================================================

  Escenario: Se rechaza una solicitud de 9 días hábiles cuando quedan 8
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene una solicitud registrada del "2026-06-01" al "2026-06-04" de 4 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-16"
    Entonces la API responde 400
    Y el detail es "La solicitud excede los días disponibles: quedan 8 días hábiles"

  Escenario: Se rechaza cualquier periodo con días hábiles cuando ya se usaron los 12 días
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene solicitudes registradas en 2026 que suman 12 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-08-03" y fecha_fin "2026-08-03"
    Entonces la API responde 400
    Y el detail es "La solicitud excede los días disponibles: quedan 0 días hábiles"

  Escenario: Se rechaza pasarse por un día cuando queda 1 y se escribe días hábiles en plural
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene solicitudes registradas en 2026 que suman 11 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-08-03" y fecha_fin "2026-08-04"
    Entonces la API responde 400
    Y el detail es "La solicitud excede los días disponibles: quedan 1 días hábiles"

  Escenario: Se acepta el último día disponible cuando quedan exactamente 1
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene solicitudes registradas en 2026 que suman 11 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-08-03" y fecha_fin "2026-08-03"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 1 y dias_restantes 0

  Escenario: Una solicitud de 13 días hábiles supera el tope de 12 de un empleado sin vacaciones previas
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-08-03" y fecha_fin "2026-08-19"
    Entonces la API responde 400
    Y el detail es "La solicitud excede los días disponibles: quedan 12 días hábiles"

  Escenario: Una solicitud de 12 días hábiles usa el tope completo
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-08-03" y fecha_fin "2026-08-18"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 12 y dias_restantes 0

  Escenario: Los días usados en 2026 no restan del saldo de 2027
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene solicitudes registradas en 2026 que suman 12 días hábiles
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-07-05" y fecha_fin "2027-07-09"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 5 y dias_restantes 7

  # ============================================================
  # Regla 1: antigüedad
  # ============================================================

  Escenario: Se rechaza a quien ingresó el 2025-12-21 con inicio el 2026-12-18
    Dado un empleado activo con id 8 y fecha_ingreso "2025-12-21"
    Cuando envía POST /api/empleados/8/vacaciones con fecha_inicio "2026-12-18" y fecha_fin "2026-12-18"
    Entonces la API responde 400
    Y el detail es "Se requiere al menos un año de antigüedad a la fecha de inicio"

  Escenario: Se rechaza a quien ingresó el 2025-12-21 con inicio un día antes del aniversario
    Dado un empleado activo con id 8 y fecha_ingreso "2025-12-21"
    Cuando envía POST /api/empleados/8/vacaciones con fecha_inicio "2026-12-20" y fecha_fin "2026-12-22"
    Entonces la API responde 400
    Y el detail es "Se requiere al menos un año de antigüedad a la fecha de inicio"

  Escenario: Se rechaza a un empleado con pocos meses de antigüedad
    Dado un empleado activo con id 9 y fecha_ingreso "2026-01-15"
    Cuando envía POST /api/empleados/9/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-10"
    Entonces la API responde 400
    Y el detail es "Se requiere al menos un año de antigüedad a la fecha de inicio"

  Escenario: Se acepta a quien ingresó el 2024-03-10 con inicio el 2026-07-06
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-06"
    Entonces la API responde 201
    Y la respuesta trae dias_habiles 1 y dias_restantes 11

  # ============================================================
  # Fechas inválidas, año calendario y años fuera de la tabla
  # ============================================================

  Escenario: Se rechaza una fecha de fin un día anterior a la de inicio
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-10" y fecha_fin "2026-07-09"
    Entonces la API responde 400
    Y el detail es "La fecha de fin no puede ser anterior a la fecha de inicio"

  Escenario: Se rechaza un periodo que cruza de diciembre de 2026 a enero de 2027
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-12-28" y fecha_fin "2027-01-08"
    Entonces la API responde 400
    Y el detail es "Las vacaciones deben estar dentro de un mismo año calendario"

  Escenario: Se rechaza un periodo que cruza el año por un solo día
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-12-31" y fecha_fin "2027-01-01"
    Entonces la API responde 400
    Y el detail es "Las vacaciones deben estar dentro de un mismo año calendario"

  Escenario: Un periodo que cruza de 2027 a 2028 se rechaza por cruzar el año y no por el año fuera de la tabla
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2027-12-31" y fecha_fin "2028-01-03"
    Entonces la API responde 400
    Y el detail es "Las vacaciones deben estar dentro de un mismo año calendario"

  Escenario: Se rechaza un periodo en 2028 porque el año no está en la tabla de festivos
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2028-01-10" y fecha_fin "2028-01-14"
    Entonces la API responde 400
    Y el detail es "Solo se pueden solicitar vacaciones en 2026 y 2027"

  Escenario: Se rechaza el primer día hábil después de 2027
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2028-01-03" y fecha_fin "2028-01-03"
    Entonces la API responde 400
    Y el detail es "Solo se pueden solicitar vacaciones en 2026 y 2027"

  Escenario: Se rechaza un periodo en 2025 porque el año no está en la tabla de festivos
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2025-12-15" y fecha_fin "2025-12-19"
    Entonces la API responde 400
    Y el detail es "Solo se pueden solicitar vacaciones en 2026 y 2027"

  Escenario: Se rechaza el último día de 2025
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2025-12-31" y fecha_fin "2025-12-31"
    Entonces la API responde 400
    Y el detail es "Solo se pueden solicitar vacaciones en 2026 y 2027"

  Escenario: Una fecha con formato inválido se rechaza con el 422 automático de FastAPI
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "21-12-2026" y fecha_fin "2026-12-31"
    Entonces la API responde 422

  # ============================================================
  # Empleado inexistente o dado de baja
  # ============================================================

  Escenario: Se rechaza un empleado que no existe
    Dado que no existe ningún empleado con id 9999
    Cuando envía POST /api/empleados/9999/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-10"
    Entonces la API responde 404
    Y el detail es "Empleado no encontrado"

  Escenario: Se rechaza un empleado dado de baja
    Dado un empleado con id 10, fecha_ingreso "2024-03-10" y estado "baja"
    Cuando envía POST /api/empleados/10/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-10"
    Entonces la API responde 409
    Y el detail es "No se pueden solicitar vacaciones para un empleado dado de baja"

  # ============================================================
  # Orden de validación: se devuelve el primer error que aplique
  # ============================================================

  Escenario: El empleado inexistente se valida antes que las fechas
    Dado que no existe ningún empleado con id 9999
    Cuando envía POST /api/empleados/9999/vacaciones con fecha_inicio "2026-07-10" y fecha_fin "2026-07-09"
    Entonces la API responde 404
    Y el detail es "Empleado no encontrado"

  Escenario: El empleado dado de baja se valida antes que las fechas
    Dado un empleado con id 10, fecha_ingreso "2024-03-10" y estado "baja"
    Cuando envía POST /api/empleados/10/vacaciones con fecha_inicio "2026-07-10" y fecha_fin "2026-07-09"
    Entonces la API responde 409
    Y el detail es "No se pueden solicitar vacaciones para un empleado dado de baja"

  Escenario: La fecha de fin anterior se valida antes que la antigüedad
    Dado un empleado activo con id 9 y fecha_ingreso "2026-01-15"
    Cuando envía POST /api/empleados/9/vacaciones con fecha_inicio "2026-07-10" y fecha_fin "2026-07-09"
    Entonces la API responde 400
    Y el detail es "La fecha de fin no puede ser anterior a la fecha de inicio"

  Escenario: El año fuera de la tabla se valida antes que la antigüedad
    Dado un empleado activo con id 11 y fecha_ingreso "2027-06-01"
    Cuando envía POST /api/empleados/11/vacaciones con fecha_inicio "2028-01-10" y fecha_fin "2028-01-14"
    Entonces la API responde 400
    Y el detail es "Solo se pueden solicitar vacaciones en 2026 y 2027"

  Escenario: La antigüedad se valida antes que los días hábiles
    Dado un empleado activo con id 9 y fecha_ingreso "2026-01-15"
    Cuando envía POST /api/empleados/9/vacaciones con fecha_inicio "2026-07-11" y fecha_fin "2026-07-12"
    Entonces la API responde 400
    Y el detail es "Se requiere al menos un año de antigüedad a la fecha de inicio"

  # ============================================================
  # Consulta del saldo del año
  # ============================================================

  Escenario: Consultar el saldo de 2026 con una solicitud de 8 días hábiles
    Dado un empleado activo con id 8 y fecha_ingreso "2025-12-21"
    Y que el empleado tiene una solicitud registrada con id 1 del "2026-12-21" al "2026-12-31" de 8 días hábiles
    Cuando consulta GET /api/empleados/8/vacaciones?anio=2026
    Entonces la API responde 200
    Y la respuesta trae empleado_id 8, anio 2026, dias_usados 8 y dias_disponibles 4
    Y solicitudes contiene un elemento con id 1, fecha_inicio "2026-12-21", fecha_fin "2026-12-31" y dias_habiles 8

  Escenario: Consultar el saldo de un año sin solicitudes
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2027
    Cuando consulta GET /api/empleados/7/vacaciones?anio=2027
    Entonces la API responde 200
    Y la respuesta trae anio 2027, dias_usados 0, dias_disponibles 12 y solicitudes vacía

  Escenario: Consultar el saldo sin indicar el año usa el año en curso
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el año en curso es 2026
    Y que el empleado tiene una solicitud registrada del "2026-07-06" al "2026-07-10" de 5 días hábiles
    Cuando consulta GET /api/empleados/7/vacaciones sin el parámetro anio
    Entonces la API responde 200
    Y la respuesta trae anio 2026, dias_usados 5 y dias_disponibles 7

  Escenario: Una solicitud rechazada no se registra ni descuenta días
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene una solicitud registrada del "2026-06-01" al "2026-06-04" de 4 días hábiles
    Cuando envía POST /api/empleados/7/vacaciones con fecha_inicio "2026-07-06" y fecha_fin "2026-07-16" y recibe 400
    Y consulta GET /api/empleados/7/vacaciones?anio=2026
    Entonces la respuesta trae dias_usados 4 y dias_disponibles 8
    Y solicitudes contiene un solo elemento

  # ============================================================
  # Pantalla
  # ============================================================

  Escenario: Un empleado activo tiene el botón Solicitar vacaciones
    Dado un empleado activo con id 7 en el directorio de empleados
    Cuando el usuario abre el directorio
    Entonces ve el botón "Solicitar vacaciones" con data-testid "vacaciones-abrir-7"

  Escenario: Un empleado dado de baja no tiene el botón Solicitar vacaciones
    Dado un empleado con id 10 y estado "baja" en el directorio de empleados
    Cuando el usuario abre el directorio
    Entonces no existe el elemento con data-testid "vacaciones-abrir-10"

  Escenario: El formulario muestra 12 días disponibles para un empleado sin vacaciones en el año
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Cuando el usuario pulsa "vacaciones-abrir-7"
    Entonces el elemento "vacaciones-disponibles" muestra "12"

  Escenario: El formulario muestra 8 días disponibles para un empleado con 4 días usados
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene una solicitud registrada del "2026-06-01" al "2026-06-04" de 4 días hábiles
    Cuando el usuario pulsa "vacaciones-abrir-7"
    Entonces el elemento "vacaciones-disponibles" muestra "8"

  Escenario: Enviar una solicitud válida muestra el mensaje de éxito
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado no tiene solicitudes de vacaciones en 2026
    Y que el usuario abrió el formulario con "vacaciones-abrir-7"
    Cuando escribe "2026-07-06" en "vacaciones-fecha-inicio", "2026-07-10" en "vacaciones-fecha-fin" y pulsa "vacaciones-enviar"
    Entonces "vacaciones-mensaje" muestra "Solicitud registrada: 5 días hábiles. Te quedan 7 días hábiles en 2026."

  Escenario: Enviar una solicitud que excede el saldo muestra el detail exacto
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el empleado tiene una solicitud registrada del "2026-06-01" al "2026-06-04" de 4 días hábiles
    Y que el usuario abrió el formulario con "vacaciones-abrir-7"
    Cuando escribe "2026-07-06" en "vacaciones-fecha-inicio", "2026-07-16" en "vacaciones-fecha-fin" y pulsa "vacaciones-enviar"
    Entonces "vacaciones-mensaje" muestra "La solicitud excede los días disponibles: quedan 8 días hábiles"

  Escenario: Enviar una solicitud de un empleado con poca antigüedad muestra el detail exacto
    Dado un empleado activo con id 9 y fecha_ingreso "2026-01-15"
    Y que el usuario abrió el formulario con "vacaciones-abrir-9"
    Cuando escribe "2026-07-06" en "vacaciones-fecha-inicio", "2026-07-10" en "vacaciones-fecha-fin" y pulsa "vacaciones-enviar"
    Entonces "vacaciones-mensaje" muestra "Se requiere al menos un año de antigüedad a la fecha de inicio"

  Escenario: Enviar un periodo sin días hábiles muestra el detail exacto
    Dado un empleado activo con id 7 y fecha_ingreso "2024-03-10"
    Y que el usuario abrió el formulario con "vacaciones-abrir-7"
    Cuando escribe "2026-07-11" en "vacaciones-fecha-inicio", "2026-07-12" en "vacaciones-fecha-fin" y pulsa "vacaciones-enviar"
    Entonces "vacaciones-mensaje" muestra "El periodo no incluye días hábiles"

  # Preguntas abiertas
  # - La regla del 29 de febrero (aniversario el 1 de marzo en año no bisiesto) no se puede probar con datos concretos:
  #   el aniversario de un ingreso el 2024-02-29 cae en 2025-03-01 y 2025 queda fuera de los años permitidos (2026 y 2027).
  #   ¿Hay un caso de prueba esperado para esa regla dentro de 2026-2027?
  # - Si una consulta GET /api/empleados/{id}/vacaciones se hace para un empleado inexistente, se asume 404 "Empleado no encontrado"; el contexto no lo detalla.
