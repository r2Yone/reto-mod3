"""Festivos oficiales (Ley Federal del Trabajo, art. 74). Un festivo en fin de semana no se recorre."""
from datetime import date

FESTIVOS: dict[int, set[date]] = {
    2026: {
        date(2026, 1, 1),
        date(2026, 2, 2),
        date(2026, 3, 16),
        date(2026, 5, 1),
        date(2026, 9, 16),
        date(2026, 11, 16),
        date(2026, 12, 25),
    },
    2027: {
        date(2027, 1, 1),
        date(2027, 2, 1),
        date(2027, 3, 15),
        date(2027, 5, 1),
        date(2027, 9, 16),
        date(2027, 11, 15),
        date(2027, 12, 25),
    },
}

ANIOS_PERMITIDOS = sorted(FESTIVOS)
