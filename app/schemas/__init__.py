from app.schemas.materia import MateriaCreate, MateriaResponse, MateriaUpdate, MateriaSimpleResponse
from app.schemas.horario import HorarioCreate, HorarioResponse, HorarioUpdate
from app.schemas.evaluacion import EvaluacionCreate, EvaluacionResponse, EvaluacionUpdate, EvaluacionNotaUpdate
from app.schemas.dashboard import DashboardStats, ProximaEvaluacion

__all__ = [
    "MateriaCreate", "MateriaResponse", "MateriaUpdate", "MateriaSimpleResponse",
    "HorarioCreate", "HorarioResponse", "HorarioUpdate",
    "EvaluacionCreate", "EvaluacionResponse", "EvaluacionUpdate", "EvaluacionNotaUpdate",
    "DashboardStats", "ProximaEvaluacion"
]