# language: es
Característica: Exportar la plantilla de empleados en CSV
  Como persona del área de Recursos Humanos
  quiero descargar el directorio de empleados en CSV
  para compartirlo con el área de nómina

  Escenario: Descargar el directorio con empleados activos
    Dado que existen los siguientes empleados en el directorio:
      | numero_empleado | nombre     | correo                 | puesto              | departamento | estado |
      | EMP-0001        | Ana Torres | ana.torres@empresa.com | Desarrolladora      | Tecnología   | activo |
      | EMP-0002        | Luis Pérez | luis.perez@empresa.com | Ejecutivo de ventas | Ventas       | activo |
    Cuando la persona de Recursos Humanos pulsa la opción de exportar el directorio en CSV
    Entonces se descarga un archivo con extensión .csv
    Y el archivo contiene una fila por cada empleado del directorio, es decir 2 filas de datos
    Y cada fila incluye, en este orden, número de empleado, nombre, puesto, departamento y estado
    Y la fila de EMP-0001 contiene los valores "EMP-0001", "Ana Torres", "Desarrolladora", "Tecnología" y "activo"
    Y la fila de EMP-0002 contiene los valores "EMP-0002", "Luis Pérez", "Ejecutivo de ventas", "Ventas" y "activo"

  Escenario: El archivo no incluye datos fuera de los acordados
    Dado que existen los siguientes empleados en el directorio:
      | numero_empleado | nombre     | correo                 | puesto              | departamento | estado |
      | EMP-0001        | Ana Torres | ana.torres@empresa.com | Desarrolladora      | Tecnología   | activo |
      | EMP-0002        | Luis Pérez | luis.perez@empresa.com | Ejecutivo de ventas | Ventas       | activo |
    Cuando la persona de Recursos Humanos exporta el directorio en CSV
    Entonces el archivo contiene exactamente 5 columnas
    Y el archivo no contiene el correo "ana.torres@empresa.com" ni "luis.perez@empresa.com"

  Escenario: Un empleado dado de baja sigue apareciendo en la exportación
    Dado que existen los siguientes empleados en el directorio:
      | numero_empleado | nombre     | correo                 | puesto              | departamento | estado |
      | EMP-0001        | Ana Torres | ana.torres@empresa.com | Desarrolladora      | Tecnología   | activo |
      | EMP-0002        | Luis Pérez | luis.perez@empresa.com | Ejecutivo de ventas | Ventas       | baja   |
    Cuando la persona de Recursos Humanos exporta el directorio en CSV
    Entonces el archivo contiene 2 filas de datos
    Y la fila de EMP-0002 contiene el estado "baja"
    Y la fila de EMP-0001 contiene el estado "activo"

  # Notas de alcance
  # - Por la regla 7 la aplicación no tiene inicio de sesión, por lo que no se define escenario de acceso no autorizado.
  # - La exportación es de solo lectura; las reglas de registro, edición y validación de correo/fechas (reglas 1, 2, 3, 4 y 6) no aplican a esta historia.
  # - La regla 5 (la baja no borra al empleado) sí aplica y se cubre en el tercer escenario.

  # Preguntas abiertas
  # - ¿Cuál es la ruta del endpoint o la ubicación del botón de exportación en pantalla?
  # - ¿Cuál es el nombre del archivo descargado (por ejemplo, con fecha)?
  # - ¿Cómo deben llamarse exactamente los encabezados de las columnas y el CSV lleva fila de encabezados?
  # - ¿Qué separador (coma o punto y coma) y qué codificación (UTF-8 con BOM para acentos en Excel) debe usar el archivo?
  # - ¿Qué debe ocurrir si el directorio está vacío: archivo solo con encabezados o un mensaje?
  # - ¿Se exportan todos los empleados o se debe poder filtrar (por estado o departamento)?
  # - ¿Cuál es el orden de las filas (por número de empleado, por nombre)?
  # - ¿Se incluye la fecha de baja para los empleados dados de baja? (la nota del dueño solo lista 5 campos)
