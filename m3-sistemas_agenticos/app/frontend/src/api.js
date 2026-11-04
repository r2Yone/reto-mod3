// Todas las llamadas usan rutas relativas (/api/...)

async function pedir(ruta, opciones) {
  const respuesta = await fetch(ruta, opciones);
  const cuerpo = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "Ocurrió un error inesperado");
  }
  return cuerpo;
}

export const listarEmpleados = ({ q, departamento } = {}) => {
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  if (departamento) params.set("departamento", departamento);
  const query = params.toString();
  return pedir(query ? `/api/empleados?${query}` : "/api/empleados");
};

export const listarDepartamentos = () => pedir("/api/departamentos");

export const editarEmpleado = (id, datos) =>
  pedir(`/api/empleados/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });

export const darDeBajaEmpleado = (id, fecha_baja) =>
  pedir(`/api/empleados/${id}/baja`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fecha_baja }),
  });

export const obtenerSaldoVacaciones = (id, anio) =>
  pedir(`/api/empleados/${id}/vacaciones${anio ? `?anio=${anio}` : ""}`);

export const solicitarVacaciones = (id, datos) =>
  pedir(`/api/empleados/${id}/vacaciones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });

export const crearEmpleado =(datos) =>
  pedir("/api/empleados", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
