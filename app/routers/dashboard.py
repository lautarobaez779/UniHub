from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List

from app.database import get_db
from app.models.materia import Materia, EstadoMateria
from app.models.horario import Horario, DiaSemana
from app.models.evaluacion import Evaluacion
from app.schemas.dashboard import DashboardStats, ProximaEvaluacion
from app.schemas.horario import HorarioResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

DIAS_MAP = {
    0: DiaSemana.LUNES,
    1: DiaSemana.MARTES,
    2: DiaSemana.MIERCOLES,
    3: DiaSemana.JUEVES,
    4: DiaSemana.VIERNES,
    5: DiaSemana.SABADO,
    6: None # Domingo no suele haber clases universitarias regulares
}

@router.get("/stats", response_model=DashboardStats)
def obtener_estadisticas_dashboard(db: Session = Depends(get_db)):
    # 1. Materias y Estados
    materias = db.query(Materia).all()
    total_materias = len(materias)
    materias_cursando = sum(1 for m in materias if m.estado == EstadoMateria.CURSANDO)
    materias_regulares = sum(1 for m in materias if m.estado == EstadoMateria.REGULAR)
    materias_aprobadas = sum(1 for m in materias if m.estado == EstadoMateria.APROBADA)
    materias_pendientes = sum(1 for m in materias if m.estado == EstadoMateria.PENDIENTE)

    # 2. Evaluaciones y Notas
    evaluaciones = db.query(Evaluacion).all()
    total_evaluaciones = len(evaluaciones)
    evals_con_nota = [e for e in evaluaciones if e.nota is not None]
    evaluaciones_rendidas = len(evals_con_nota)
    evaluaciones_aprobadas = sum(1 for e in evals_con_nota if e.nota >= 4.0)
    evaluaciones_pendientes = total_evaluaciones - evaluaciones_rendidas

    # Promedio simple
    if evals_con_nota:
        promedio_general = round(sum(e.nota for e in evals_con_nota) / len(evals_con_nota), 2)
    else:
        promedio_general = 0.0

    # Promedio ponderado
    # Considera notas con peso_porcentaje > 0. Si no hay pesos definidos, usa promedio simple.
    evals_ponderadas = [e for e in evals_con_nota if e.peso_porcentaje and e.peso_porcentaje > 0]
    if evals_ponderadas:
        suma_productos = sum(e.nota * e.peso_porcentaje for e in evals_ponderadas)
        suma_pesos = sum(e.peso_porcentaje for e in evals_ponderadas)
        promedio_ponderado = round(suma_productos / suma_pesos, 2) if suma_pesos > 0 else promedio_general
    else:
        promedio_ponderado = promedio_general

    # Tasa de aprobación
    tasa_aprobacion = round((evaluaciones_aprobadas / evaluaciones_rendidas * 100), 1) if evaluaciones_rendidas > 0 else 0.0

    # 3. Próximos exámenes y fechas límite
    ahora = datetime.now()
    evaluaciones_futuras = [
        e for e in evaluaciones 
        if e.fecha >= ahora.replace(hour=0, minute=0, second=0) and e.nota is None
    ]
    evaluaciones_futuras.sort(key=lambda x: x.fecha)

    proximos_examenes: List[ProximaEvaluacion] = []
    for ev in evaluaciones_futuras[:6]:  # Las 6 más próximas
        dias_restantes = (ev.fecha.date() - ahora.date()).days
        if dias_restantes <= 3:
            urgencia = "URGENTE"
        elif dias_restantes <= 7:
            urgencia = "PROXIMO"
        else:
            urgencia = "NORMAL"

        proximos_examenes.append(
            ProximaEvaluacion(
                id=ev.id,
                titulo=ev.titulo,
                tipo=ev.tipo.value,
                fecha=ev.fecha,
                dias_restantes=dias_restantes,
                urgencia=urgencia,
                materia_id=ev.materia_id,
                materia_nombre=ev.materia.nombre if ev.materia else "Materia",
                materia_color=ev.materia.color_hex if ev.materia else "#3b82f6",
                peso_porcentaje=ev.peso_porcentaje
            )
        )

    # 4. Clases del día de hoy
    dia_semana_actual = DIAS_MAP.get(ahora.weekday())
    clases_hoy: List[HorarioResponse] = []
    if dia_semana_actual:
        horarios_hoy = db.query(Horario).filter(Horario.dia_semana == dia_semana_actual).order_by(Horario.hora_inicio.asc()).all()
        for h in horarios_hoy:
            clases_hoy.append(
                HorarioResponse(
                    id=h.id,
                    materia_id=h.materia_id,
                    dia_semana=h.dia_semana,
                    hora_inicio=h.hora_inicio,
                    hora_fin=h.hora_fin,
                    aula=h.aula,
                    materia_nombre=h.materia.nombre if h.materia else "",
                    materia_color=h.materia.color_hex if h.materia else "#3b82f6"
                )
            )

    return DashboardStats(
        total_materias=total_materias,
        materias_cursando=materias_cursando,
        materias_regulares=materias_regulares,
        materias_aprobadas=materias_aprobadas,
        materias_pendientes=materias_pendientes,
        promedio_general=promedio_general,
        promedio_ponderado=promedio_ponderado,
        total_evaluaciones=total_evaluaciones,
        evaluaciones_rendidas=evaluaciones_rendidas,
        evaluaciones_aprobadas=evaluaciones_aprobadas,
        evaluaciones_pendientes=evaluaciones_pendientes,
        tasa_aprobacion=tasa_aprobacion,
        proximos_examenes=proximos_examenes,
        clases_hoy=clases_hoy
    )
