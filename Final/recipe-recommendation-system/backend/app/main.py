from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .auth import routes as auth_routes
from .recipes import routes as recipe_routes
from .reviews import routes as review_routes
from .recommendations import routes as recommendation_routes
from .recommendations import enhanced_routes
from .meal_planner import routes as meal_planner_routes
from .grocery import routes as grocery_routes
from .ai_generator import routes as ai_generator_routes
from app import models


# -------------------------------------------------------------------
# Database initialization
# -------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------
# FastAPI App
# -------------------------------------------------------------------
app = FastAPI(
    title="AI Recipe Recommendation System",
    description="Complete ML-powered recipe recommendation system with SBERT + FAISS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# -------------------------------------------------------------------
# CORS Configuration (Frontend Safe)
# -------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins (safe for dev)
    allow_credentials=True,
    allow_methods=["*"],           # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],           # Authorization, Content-Type, etc.
    expose_headers=["*"]
)

# -------------------------------------------------------------------
# API Routers (DO NOT ADD TAGS HERE)
# Tags must be inside each router file
# -------------------------------------------------------------------
app.include_router(auth_routes.router, prefix="/api")
app.include_router(recipe_routes.router, prefix="/api")
app.include_router(review_routes.router, prefix="/api")
app.include_router(recommendation_routes.router, prefix="/api")
app.include_router(enhanced_routes.router, prefix="/api")
app.include_router(meal_planner_routes.router, prefix="/api")
app.include_router(grocery_routes.router, prefix="/api")
app.include_router(ai_generator_routes.router, prefix="/api")


# -------------------------------------------------------------------
# Health & Root Endpoints
# -------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "AI Recipe Recommendation System API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ml_models": "loaded"
    }

# -------------------------------------------------------------------
# Local development entry point
# -------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
