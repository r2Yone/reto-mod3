# language: es

Característica: Editar y dar de baja a un empleado
  Como persona del área de Recursos Humanos
  quiero cambiar el puesto y el departamento de un empleado, y poder darlo de baja
  para mantener el directorio al día sin perder el historial

  # ---------- Edición: camino feliz ----------

  Escenario: Cambiar el puesto y el departamento de un empleado activo
    Dado que existe el empleado "EMP-0001" con nombre "Ana Torres", correo "ana.torres@empresa.com", puesto "Analista", departamento "Ventas", fecha de ingreso "2023-03-01" y estado "activo"
    Cuando edito al empleado "EMP-0001" con puesto "Líder de Finanzas" y departamento "Finanzas"
    Entonces la respuesta es exitosa
    Y el empleado "EMP-0001" muestra puesto "Líder de Finanzas" y departamento "Finanzas"
    Y el estado del empleado sigue siendo "activo"

  Escenario: El número de empleado y el correo permanecen iguales tras editar
    Dado que existe el empleado "EMP-0001" con nombre "Ana Torres", correo "ana.torres@empresa.com", puesto "Analista", departamento "Ventas", fecha de ingreso "2023-03-01" y estado "activo"
    Cuando edito al empleado "EMP-0001" con puesto "Líder de Finanzas" y departamento "Finanzas"
    Entonces el empleado conserva el número de empleado "EMP-0001"
    Y el empleado conserva el correo "ana.torres@empresa.com"

  # ---------- Edición: datos inválidos (regla 3) ----------

  Escenario: Rechazar un puesto de 1 carácter
    Dado que existe el empleado "EMP-0001" con puesto "Analista", departamento "Ventas" y estado "activo"
    Cuando edito al empleado "EMP-0001" con puesto "A" y departamento "Ventas"
    Entonces la respuesta es 422
    Y la pantalla indica que debo corregir el campo "puesto"
    Y el puesto del empleado "EMP-0001" sigue siendo "Analista"

  Escenario: Rechazar un puesto de 61 caracteres
    Dado que existe el empleado "EMP-0001" con puesto "Analista", departamento "Ventas" y estado "activo"
    Cuando edito al empleado "EMP-0001" con un puesto de 61 caracteres y departamento "Ventas"
    Entonces la respuesta es 422
    Y la pantalla indica que debo corregir el campo "puesto"
    Y el puesto del empleado "EMP-0001" sigue siendo "Analista"

  Escenario: Rechazar un puesto vacío
    Dado que existe el empleado "EMP-0001" con puesto "Analista", departamento "Ventas" y estado "activo"
    Cuando edito al empleado "EMP-0001" con puesto "" y departamento "Ventas"
    Entonces la respuesta es 422
    Y la pantalla indica que debo corregir el campo "puesto"
    Y el puesto del empleado "EMP-0001" sigue siendo "Analista"

  Escenario: Rechazar un departamento que no está en la lista
    Dado que existe el empleado "EMP-0001" con puesto "Analista", departamento "Ventas" y estado "activo"
    Cuando edito al empleado "EMP-0001" con puesto "Analista" y departamento "Marketing"
    Entonces la respuesta es 422
    Y la pantalla indica que debo corregir el campo "departamento"
    Y el departamento del empleado "EMP-0001" sigue siendo "Ventas"

  # ---------- Baja: camino feliz (regla 5) ----------

  Escenario: Dar de baja a un empleado activo
    Dado que existe el empleado "EMP-0001" con nombre "Ana Torres", fecha de ingreso "2023-03-01" y estado "activo"
    Cuando doy de baja al empleado "EMP-0001" con fecha de baja "2024-06-30"
    Entonces la respuesta es exitosa
    Y el estado del empleado "EMP-0001" es "baja"
    Y la fecha de baja del empleado "EMP-0001" es "2024-06-30"

  Escenario: El empleado dado de baja sigue apareciendo en el directorio
    Dado que existe el empleado "EMP-0001" con nombre "Ana Torres", fecha de ingreso "2023-03-01" y estado "activo"
    Cuando doy de baja al empleado "EMP-0001" con fecha de baja "2024-06-30"
    Y consulto el directorio de empleados
    Entonces el directorio incluye a "EMP-0001" "Ana Torres" marcado como "Baja"

  Escenario: Dar de baja con fecha igual a la fecha de ingreso
    Dado que existe el empleado "EMP-0001" con fecha de ingreso "2023-03-01" y estado "activo"
    Cuando doy de baja al empleado "EMP-0001" con fecha de baja "2023-03-01"
    Entonces la respuesta es exitosa
    Y el estado del empleado "EMP-0001" es "baja"
    Y la fecha de baja del empleado "EMP-0001" es "2023-03-01"

  # ---------- Baja: fecha inválida ----------

  Escenario: Rechazar una fecha de baja anterior a la fecha de ingreso
    Dado que existe el empleado "EMP-0001" con fecha de ingreso "2023-03-01" y estado "activo"
    Cuando doy de baja al empleado "EMP-0001" con fecha de baja "2023-02-28"
    Entonces la respuesta es 422
    Y la pantalla indica que debo corregir el campo "fecha de baja"
    Y el estado del empleado "EMP-0001" sigue siendo "activo"
    Y el empleado "EMP-0001" no tiene fecha de baja

  # ---------- Empleado dado de baja no se edita (regla 6) ----------

  Escenario: No se puede editar a un empleado dado de baja
    Dado que existe el empleado "EMP-0001" con puesto "Analista" y departamento "Ventas"
    Y el empleado "EMP-0001" está dado de baja con fecha de baja "2024-06-30"
    Cuando edito al empleado "EMP-0001" con puesto "Gerente" y departamento "Operaciones"
    Entonces la respuesta es 409
    Y el mensaje es "No se puede editar a un empleado dado de baja"
    Y el puesto del empleado "EMP-0001" sigue siendo "Analista"
    Y el departamento del empleado "EMP-0001" sigue siendo "Ventas"

# Preguntas abiertas
# - ¿Quién define la fecha de baja: la elige RR. HH. o el sistema usa la fecha del día? Los escenarios asumen que RR. HH. la indica.
# - ¿Puede la fecha de baja ser futura? Las reglas solo prohíben que sea anterior al ingreso.
# - ¿Qué mensaje se muestra cuando la fecha de baja es anterior a la de ingreso? Solo se sabe que aplica la regla 3 (422, campo a corregir).
# - ¿Qué responde el sistema si se intenta enviar un cambio de número de empleado o de correo (se ignora el dato o se rechaza con un error)? Las notas solo dicen que no son editables.
# - ¿Qué ocurre al dar de baja a un empleado que ya está en baja (error, o se ignora)? No hay regla definida.
# - ¿Se puede editar solo uno de los dos campos (solo puesto o solo departamento) o siempre se envían ambos?
# - ¿Se puede revertir una baja (reactivar al empleado)? No se menciona.
# - ¿Qué responde el sistema al editar o dar de baja un id/número de empleado que no existe (404)? No hay regla definida.
