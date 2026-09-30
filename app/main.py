from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
import app.models  # Asegura que todos los modelos ORM estén registrados en Base.metadata
from app.routers import (
    materias_router,
    horarios_router,
    evaluaciones_router,
    dashboard_router,
    views_router
)

# Asegurar directorios estáticos y de base de datos
os.makedirs("app/static/css", exist_ok=True)
os.makedirs("app/static/js", exist_ok=True)
os.makedirs("app/templates", exist_ok=True)

# Crea las tablas en SQLite automáticamente al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UniHub",
    description="Plataforma de gestión, organización y rendimiento académico universitario",
    version="1.0.0"
)

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Registrar routers de API REST
app.include_router(materias_router, prefix="/api")
app.include_router(horarios_router, prefix="/api")
app.include_router(evaluaciones_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")

# Registrar router de vistas HTML Jinja2
app.include_router(views_router)

from fastapi.responses import FileResponse

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("app/static/icons/icon-192.png")

@app.get("/apple-touch-icon.png", include_in_schema=False)
@app.get("/apple-touch-icon-precomposed.png", include_in_schema=False)
def apple_touch_icon():
    return FileResponse("app/static/icons/apple-touch-icon.png")

@app.get("/manifest.json", include_in_schema=False)
def manifest():
    return FileResponse("app/static/manifest.json", media_type="application/manifest+json")

@app.get("/sw.js", include_in_schema=False)
def service_worker():
    return FileResponse("app/static/sw.js", media_type="application/javascript")

@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app": "UniHub", "version": "1.0.0"}