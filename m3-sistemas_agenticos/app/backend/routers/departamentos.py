from fastapi import APIRouter

from esquemas import DEPARTAMENTOS

router = APIRouter(prefix="/api/departamentos", tags=["departamentos"])


@router.get("")
def listar_departamentos() -> list[str]:
    return DEPARTAMENTOS
