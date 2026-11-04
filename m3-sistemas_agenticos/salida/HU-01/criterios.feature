# language: es
Característica: Registrar empleado
  Como persona del área de Recursos Humanos
  Quiero registrar a un empleado con su nombre, correo corporativo, puesto, departamento y fecha de ingreso
  Para darlo de alta en la empresa

  # ---------- Camino feliz ----------

  Escenario: Registrar un empleado con datos válidos
    Dado que estoy en el formulario de registro de empleado
    Y no existe ningún empleado registrado
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@empresa.com", puesto "Analista", departamento "Finanzas" y fecha de ingreso de hace 5 días
    Entonces el sistema guarda al empleado con estado "activo"
    Y el sistema le asigna el número de empleado "EMP-0001"
    Y la pantalla muestra un mensaje de confirmación que incluye "EMP-0001"
    Y el registro tiene una fecha y hora de creación asignada por el sistema

  Escenario: El número de empleado es consecutivo
    Dado que estoy en el formulario de registro de empleado
    Y el último empleado registrado tiene el número "EMP-0007"
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@empresa.com", puesto "Analista", departamento "Finanzas" y fecha de ingreso de hoy
    Entonces el empleado queda guardado con el número "EMP-0008"
    Y el mensaje de confirmación muestra "EMP-0008"

  Escenario: El número de empleado no se captura en el formulario
    Dado que soy una persona del área de Recursos Humanos
    Cuando abro el formulario de registro de empleado
    Entonces el formulario muestra los campos nombre, correo, puesto, departamento y fecha de ingreso
    Y el formulario no tiene un campo para escribir el número de empleado

  Escenario: El correo se guarda en minúsculas
    Dado que estoy en el formulario de registro de empleado
    Y no existe ningún empleado con el correo "ana.lopez@empresa.com"
    Cuando registro un empleado con nombre "Ana López", correo "Ana.Lopez@Empresa.com", puesto "Analista", departamento "Finanzas" y fecha de ingreso de hoy
    Entonces el empleado queda guardado con el correo "ana.lopez@empresa.com"

  Escenario: Se acepta una fecha de ingreso igual a la fecha de hoy
    Dado que estoy en el formulario de registro de empleado
    Y no existe ningún empleado con el correo "ana.lopez@empresa.com"
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@empresa.com", puesto "Analista", departamento "Finanzas" y fecha de ingreso de hoy
    Entonces el sistema guarda al empleado con estado "activo"

  Escenario: Se aceptan nombre de 80 caracteres y puesto de 60 caracteres
    Dado que estoy en el formulario de registro de empleado
    Y no existe ningún empleado con el correo "ana.lopez@empresa.com"
    Cuando registro un empleado con un nombre de 80 caracteres, correo "ana.lopez@empresa.com", un puesto de 60 caracteres, departamento "Tecnología" y fecha de ingreso de hoy
    Entonces el sistema guarda al empleado con estado "activo"

  # ---------- Regla 1: correo único ----------

  Escenario: Rechazar un correo que ya está registrado
    Dado que estoy en el formulario de registro de empleado
    Y existe un empleado con el correo "ana.lopez@empresa.com"
    Cuando registro otro empleado con el correo "ana.lopez@empresa.com" y el resto de los datos válidos
    Entonces la API responde 409
    Y la pantalla muestra el mensaje "El correo ya está registrado"
    Y no se crea un nuevo empleado ni se consume un número de empleado

  Escenario: Rechazar un correo repetido que solo cambia en mayúsculas
    Dado que estoy en el formulario de registro de empleado
    Y existe un empleado con el correo "ana.lopez@empresa.com"
    Cuando registro otro empleado con el correo "ANA.LOPEZ@EMPRESA.COM" y el resto de los datos válidos
    Entonces la API responde 409
    Y la pantalla muestra el mensaje "El correo ya está registrado"
    Y no se crea un nuevo empleado

  # ---------- Regla 2: correo corporativo ----------

  Escenario: Rechazar un correo que no es del dominio corporativo
    Dado que estoy en el formulario de registro de empleado
    Y no existe ningún empleado con el correo "ana.lopez@gmail.com"
    Cuando registro un empleado con el correo "ana.lopez@gmail.com" y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla muestra el mensaje "Usa el correo corporativo @empresa.com"
    Y no se crea ningún empleado

  # ---------- Regla 3: otros datos inválidos ----------

  Escenario: Rechazar el registro sin correo
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado dejando el correo vacío y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "correo"
    Y no se crea ningún empleado

  Escenario: Rechazar el registro sin nombre
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado dejando el nombre vacío y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "nombre"
    Y no se crea ningún empleado

  Escenario: Rechazar un nombre de 1 carácter
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado con nombre "A" y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "nombre"

  Escenario: Rechazar un nombre de 81 caracteres
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado con un nombre de 81 caracteres y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "nombre"

  Escenario: Rechazar el registro sin puesto
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado dejando el puesto vacío y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "puesto"

  Escenario: Rechazar un puesto de 1 carácter
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado con puesto "A" y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "puesto"

  Escenario: Rechazar un puesto de 61 caracteres
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado con un puesto de 61 caracteres y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "puesto"

  Escenario: Rechazar un departamento que no está en la lista
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado con departamento "Marketing" y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "departamento"

  Escenario: Rechazar el registro sin fecha de ingreso
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado dejando la fecha de ingreso vacía y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla indica que debe corregirse el campo "fecha de ingreso"

  # ---------- Regla 4: fecha de ingreso futura ----------

  Escenario: Rechazar una fecha de ingreso futura
    Dado que estoy en el formulario de registro de empleado
    Cuando registro un empleado con fecha de ingreso de mañana y el resto de los datos válidos
    Entonces la API responde 422
    Y la pantalla muestra el mensaje "La fecha de ingreso no puede ser futura"
    Y no se crea ningún empleado

# Preguntas abiertas
# - ¿Cuál es el texto exacto del mensaje de confirmación? Solo se sabe que debe incluir el número asignado (ej. «Empleado registrado con número EMP-0008»).
# - ¿Qué mensaje exacto se muestra por campo en los errores 422 de nombre, puesto, departamento y fecha de ingreso vacía? Las reglas solo piden "mostrar qué campo corregir".
# - Un correo vacío, ¿responde con el mensaje de la regla 2 («Usa el correo corporativo @empresa.com») o con un mensaje de campo obligatorio?
# - ¿Se recortan los espacios al inicio y al final de nombre, puesto y correo antes de validar la longitud? ¿Un nombre de solo espacios cuenta como vacío?
# - ¿El departamento es obligatorio? La regla dice «uno de» la lista, pero no dice si puede quedar vacío; no se escribió escenario para departamento vacío.
# - ¿Qué pasa si el cliente envía un número de empleado en la API? ¿Se ignora o se rechaza con 422?
# - ¿Qué ocurre al superar EMP-9999 (el formato tiene 4 dígitos)?
# - ¿Hay un límite de antigüedad para la fecha de ingreso (por ejemplo, años atrás)? No está definido.
# - ¿Cuál es la zona horaria para decidir si una fecha es «futura»?
# - ¿Un correo sin parte local (por ejemplo "@empresa.com") se considera válido?
