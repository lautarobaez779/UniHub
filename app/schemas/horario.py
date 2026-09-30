from pydantic import BaseModel, ConfigDict
from datetime import time
from typing import Optional
from app.models.horario import DiaSemana

class HorarioBase(BaseModel):
    dia_semana: DiaSemana
    hora_inicio: time
    hora_fin: time
    aula: Optional[str] = None

class HorarioCreate(HorarioBase):
    materia_id: int

class HorarioUpdate(BaseModel):
    dia_semana: Optional[DiaSemana] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    aula: Optional[str] = None

class HorarioResponse(HorarioBase):
    id: int
    materia_id: int
    materia_nombre: Optional[str] = None
    materia_color: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)