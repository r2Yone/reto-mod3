import { useCallback, useEffect, useState } from "react";
import { listarDepartamentos, listarEmpleados } from "./api.js";
import FormularioEmpleado from "./componentes/FormularioEmpleado.jsx";
import FormularioBaja from "./componentes/FormularioBaja.jsx";
import TablaEmpleados from "./componentes/TablaEmpleados.jsx";

export default function App() {
  const [empleados, setEmpleados] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [empleadoEnEdicion, setEmpleadoEnEdicion] = useState(null);
  const [empleadoEnBaja, setEmpleadoEnBaja] = useState(null);

  const [busqueda, setBusqueda] = useState("");
  const [filtroDepto, setFiltroDepto] = useState("");
  // Cada recarga respeta la búsqueda y el filtro activos
  const recargar = useCallback(async () => {
    setEmpleados(await listarEmpleados({ q: busqueda, departamento: filtroDepto }));
  }, [busqueda, filtroDepto]);

  useEffect(() => {
    // La bandera evita que una respuesta lenta pise a una más reciente
    let cancelado = false;
    listarEmpleados({ q: busqueda, departamento: filtroDepto })
      .then((datos) => {
        if (!cancelado) setEmpleados(datos);
      })
      .catch(() => {});
    return () => {
      cancelado = true;
    };
  }, [busqueda, filtroDepto]);

  useEffect(() => {
    listarDepartamentos().then(setDepartamentos).catch(() => {});
  }, []);

  return (
    <main>
      <h1>Gestión de empleados</h1>
      {empleadoEnBaja ? (
        <FormularioBaja
          key={`baja-${empleadoEnBaja.id}`}
          empleado={empleadoEnBaja}
          alGuardar={recargar}
          alCancelar={() => setEmpleadoEnBaja(null)}
        />
      ) : (
        // La key reinicia el formulario al pasar de registro a edición (y entre empleados)
        <FormularioEmpleado
          key={empleadoEnEdicion ? `editar-${empleadoEnEdicion.id}` : "nuevo"}
          departamentos={departamentos}
          alGuardar={recargar}
          empleado={empleadoEnEdicion}
          alCancelar={() => setEmpleadoEnEdicion(null)}
        />
      )}
      <TablaEmpleados
        alEditar={(e) => {
          setEmpleadoEnBaja(null);
          setEmpleadoEnEdicion(e);
        }}
        alDarDeBaja={(e) => {
          setEmpleadoEnEdicion(null);
          setEmpleadoEnBaja(e);
        }}
        empleados={empleados}
        departamentos={departamentos}
        busqueda={busqueda}
        alCambiarBusqueda={setBusqueda}
        filtroDepto={filtroDepto}
        alCambiarFiltro={setFiltroDepto}
      />
    </main>
  );
}
