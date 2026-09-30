from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.evaluacion import Evaluacion, TipoEvaluacion
from app.models.materia import Materia
from app.schemas.evaluacion import (
    EvaluacionCreate,
    EvaluacionResponse,
    EvaluacionUpdate,
    EvaluacionNotaUpdate
)

router = APIRouter(prefix="/evaluaciones", tags=["Evaluaciones"])

def serialize_evaluacion(ev: Evaluacion) -> EvaluacionResponse:
    return EvaluacionResponse(
        id=ev.id,
        materia_id=ev.materia_id,
        titulo=ev.titulo,
        tipo=ev.tipo,
        fecha=ev.fecha,
        peso_porcentaje=ev.peso_porcentaje or 0.0,
        nota=ev.nota,
        materia_nombre=ev.materia.nombre if ev.materia else "",
        materia_color=ev.materia.color_hex if ev.materia else "#3b82f6"
    )

@router.get("/", response_model=List[EvaluacionResponse])
def listar_evaluaciones(
    materia_id: Optional[int] = None,
    tipo: Optional[TipoEvaluacion] = None,
    pendientes: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Evaluacion)
    if materia_id:
        query = query.filter(Evaluacion.materia_id == materia_id)
    if tipo:
        query = query.filter(Evaluacion.tipo == tipo)
    if pendientes is True:
        query = query.filter(Evaluacion.nota.is_(None))
    elif pendientes is False:
        query = query.filter(Evaluacion.nota.isnot(None))
    
    evaluaciones = query.order_by(Evaluacion.fecha.asc()).all()
    return [serialize_evaluacion(ev) for ev in evaluaciones]

@router.post("/", response_model=EvaluacionResponse, status_code=status.HTTP_201_CREATED)
def crear_evaluacion(eval_in: EvaluacionCreate, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == eval_in.materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="La materia especificada no existe")
    
    nueva_eval = Evaluacion(**eval_in.model_dump())
    db.add(nueva_eval)
    db.commit()
    db.refresh(nueva_eval)
    return serialize_evaluacion(nueva_eval)

@router.get("/{evaluacion_id}", response_model=EvaluacionResponse)
def obtener_evaluacion(evaluacion_id: int, db: Session = Depends(get_db)):
    evaluacion = db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return serialize_evaluacion(evaluacion)

@router.put("/{evaluacion_id}", response_model=EvaluacionResponse)
@router.patch("/{evaluacion_id}", response_model=EvaluacionResponse)
def actualizar_evaluacion(evaluacion_id: int, eval_update: EvaluacionUpdate, db: Session = Depends(get_db)):
    evaluacion = db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    update_data = eval_update.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(evaluacion, field, val)
    
    db.commit()
    db.refresh(evaluacion)
    return serialize_evaluacion(evaluacion)

@router.patch("/{evaluacion_id}/nota", response_model=EvaluacionResponse)
def actualizar_nota(evaluacion_id: int, nota_in: EvaluacionNotaUpdate, db: Session = Depends(get_db)):
    evaluacion = db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    evaluacion.nota = nota_in.nota
    db.commit()
    db.refresh(evaluacion)
    return serialize_evaluacion(evaluacion)

@router.delete("/{evaluacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_evaluacion(evaluacion_id: int, db: Session = Depends(get_db)):
    evaluacion = db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    db.delete(evaluacion)
    db.commit()
    return None