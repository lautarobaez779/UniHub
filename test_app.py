import anyio
import httpx
from app.main import app

async def run_tests():
    print("Iniciando pruebas de integración de UniHub con AsyncClient...")
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 1. Health check
        res = await client.get("/api/health")
        assert res.status_code == 200, f"Error en /api/health: {res.status_code}"
        print("✔ /api/health OK")

        # 2. Vistas HTML principales
        vistas = ["/", "/materias", "/horarios", "/evaluaciones", "/calculadora"]
        for v in vistas:
            res = await client.get(v)
            assert res.status_code == 200, f"Error en vista {v}: {res.status_code}"
            assert "UniHub" in res.text, f"No se encontró 'UniHub' en vista {v}"
            print(f"✔ Vista {v} OK (HTML 200)")

        # 3. API Materias
        res = await client.get("/api/materias/")
        assert res.status_code == 200, f"Error en GET /api/materias/: {res.status_code}"
        materias = res.json()
        assert len(materias) > 0, "No se encontraron materias"
        print(f"✔ GET /api/materias/ OK ({len(materias)} materias cargadas)")

        # Crear Materia de prueba
        test_materia_payload = {
            "nombre": "Materia de Prueba Temporal",
            "codigo": "TEST-999",
            "profesor": "Prof. Test",
            "anio": 4,
            "cuatrimestre": 2,
            "estado": "CURSANDO",
            "color_hex": "#10b981",
            "drive_url": "https://test.com"
        }
        res = await client.post("/api/materias/", json=test_materia_payload)
        assert res.status_code == 201, f"Error en POST /api/materias/: {res.status_code} {res.text}"
        materia_creada = res.json()
        mat_id = materia_creada["id"]
        print(f"✔ POST /api/materias/ OK (ID creado: {mat_id})")

        # Actualizar Materia
        res = await client.put(f"/api/materias/{mat_id}", json={"nombre": "Materia de Prueba Actualizada"})
        assert res.status_code == 200
        assert res.json()["nombre"] == "Materia de Prueba Actualizada"
        print(f"✔ PUT /api/materias/{mat_id} OK")

        # 4. API Horarios
        horario_payload = {
            "materia_id": mat_id,
            "dia_semana": "LUNES",
            "hora_inicio": "10:00:00",
            "hora_fin": "12:00:00",
            "aula": "Aula Test 101"
        }
        res = await client.post("/api/horarios/", json=horario_payload)
        assert res.status_code == 201, f"Error en POST /api/horarios/: {res.status_code} {res.text}"
        horario_id = res.json()["id"]
        print(f"✔ POST /api/horarios/ OK (ID: {horario_id})")

        res = await client.get(f"/api/horarios/?materia_id={mat_id}")
        assert res.status_code == 200
        assert len(res.json()) >= 1
        print("✔ GET /api/horarios/ OK")

        # 5. API Evaluaciones
        eval_payload = {
            "materia_id": mat_id,
            "titulo": "Parcial de Prueba",
            "tipo": "PARCIAL",
            "fecha": "2026-11-15T09:00:00",
            "peso_porcentaje": 30.0,
            "nota": None
        }
        res = await client.post("/api/evaluaciones/", json=eval_payload)
        assert res.status_code == 201, f"Error en POST /api/evaluaciones/: {res.status_code} {res.text}"
        eval_id = res.json()["id"]
        print(f"✔ POST /api/evaluaciones/ OK (ID: {eval_id})")

        # Cargar nota
        res = await client.patch(f"/api/evaluaciones/{eval_id}/nota", json={"nota": 9.5})
        assert res.status_code == 200
        assert res.json()["nota"] == 9.5
        print(f"✔ PATCH /api/evaluaciones/{eval_id}/nota OK (Nota: 9.5)")

        # 6. Dashboard Stats
        res = await client.get("/api/dashboard/stats")
        assert res.status_code == 200
        stats = res.json()
        assert "promedio_ponderado" in stats
        assert "total_materias" in stats
        assert stats["promedio_ponderado"] > 0
        print(f"✔ GET /api/dashboard/stats OK (Promedio ponderado: {stats['promedio_ponderado']}, Total materias: {stats['total_materias']})")

        # 7. Limpieza del registro de prueba
        res = await client.delete(f"/api/evaluaciones/{eval_id}")
        assert res.status_code == 204
        res = await client.delete(f"/api/horarios/{horario_id}")
        assert res.status_code == 204
        res = await client.delete(f"/api/materias/{mat_id}")
        assert res.status_code == 204
        print("✔ DELETE cascada y limpieza OK")

        print("\n🎉 ¡TODAS LAS PRUEBAS DE UNIHUB PASARON EXITOSAMENTE!")

if __name__ == "__main__":
    anyio.run(run_tests)
