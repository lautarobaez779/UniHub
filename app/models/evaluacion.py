import enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.database import Base

class TipoEvaluacion(str, enum.Enum):
    PARCIAL = "PARCIAL"
    TP = "TP"
    FINAL = "FINAL"
    RECUPERATORIO = "RECUPERATORIO"

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    titulo = Column(String(100), nullable=False)
    tipo = Column(SQLEnum(TipoEvaluacion), nullable=False)
    fecha = Column(DateTime, nullable=False)
    peso_porcentaje = Column(Float, nullable=True)
    nota = Column(Float, nullable=True)

    materia = relationship("Materia", back_populates="evaluaciones")