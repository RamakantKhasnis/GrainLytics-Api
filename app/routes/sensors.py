from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Device

router = APIRouter()

@router.get("/devices")
def get_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    results = []
    for d in devices:
        results.append({
            "id": d.id,
            "device_id": d.device_id,
            "device_type": d.device_type,
            "warehouse_name": d.warehouse_name,
            "capacity_tons": d.capacity_tons,
            "city_id": d.city_id
        })
    return results

@router.post("/sensor-data")
def ingest_sensor_data(db: Session = Depends(get_db)):
    # Endpoint to simulate real data ingestion later
    return {"status": "success", "message": "Simulated ingestion"}
