import { useState } from "react";
import { crearEmpleado, editarEmpleado } from "../api.js";

const VACIO = { nombre: "", correo: "", puesto: "", departamento: "", fecha_ingreso: "" };

// Con `empleado` el formulario entra en modo edición: solo puesto y departamento cambian
export default function FormularioEmpleado({ departamentos, alGuardar, empleado, alCancelar }) {
  const editando = Boolean(empleado);
  const [datos, setDatos] = useState(empleado ?? VACIO);
  const [exito, setExito] = useState("");
  const [error, setError] = useState("");

  const cambiar = (campo) => (e) => setDatos({ ...datos, [campo]: e.target.value });

  async function enviar(e) {
    e.preventDefault();
    setExito("");
    setError("");
    try {
      if (editando) {
        const editado = await editarEmpleado(empleado.id, {
          puesto: datos.puesto,
          departamento: datos.departamento,
        });
        setExito(`Empleado actualizado: ${editado.numero_empleado}`);
      } else {
        const creado = await crearEmpleado(datos);
        setExito(`Empleado registrado: ${creado.numero_empleado}`);
        setDatos(VACIO);
      }
      await alGuardar();
    } catch (err) {
      setError(err.message);
    }
  }

  // noValidate: los errores los decide el backend, no el navegador
  return (
    <form onSubmit={enviar} noValidate>
      <h2>{editando ? `Editar empleado ${empleado.numero_empleado}` : "Registrar empleado"}</h2>
      <label>
        Nombre
        <input
          data-testid="empleado-nombre"
          value={datos.nombre}
          onChange={cambiar("nombre")}
          disabled={editando}
        />
      </label>
      <label>
        Correo
        <input
          data-testid="empleado-correo"
          value={datos.correo}
          onChange={cambiar("correo")}
          disabled={editando}
        />
      </label>
      <label>
        Puesto
        <input data-testid="empleado-puesto" value={datos.puesto} onChange={cambiar("puesto")} />
      </label>
      <label>
        Departamento
        <select
          data-testid="empleado-departamento"
          value={datos.departamento}
          onChange={cambiar("departamento")}
        >
          <option value="">Selecciona un departamento</option>
          {departamentos.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </label>
      <label>
        Fecha de ingreso
        <input
          type="date"
          data-testid="empleado-fecha-ingreso"
          value={datos.fecha_ingreso}
          onChange={cambiar("fecha_ingreso")}
          disabled={editando}
        />
      </label>
      <button type="submit" data-testid="empleado-guardar">
        Guardar
      </button>
      {editando && (
        <button type="button" onClick={alCancelar}>
          Cancelar
        </button>
      )}
      {exito && (
        <p className="exito" data-testid="mensaje-exito">
          {exito}
        </p>
      )}
      {error && (
        <p className="error" data-testid="mensaje-error">
          {error}
        </p>
      )}
    </form>
  );
}
