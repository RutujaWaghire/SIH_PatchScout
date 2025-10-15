"""
PatchScout Backend - Main FastAPI Application
Centralized Vulnerability Detection System
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging

from app.config import settings
from app.database import engine, Base, get_db
from app.api import scans, vulnerabilities, chat, attack_paths, reports
from app.models import Scan, Vulnerability, ScanResult, CVEData  # Import models
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Starting PatchScout Backend...")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
    
    # Initialize ChromaDB (optional)
    # try:
    #     from app.services.rag_chatbot.embeddings import initialize_chroma
    #     initialize_chroma()
    #     logger.info("✅ ChromaDB initialized successfully")
    # except Exception as e:
    #     logger.warning(f"⚠️ ChromaDB initialization skipped: {e}")
    
    # Initialize Neo4j (optional)
    # try:
    #     from app.services.attack_path.graph_generator import test_neo4j_connection
    #     if test_neo4j_connection():
    #         logger.info("✅ Neo4j connection established")
    # except Exception as e:
    #     logger.warning(f"⚠️ Neo4j connection skipped: {e}")
    
    logger.info(f"✅ PatchScout Backend started on {settings.HOST}:{settings.PORT}")
    logger.info(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down PatchScout Backend...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Centralized Vulnerability Detection System with AI-Powered Analysis",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log request
    logger.info(
        f"{request.method} {request.url.path} "
        f"- Status: {response.status_code} - Duration: {duration:.3f}s"
    )
    
    # Add custom headers
    response.headers["X-Process-Time"] = str(duration)
    response.headers["X-PatchScout-Version"] = settings.APP_VERSION
    
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Validation error in request data"
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred processing your request"
        },
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": time.time()
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Centralized Vulnerability Detection System",
        "docs": f"{settings.API_V1_STR}/docs",
        "health": "/health",
        "features": {
            "scanning_tools": ["Nmap", "OpenVAS", "Nessus", "Nikto", "Nuclei"],
            "ai_assistant": "RAG-powered chatbot",
            "attack_paths": "Neo4j graph analysis",
            "threat_intel": "NVD, ExploitDB integration"
        }
    }


# Include API routers
app.include_router(scans.router, prefix="/api")
app.include_router(vulnerabilities.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(attack_paths.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS if not settings.RELOAD else 1,
        log_level=settings.LOG_LEVEL.lower()
    )
