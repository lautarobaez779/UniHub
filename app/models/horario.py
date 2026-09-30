import enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.database import Base

class DiaSemana(str, enum.Enum):
    LUNES = "LUNES"
    MARTES = "MARTES"
    MIERCOLES = "MIÉRCOLES"
    JUEVES = "JUEVES"
    VIERNES = "VIERNES"
    SABADO = "SÁBADO"

class Horario(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    dia_semana = Column(SQLEnum(DiaSemana), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    aula = Column(String(200), nullable=True)

    materia = relationship("Materia", back_populates="horarios")