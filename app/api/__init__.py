"""
API module initialization.
"""

from app.api.routes import router as calculators_router
from app.api.history_routes import router as history_router

__all__ = ["calculators_router", "history_router"]
