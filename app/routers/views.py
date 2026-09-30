from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.materia import Materia
from app.models.horario import Horario
from app.models.evaluacion import Evaluacion
from app.routers.dashboard import obtener_estadisticas_dashboard

views_router = APIRouter(tags=["Vistas Web"])
templates = Jinja2Templates(directory="app/templates")

@views_router.get("/", response_class=HTMLResponse)
@views_router.get("/dashboard", response_class=HTMLResponse)
def vista_dashboard(request: Request, db: Session = Depends(get_db)):
    stats = obtener_estadisticas_dashboard(db)
    materias = db.query(Materia).order_by(Materia.nombre.asc()).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "active_tab": "dashboard",
            "stats": stats,
            "materias": materias,
            "ahora": datetime.now()
        }
    )

@views_router.get("/materias", response_class=HTMLResponse)
def vista_materias(request: Request, db: Session = Depends(get_db)):
    materias = db.query(Materia).order_by(Materia.id.desc()).all()
    return templates.TemplateResponse(
        "materias.html",
        {
            "request": request,
            "active_tab": "materias",
            "materias": materias
        }
    )

@views_router.get("/horarios", response_class=HTMLResponse)
def vista_horarios(request: Request, db: Session = Depends(get_db)):
    materias = db.query(Materia).order_by(Materia.nombre.asc()).all()
    horarios = db.query(Horario).order_by(Horario.hora_inicio.asc()).all()
    dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO"]
    return templates.TemplateResponse(
        "horarios.html",
        {
            "request": request,
            "active_tab": "horarios",
            "materias": materias,
            "horarios": horarios,
            "dias": dias
        }
    )

@views_router.get("/evaluaciones", response_class=HTMLResponse)
def vista_evaluaciones(request: Request, db: Session = Depends(get_db)):
    materias = db.query(Materia).order_by(Materia.nombre.asc()).all()
    evaluaciones = db.query(Evaluacion).order_by(Evaluacion.fecha.asc()).all()
    return templates.TemplateResponse(
        "evaluaciones.html",
        {
            "request": request,
            "active_tab": "evaluaciones",
            "materias": materias,
            "evaluaciones": evaluaciones
        }
    )

@views_router.get("/calculadora", response_class=HTMLResponse)
def vista_calculadora(request: Request, db: Session = Depends(get_db)):
    stats = obtener_estadisticas_dashboard(db)
    materias = db.query(Materia).order_by(Materia.nombre.asc()).all()
    evaluaciones = db.query(Evaluacion).order_by(Evaluacion.fecha.asc()).all()
    return templates.TemplateResponse(
        "calculadora.html",
        {
            "request": request,
            "active_tab": "calculadora",
            "stats": stats,
            "materias": materias,
            "evaluaciones": evaluaciones
        }
    )
