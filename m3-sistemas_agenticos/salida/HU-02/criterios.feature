# language: es
Característica: Consultar el directorio de empleados
  Como persona del área de Recursos Humanos
  quiero ver el directorio, buscar por nombre o correo y filtrar por departamento
  para encontrar rápido a una persona

  Antecedentes:
    Dado que existen los siguientes empleados:
      | numero_empleado | nombre       | correo                  | puesto              | departamento     | estado |
      | EMP-0001        | Ana García   | ana.garcia@empresa.com  | Desarrolladora      | Tecnología       | activo |
      | EMP-0002        | Luis Pérez   | luis.perez@empresa.com  | Ejecutivo de ventas | Ventas           | activo |
      | EMP-0003        | Marta Ruiz   | marta.ruiz@empresa.com  | Analista contable   | Finanzas         | baja   |
      | EMP-0004        | Carlos Soto  | carlos.soto@empresa.com | Reclutador          | Recursos Humanos | activo |

  Escenario: Ver el directorio completo
    Dado que la persona de RR. HH. está en la pantalla del directorio sin búsqueda ni filtro
    Cuando se carga el listado
    Entonces ve 4 empleados
    Y cada fila muestra número de empleado, nombre, puesto, departamento y estado
    Y la fila de "Ana García" muestra "EMP-0001", "Ana García", "Desarrolladora", "Tecnología" y "activo"

  Escenario: Un empleado dado de baja sigue apareciendo en el directorio
    Dado que "Marta Ruiz" con número "EMP-0003" tiene estado "baja"
    Cuando la persona de RR. HH. abre el directorio sin búsqueda ni filtro
    Entonces ve la fila de "Marta Ruiz" con número "EMP-0003" y estado "baja"

  Escenario: Buscar por nombre
    Dado que la persona de RR. HH. está en la pantalla del directorio
    Cuando busca "Luis Pérez"
    Entonces ve 1 empleado
    Y la fila es la de "EMP-0002"

  Escenario: Buscar por correo
    Dado que la persona de RR. HH. está en la pantalla del directorio
    Cuando busca "carlos.soto@empresa.com"
    Entonces ve 1 empleado
    Y la fila es la de "EMP-0004"

  Escenario: La búsqueda por nombre no distingue mayúsculas de minúsculas
    Dado que la persona de RR. HH. está en la pantalla del directorio
    Cuando busca "ANA GARCÍA"
    Entonces ve 1 empleado
    Y la fila es la de "EMP-0001"

  Escenario: La búsqueda por correo no distingue mayúsculas de minúsculas
    Dado que la persona de RR. HH. está en la pantalla del directorio
    Cuando busca "Marta.Ruiz@EMPRESA.COM"
    Entonces ve 1 empleado
    Y la fila es la de "EMP-0003"

  Escenario: Filtrar por departamento
    Dado que la persona de RR. HH. está en la pantalla del directorio
    Cuando filtra por el departamento "Ventas"
    Entonces ve 1 empleado
    Y la fila es la de "EMP-0002" con departamento "Ventas"

  Escenario: Filtrar por un departamento que incluye empleados dados de baja
    Dado que "Marta Ruiz" del departamento "Finanzas" tiene estado "baja"
    Cuando la persona de RR. HH. filtra por el departamento "Finanzas"
    Entonces ve 1 empleado
    Y la fila es la de "EMP-0003" con estado "baja"

  Escenario: Filtrar por un departamento sin empleados
    Dado que ningún empleado pertenece al departamento "Operaciones"
    Cuando la persona de RR. HH. filtra por el departamento "Operaciones"
    Entonces ve 0 empleados
    Y se muestra un mensaje indicando que no hay resultados

  Escenario: Búsqueda sin resultados
    Dado que ningún empleado tiene nombre ni correo que coincida con "Zacarías Inexistente"
    Cuando la persona de RR. HH. busca "Zacarías Inexistente"
    Entonces ve 0 empleados
    Y se muestra un mensaje indicando que no hay resultados

  Escenario: Quitar la búsqueda restablece el listado
    Dado que la persona de RR. HH. buscó "Luis Pérez" y ve 1 empleado
    Cuando borra el texto de búsqueda
    Entonces ve 4 empleados

  # Preguntas abiertas
  # - ¿Cuál es el texto exacto del mensaje cuando no hay resultados? (la historia solo dice que debe decirlo)
  # - ¿La búsqueda es por coincidencia parcial (p. ej. "garc" encuentra a "Ana García") o solo por texto completo?
  # - ¿La búsqueda ignora acentos (p. ej. "garcia" encuentra a "García")?
  # - ¿Se pueden combinar búsqueda y filtro de departamento a la vez (ambos deben cumplirse)?
  # - ¿Qué orden tiene el listado (por número de empleado, por nombre)?
  # - ¿Hay paginación o un límite de filas? Si sí, ¿de cuántas?
  # - ¿Qué se muestra cuando el directorio está completamente vacío (sin empleados registrados)? ¿Es el mismo mensaje de "sin resultados"?
  # - ¿Cómo se quita el filtro de departamento (opción "Todos")? ¿Se necesita un texto concreto para esa opción?
  # - ¿La búsqueda también debe encontrar por número de empleado? La historia solo menciona nombre y correo.
