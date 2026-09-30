from app.routers.materias import router as materias_router
from app.routers.horarios import router as horarios_router
from app.routers.evaluaciones import router as evaluaciones_router
from app.routers.dashboard import router as dashboard_router
from app.routers.views import views_router

__all__ = [
    "materias_router",
    "horarios_router",
    "evaluaciones_router",
    "dashboard_router",
    "views_router"
]