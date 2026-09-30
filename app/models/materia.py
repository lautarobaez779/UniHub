import enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from app.database import Base

class EstadoMateria(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    CURSANDO = "CURSANDO"
    REGULAR = "REGULAR"
    APROBADA = "APROBADA"

class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), nullable=True)
    profesor = Column(String(100), nullable=True)
    anio = Column(Integer, nullable=True, default=1)
    cuatrimestre = Column(Integer, nullable=False, default=1)
    estado = Column(SQLEnum(EstadoMateria), default=EstadoMateria.CURSANDO)
    color_hex = Column(String(7), default="#3b82f6")
    drive_url = Column(Text, nullable=True)

    horarios = relationship("Horario", back_populates="materia", cascade="all, delete-orphan")
    evaluaciones = relationship("Evaluacion", back_populates="materia", cascade="all, delete-orphan")