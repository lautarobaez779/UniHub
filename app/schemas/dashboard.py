from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.evaluacion import EvaluacionResponse
from app.schemas.horario import HorarioResponse

class ProximaEvaluacion(BaseModel):
    id: int
    titulo: str
    tipo: str
    fecha: datetime
    dias_restantes: int
    urgencia: str  # 'URGENTE', 'PROXIMO', 'NORMAL'
    materia_id: int
    materia_nombre: str
    materia_color: str
    peso_porcentaje: Optional[float] = None

class DashboardStats(BaseModel):
    total_materias: int
    materias_cursando: int
    materias_regulares: int
    materias_aprobadas: int
    materias_pendientes: int
    promedio_general: float
    promedio_ponderado: float
    total_evaluaciones: int
    evaluaciones_rendidas: int
    evaluaciones_aprobadas: int
    evaluaciones_pendientes: int
    tasa_aprobacion: float
    proximos_examenes: List[ProximaEvaluacion] = []
    clases_hoy: List[HorarioResponse] = []
