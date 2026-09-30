from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.evaluacion import TipoEvaluacion

class EvaluacionBase(BaseModel):
    titulo: str
    tipo: TipoEvaluacion
    fecha: datetime
    peso_porcentaje: Optional[float] = 0.0
    nota: Optional[float] = None

class EvaluacionCreate(EvaluacionBase):
    materia_id: int

class EvaluacionUpdate(BaseModel):
    titulo: Optional[str] = None
    tipo: Optional[TipoEvaluacion] = None
    fecha: Optional[datetime] = None
    peso_porcentaje: Optional[float] = None
    nota: Optional[float] = None

class EvaluacionNotaUpdate(BaseModel):
    nota: Optional[float] = None

class EvaluacionResponse(EvaluacionBase):
    id: int
    materia_id: int
    materia_nombre: Optional[str] = None
    materia_color: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)