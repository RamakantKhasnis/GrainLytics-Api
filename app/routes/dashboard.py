from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Device, SensorData, RiskAnalysis, Alert

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    # Mock data aggregation
    total_devices = db.query(Device).count()
    active_alerts = db.query(Alert).filter(Alert.is_active == True).count()
    
    # Get latest sensor data (mocked simulation)
    # Since sqlite might not easily grouped by max ID in simple query, we just simulate dashboard numbers
    avg_temp = db.query(func.avg(SensorData.temperature)).scalar() or 22.5
    avg_humidity = db.query(func.avg(SensorData.humidity)).scalar() or 55.0

    return {
        "kpis": {
            "total_sensors": total_devices,
            "active_alerts": active_alerts,
            "average_temperature": round(avg_temp, 1),
            "average_humidity": round(avg_humidity, 1)
        },
        "trends": { # mock trends for 24h
            "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
            "temperature": [20, 19, 21, 26, 28, 24],
            "humidity": [60, 62, 58, 50, 48, 55]
        }
    }

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(10).all()
    results = []
    for a in alerts:
        results.append({
            "id": a.id,
            "alert_level": a.alert_level,
            "message": a.message,
            "timestamp": a.timestamp.isoformat(),
            "warehouse_name": a.device.warehouse_name if a.device else "Unknown"
        })
    return results
