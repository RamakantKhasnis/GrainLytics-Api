from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import dashboard, sensors, geo, chat

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grainlytics API", description="API for Grain Storage Condition Monitor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
app.include_router(sensors.router, prefix="/api", tags=["sensors"])
app.include_router(geo.router, prefix="/api", tags=["geo"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
