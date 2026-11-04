"""Sesión 1 · Agente 1, analista: historia de usuario -> criterios de aceptación en Gherkin.

Uso:  python -m agentes.analista historias/HU-01-registrar-empleado.md
"""
import re
import sys
from pathlib import Path

from agentes.base import RAIZ, SALIDA, ejecutar_agente, herramientas_archivos, hu_de, rel

SISTEMA = """Eres analista de producto en un equipo de software. Conviertes historias de usuario
en criterios de aceptación escritos en Gherkin, en español.

Cómo trabajas:
1. Lee la historia, contexto/reglas_negocio.md y contexto/convenciones_app.md, y además cada
   archivo de contexto/ que la historia mencione.
2. Escribe {destino}. La primera línea es `# language: es` y usas las palabras clave
   Característica, Escenario, Dado, Cuando, Entonces, Y.
3. Incluye el camino feliz y un escenario de error por cada regla de negocio que aplique a ESTA historia.
4. Cada escenario se puede verificar desde la pantalla o la API: datos concretos, nada de «funciona bien».
5. Si el contexto define códigos y mensajes de error exactos, cada uno tiene su escenario, con el código
   HTTP y el mensaje copiado carácter por carácter entre comillas (acentos y puntuación incluidos).
   Donde el mensaje tiene un valor variable (por ejemplo N), escribe el número concreto que espera el escenario.
6. Cubre los límites de cada regla con datos concretos: el valor justo que se acepta y el primero que se
   rechaza (por ejemplo, el día exacto en que se cumple un plazo y el día anterior; usar exactamente lo que
   queda y pasarse por uno), y los ejemplos que trae el contexto.
7. No inventes reglas ni preguntes lo que el contexto ya responde. Si de verdad falta información,
   agrégala al final como comentarios bajo `# Preguntas abiertas`.
8. Responde al final con una sola línea: cuántos escenarios escribiste."""

# Mensajes con valores variables: N, M (números) y AAAA (año) se aceptan como cualquier número
_COMODINES = {"N": r"\d+", "M": r"\d+", "AAAA": r"\d{4}"}


def mensajes_exactos(historia: Path) -> list[tuple[str, str]]:
    """(código, mensaje) de las tablas de errores de los archivos de contexto/ que la historia menciona.

    Una fila de tabla cuenta si tiene un código HTTP y un mensaje entre comillas invertidas:
    `| caso | 400 | `mensaje` |`. También cuenta una línea «... exacto ...: `mensaje`» (código vacío).
    """
    texto = historia.read_text(encoding="utf-8")
    citados = sorted(set(re.findall(r"contexto/[\w\-]+\.md", texto)))
    mensajes = []
    for archivo in citados:
        ruta = RAIZ / archivo
        if not ruta.exists():
            continue
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            fila = re.match(r"^\|.*\|\s*(\d{3})\s*\|\s*`([^`]+)`\s*\|\s*$", linea)
            if fila:
                mensajes.append((fila.group(1), fila.group(2)))
            elif "exacto" in linea.lower() and (m := re.search(r":\s*`([^`]+)`\s*$", linea)):
                mensajes.append(("", m.group(1)))
    return mensajes


def patron_mensaje(mensaje: str) -> re.Pattern:
    """Convierte un mensaje con comodines (N, M, AAAA) en una expresión regular exacta."""
    partes = re.split(r"\b(N|M|AAAA)\b", mensaje)
    return re.compile("".join(_COMODINES[p] if p in _COMODINES else re.escape(p) for p in partes))


def validar_mensajes(texto: str, mensajes: list[tuple[str, str]]) -> list[str]:
    """Cada mensaje exacto aparece en algún escenario, y en ese escenario aparece también su código."""
    bloques = re.split(r"^\s*Escenario:", texto, flags=re.MULTILINE)[1:]
    problemas = []
    for codigo, mensaje in mensajes:
        patron = patron_mensaje(mensaje)
        con_mensaje = [b for b in bloques if patron.search(b)]
        if not con_mensaje:
            problemas.append(f"Ningún escenario contiene el mensaje exacto «{mensaje}» (cópialo letra por letra).")
        elif codigo and not any(re.search(rf"\b{codigo}\b", b) for b in con_mensaje):
            problemas.append(f"El escenario del mensaje «{mensaje}» no indica el código {codigo}.")
    return problemas


def escenarios(gherkin: str) -> list[str]:
    return re.findall(r"^\s*Escenario:\s*(.+?)\s*$", gherkin, flags=re.MULTILINE)


def preguntas_abiertas(gherkin: str) -> list[str]:
    if "# Preguntas abiertas" not in gherkin:
        return []
    bloque = gherkin.split("# Preguntas abiertas", 1)[1]
    return [l.lstrip("# -").strip() for l in bloque.splitlines() if l.strip().lstrip("#").strip()]


def validar_gherkin(texto: str) -> list[str]:
    """Evaluador determinista: devuelve los problemas encontrados; vacío = válido."""
    problemas = []
    if not texto.lstrip().startswith("# language: es"):
        problemas.append("La primera línea debe ser '# language: es'.")
    if "Característica:" not in texto:
        problemas.append("Falta 'Característica:'.")
    bloques = re.split(r"^\s*Escenario:", texto, flags=re.MULTILINE)[1:]
    if len(bloques) < 2:
        problemas.append("Se esperan al menos 2 escenarios (camino feliz y un error).")
    for i, bloque in enumerate(bloques, 1):
        for clave in ("Dado", "Cuando", "Entonces"):
            if not re.search(rf"^\s*{clave}\b", bloque, flags=re.MULTILINE):
                problemas.append(f"El escenario {i} no tiene '{clave}'.")
    return problemas


def generar_criterios(historia: Path, max_intentos: int = 2) -> Path:
    carpeta = SALIDA / hu_de(historia)
    destino = carpeta / "criterios.feature"
    herramientas = herramientas_archivos(lectura=[RAIZ / "historias", RAIZ / "contexto"], escritura=carpeta)
    tarea = f"Historia de usuario: {rel(historia)}"
    mensajes = mensajes_exactos(historia)
    for intento in range(1, max_intentos + 1):
        print(f"Analista · intento {intento}")
        ejecutar_agente(SISTEMA.format(destino=rel(destino)), herramientas, tarea, max_pasos=15, nombre="analista")
        if destino.exists():
            texto = destino.read_text(encoding="utf-8")
            problemas = validar_gherkin(texto) + validar_mensajes(texto, mensajes)
        else:
            problemas = [f"No se escribió {rel(destino)}."]
        if not problemas:
            return destino
        # Reflexión guiada por un evaluador determinista: el agente recibe los problemas y corrige
        tarea += "\n\nTu versión anterior tiene estos problemas; corrígelos:\n- " + "\n- ".join(problemas)
    raise ValueError("Criterios inválidos tras varios intentos:\n- " + "\n- ".join(problemas))


if __name__ == "__main__":
    ruta = generar_criterios(Path(sys.argv[1]).resolve())
    texto = ruta.read_text(encoding="utf-8")
    print(f"\nListo: {rel(ruta)} · {len(escenarios(texto))} escenarios")
    for p in preguntas_abiertas(texto):
        print("  Pregunta abierta:", p)
