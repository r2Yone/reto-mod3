import { useState } from "react";
import { darDeBajaEmpleado } from "../api.js";

export default function FormularioBaja({ empleado, alGuardar, alCancelar }) {
  const [fecha, setFecha] = useState("");
  const [exito, setExito] = useState("");
  const [error, setError] = useState("");

  async function confirmar(e) {
    e.preventDefault();
    setExito("");
    setError("");
    try {
      await darDeBajaEmpleado(empleado.id, fecha);
      setExito(`Empleado dado de baja: ${empleado.numero_empleado}`);
      await alGuardar();
    } catch (err) {
      setError(err.message);
    }
  }

  // noValidate: los errores los decide el backend, no el navegador
  return (
    <form onSubmit={confirmar} noValidate>
      <h2>Dar de baja a {empleado.numero_empleado}</h2>
      <label>
        Fecha de baja
        <input
          type="date"
          data-testid="empleado-fecha-baja"
          value={fecha}
          onChange={(e) => setFecha(e.target.value)}
        />
      </label>
      <button type="submit" data-testid="confirmar-baja" disabled={Boolean(exito)}>
        Confirmar baja
      </button>
      <button type="button" onClick={alCancelar}>
        Cerrar
      </button>
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
