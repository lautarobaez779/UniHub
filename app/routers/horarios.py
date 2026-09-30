from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.horario import Horario, DiaSemana
from app.models.materia import Materia
from app.schemas.horario import HorarioCreate, HorarioResponse, HorarioUpdate

router = APIRouter(prefix="/horarios", tags=["Horarios"])

def serialize_horario(h: Horario) -> HorarioResponse:
    return HorarioResponse(
        id=h.id,
        materia_id=h.materia_id,
        dia_semana=h.dia_semana,
        hora_inicio=h.hora_inicio,
        hora_fin=h.hora_fin,
        aula=h.aula,
        materia_nombre=h.materia.nombre if h.materia else "",
        materia_color=h.materia.color_hex if h.materia else "#3b82f6"
    )

@router.get("/", response_model=List[HorarioResponse])
def listar_horarios(
    materia_id: Optional[int] = None,
    dia_semana: Optional[DiaSemana] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Horario)
    if materia_id:
        query = query.filter(Horario.materia_id == materia_id)
    if dia_semana:
        query = query.filter(Horario.dia_semana == dia_semana)
    
    horarios = query.order_by(Horario.hora_inicio.asc()).all()
    return [serialize_horario(h) for h in horarios]

@router.post("/", response_model=HorarioResponse, status_code=status.HTTP_201_CREATED)
def crear_horario(horario_in: HorarioCreate, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == horario_in.materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="La materia especificada no existe")
    
    nuevo_horario = Horario(**horario_in.model_dump())
    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)
    return serialize_horario(nuevo_horario)

@router.get("/{horario_id}", response_model=HorarioResponse)
def obtener_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return serialize_horario(horario)

@router.put("/{horario_id}", response_model=HorarioResponse)
@router.patch("/{horario_id}", response_model=HorarioResponse)
def actualizar_horario(horario_id: int, horario_update: HorarioUpdate, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    update_data = horario_update.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(horario, field, val)
    
    db.commit()
    db.refresh(horario)
    return serialize_horario(horario)

@router.delete("/{horario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    db.delete(horario)
    db.commit()
    return None