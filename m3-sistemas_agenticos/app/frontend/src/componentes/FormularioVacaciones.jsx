import { useEffect, useState } from "react";
import { obtenerSaldoVacaciones, solicitarVacaciones } from "../api.js";

// Solo muestra lo que responde la API: saldo, éxito o el detail exacto del error
export default function FormularioVacaciones({ empleado, alCerrar }) {
  const [disponibles, setDisponibles] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    // Sin anio: la API usa el año en curso
    obtenerSaldoVacaciones(empleado.id)
      .then((saldo) => setDisponibles(saldo.dias_disponibles))
      .catch((error) => setMensaje(error.message));
  }, [empleado.id]);

  const enviar = async (ev) => {
    ev.preventDefault();
    try {
      const r = await solicitarVacaciones(empleado.id, {
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
      });
      setMensaje(
        `Solicitud registrada: ${r.dias_habiles} días hábiles. Te quedan ${r.dias_restantes} días hábiles en ${r.fecha_inicio.slice(0, 4)}.`
      );
      const saldo = await obtenerSaldoVacaciones(empleado.id, r.fecha_inicio.slice(0, 4));
      setDisponibles(saldo.dias_disponibles);
    } catch (error) {
      setMensaje(error.message);
    }
  };

  return (
    <section>
      <h2>Solicitar vacaciones: {empleado.nombre}</h2>
      <p>
        Días disponibles: <span data-testid="vacaciones-disponibles">{disponibles}</span>
      </p>
      <form onSubmit={enviar}>
        <label>
          Fecha de inicio
          <input
            type="date"
            data-testid="vacaciones-fecha-inicio"
            value={fechaInicio}
            onChange={(ev) => setFechaInicio(ev.target.value)}
          />
        </label>
        <label>
          Fecha de fin
          <input
            type="date"
            data-testid="vacaciones-fecha-fin"
            value={fechaFin}
            onChange={(ev) => setFechaFin(ev.target.value)}
          />
        </label>
        <button type="submit" data-testid="vacaciones-enviar">
          Enviar
        </button>
        <button type="button" onClick={alCerrar}>
          Cerrar
        </button>
      </form>
      {mensaje && <p data-testid="vacaciones-mensaje">{mensaje}</p>}
    </section>
  );
}
