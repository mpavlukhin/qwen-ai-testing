"""
Calculator Hub - Main Application Entry Point
FastAPI application with separated frontend and backend.
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.api.routes import router as calculators_router
from app.api.history_routes import router as history_router
from app.api.database import init_db


# Initialize FastAPI app
app = FastAPI(
    title="Calculator Hub",
    description="A comprehensive web-based calculator application with multiple calculation tools",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Get the directory where this file is located
BASE_DIR = Path(__file__).parent

# Mount static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Setup templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Include API routers
app.include_router(calculators_router)
app.include_router(history_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Calculator Hub is running"}


def main():
    """Run the application with default settings."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    Calculator Hub                         ║
    ║                                                           ║
    ║  Starting server...                                       ║
    ║  Open http://127.0.0.1:8000 in your browser               ║
    ║                                                           ║
    ║  API Documentation: http://127.0.0.1:8000/docs            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
