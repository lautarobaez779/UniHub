from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.models.materia import EstadoMateria
from app.schemas.horario import HorarioResponse
from app.schemas.evaluacion import EvaluacionResponse

class MateriaBase(BaseModel):
    nombre: str
    codigo: Optional[str] = None
    profesor: Optional[str] = None
    anio: Optional[int] = 1
    cuatrimestre: int = 1
    estado: EstadoMateria = EstadoMateria.CURSANDO
    color_hex: Optional[str] = "#3b82f6"
    drive_url: Optional[str] = None

class MateriaCreate(MateriaBase):
    pass

class MateriaUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    profesor: Optional[str] = None
    anio: Optional[int] = None
    cuatrimestre: Optional[int] = None
    estado: Optional[EstadoMateria] = None
    color_hex: Optional[str] = None
    drive_url: Optional[str] = None

class MateriaSimpleResponse(MateriaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MateriaResponse(MateriaBase):
    id: int
    horarios: List[HorarioResponse] = []
    evaluaciones: List[EvaluacionResponse] = []
    model_config = ConfigDict(from_attributes=True)