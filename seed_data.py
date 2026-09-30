"""
Script para inicializar datos de prueba realistas en UniHub.
"""
from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models.materia import Materia, EstadoMateria
from app.models.horario import Horario, DiaSemana
from app.models.evaluacion import Evaluacion, TipoEvaluacion

def seed():
    db = SessionLocal()
    try:
        # Limpiar datos previos si existen
        db.query(Evaluacion).delete()
        db.query(Horario).delete()
        db.query(Materia).delete()
        db.commit()

        print("Insertando materias de ejemplo...")
        # 1. Materias
        m1 = Materia(
            nombre="Algoritmos y Estructuras de Datos",
            codigo="CS-201",
            profesor="Dr. Martín Gómez",
            anio=2,
            cuatrimestre=1,
            estado=EstadoMateria.CURSANDO,
            color_hex="#3b82f6", # Azul
            drive_url="https://drive.google.com"
        )
        m2 = Materia(
            nombre="Bases de Datos Relacionales",
            codigo="BD-102",
            profesor="Ing. Valeria Rossi",
            anio=2,
            cuatrimestre=1,
            estado=EstadoMateria.CURSANDO,
            color_hex="#10b981", # Verde esmeralda
            drive_url="https://drive.google.com"
        )
        m3 = Materia(
            nombre="Sistemas Operativos y Redes",
            codigo="SO-301",
            profesor="Lic. Carlos Morales",
            anio=3,
            cuatrimestre=1,
            estado=EstadoMateria.CURSANDO,
            color_hex="#f59e0b", # Ámbar
            drive_url=None
        )
        m4 = Materia(
            nombre="Probabilidad y Estadística",
            codigo="MAT-105",
            profesor="Dra. Elena Bianchi",
            anio=2,
            cuatrimestre=1,
            estado=EstadoMateria.REGULAR,
            color_hex="#8b5cf6", # Violeta
            drive_url=None
        )
        m5 = Materia(
            nombre="Álgebra y Geometría Analítica",
            codigo="MAT-101",
            profesor="Prof. Roberto Fernández",
            anio=1,
            cuatrimestre=1,
            estado=EstadoMateria.APROBADA,
            color_hex="#ec4899", # Rosa
            drive_url=None
        )

        db.add_all([m1, m2, m3, m4, m5])
        db.commit()

        for m in [m1, m2, m3, m4, m5]:
            db.refresh(m)

        print("Insertando bloques horarios...")
        # 2. Horarios
        h1 = Horario(
            materia_id=m1.id,
            dia_semana=DiaSemana.LUNES,
            hora_inicio=datetime.strptime("08:00", "%H:%M").time(),
            hora_fin=datetime.strptime("10:30", "%H:%M").time(),
            aula="Laboratorio de Cómputo 3"
        )
        h2 = Horario(
            materia_id=m1.id,
            dia_semana=DiaSemana.MIERCOLES,
            hora_inicio=datetime.strptime("08:00", "%H:%M").time(),
            hora_fin=datetime.strptime("10:30", "%H:%M").time(),
            aula="Aula 104 - Pabellón A"
        )
        h3 = Horario(
            materia_id=m2.id,
            dia_semana=DiaSemana.MARTES,
            hora_inicio=datetime.strptime("14:00", "%H:%M").time(),
            hora_fin=datetime.strptime("17:00", "%H:%M").time(),
            aula="Sala Multimedia 2"
        )
        h4 = Horario(
            materia_id=m3.id,
            dia_semana=DiaSemana.JUEVES,
            hora_inicio=datetime.strptime("18:00", "%H:%M").time(),
            hora_fin=datetime.strptime("21:00", "%H:%M").time(),
            aula="Aula Magna / Meet virtual"
        )
        h5 = Horario(
            materia_id=m3.id,
            dia_semana=DiaSemana.VIERNES,
            hora_inicio=datetime.strptime("16:00", "%H:%M").time(),
            hora_fin=datetime.strptime("18:30", "%H:%M").time(),
            aula="Lab Sistemas 1"
        )
        h6 = Horario(
            materia_id=m4.id,
            dia_semana=DiaSemana.SABADO,
            hora_inicio=datetime.strptime("09:00", "%H:%M").time(),
            hora_fin=datetime.strptime("12:00", "%H:%M").time(),
            aula="Campus Virtual Zoom"
        )

        db.add_all([h1, h2, h3, h4, h5, h6])
        db.commit()

        print("Insertando evaluaciones y exámenes...")
        # 3. Evaluaciones (algunas rendidas con nota, algunas próximas en 2, 6 y 15 días)
        ahora = datetime.now()

        # Ya rendidas
        ev1 = Evaluacion(
            materia_id=m1.id,
            titulo="Primer Parcial Práctico: Árboles y Grafos",
            tipo=TipoEvaluacion.PARCIAL,
            fecha=ahora - timedelta(days=20),
            peso_porcentaje=30.0,
            nota=8.5
        )
        ev2 = Evaluacion(
            materia_id=m2.id,
            titulo="TP 1: Modelado Entidad-Relación y Normalización",
            tipo=TipoEvaluacion.TP,
            fecha=ahora - timedelta(days=12),
            peso_porcentaje=20.0,
            nota=9.0
        )
        ev3 = Evaluacion(
            materia_id=m5.id,
            titulo="Examen Final Regular",
            tipo=TipoEvaluacion.FINAL,
            fecha=ahora - timedelta(days=60),
            peso_porcentaje=100.0,
            nota=8.0
        )

        # Futuras / Próximas (una urgente en 2 días, otra en 6 días, otra en 18 días)
        ev4 = Evaluacion(
            materia_id=m1.id,
            titulo="Segundo Parcial: Complejidad y Algoritmos Voraces",
            tipo=TipoEvaluacion.PARCIAL,
            fecha=ahora + timedelta(days=2, hours=4),
            peso_porcentaje=40.0,
            nota=None
        )
        ev5 = Evaluacion(
            materia_id=m3.id,
            titulo="Entrega TP Integrador: Administrador de Procesos",
            tipo=TipoEvaluacion.TP,
            fecha=ahora + timedelta(days=6, hours=2),
            peso_porcentaje=25.0,
            nota=None
        )
        ev6 = Evaluacion(
            materia_id=m2.id,
            titulo="Parcial SQL Avanzado y Stored Procedures",
            tipo=TipoEvaluacion.PARCIAL,
            fecha=ahora + timedelta(days=18),
            peso_porcentaje=35.0,
            nota=None
        )

        db.add_all([ev1, ev2, ev3, ev4, ev5, ev6])
        db.commit()

        print("¡Datos de prueba insertados con éxito en unihub.db!")
    except Exception as e:
        db.rollback()
        print(f"Error al sembrar datos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
