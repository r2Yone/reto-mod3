export default function TablaEmpleados({
  empleados,
  departamentos = [],
  busqueda,
  alCambiarBusqueda,
  filtroDepto,
  alCambiarFiltro,
  alEditar,
  alDarDeBaja,
  alSolicitarVacaciones,
}) {
  return (
    <section>
      <h2>Directorio</h2>
      <div>
        <input
          type="text"
          data-testid="buscar-empleados"
          placeholder="Buscar por nombre o correo"
          value={busqueda}
          onChange={(ev) => alCambiarBusqueda(ev.target.value)}
        />
        <select
          data-testid="filtro-departamento"
          value={filtroDepto}
          onChange={(ev) => alCambiarFiltro(ev.target.value)}
        >
          <option value="">Todos</option>
          {departamentos.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </div>
      <table data-testid="tabla-empleados">
        <thead>
          <tr>
            <th>Número</th>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Puesto</th>
            <th>Departamento</th>
            <th>Ingreso</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {empleados.map((e) => (
            <tr key={e.id} data-testid={`fila-empleado-${e.id}`}>
              <td data-testid={`numero-empleado-${e.id}`}>{e.numero_empleado}</td>
              <td>{e.nombre}</td>
              <td>{e.correo}</td>
              <td>{e.puesto}</td>
              <td>{e.departamento}</td>
              <td>{e.fecha_ingreso}</td>
              <td data-testid={`estado-empleado-${e.id}`}>
                {e.estado === "baja" ? "Baja" : "Activo"}
              </td>
              <td>
                {e.estado !== "baja" && (
                  <>
                    <button data-testid={`editar-empleado-${e.id}`} onClick={() => alEditar(e)}>
                      Editar
                    </button>
                    <button data-testid={`baja-empleado-${e.id}`} onClick={() => alDarDeBaja(e)}>
                      Dar de baja
                    </button>
                    <button
                      data-testid={`vacaciones-abrir-${e.id}`}
                      onClick={() => alSolicitarVacaciones(e)}
                    >
                      Solicitar vacaciones
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {empleados.length === 0 && (
        <p data-testid="sin-resultados">No se encontraron empleados con esos criterios</p>
      )}
    </section>
  );
}
