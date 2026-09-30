from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.materia import Materia, EstadoMateria
from app.schemas.materia import MateriaCreate, MateriaResponse, MateriaUpdate

router = APIRouter(prefix="/materias", tags=["Materias"])

@router.get("/", response_model=List[MateriaResponse])
def listar_materias(
    estado: Optional[EstadoMateria] = None,
    anio: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Materia)
    if estado:
        query = query.filter(Materia.estado == estado)
    if anio:
        query = query.filter(Materia.anio == anio)
    return query.order_by(Materia.id.desc()).all()

@router.post("/", response_model=MateriaResponse, status_code=status.HTTP_201_CREATED)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    nueva_materia = Materia(**materia.model_dump())
    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)
    return nueva_materia

@router.get("/{materia_id}", response_model=MateriaResponse)
def obtener_materia(materia_id: int, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia

@router.put("/{materia_id}", response_model=MateriaResponse)
@router.patch("/{materia_id}", response_model=MateriaResponse)
def actualizar_materia(materia_id: int, materia_update: MateriaUpdate, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    
    update_data = materia_update.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(materia, field, val)
    
    db.commit()
    db.refresh(materia)
    return materia

@router.delete("/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_materia(materia_id: int, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    db.delete(materia)
    db.commit()
    return None