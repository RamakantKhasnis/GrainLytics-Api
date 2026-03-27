from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import State, District, City, Device

router = APIRouter()

@router.get("/locations")
def get_all_locations(db: Session = Depends(get_db)):
    states = db.query(State).all()
    results = []
    for s in states:
        results.append({
            "id": s.id,
            "name": s.name,
            "districts": [
                {
                    "id": d.id, 
                    "name": d.name,
                    "cities": [{"id": c.id, "name": c.name, "lat": c.lat, "lng": c.lng} for c in d.cities]
                } for d in s.districts
            ]
        })
    return results

@router.get("/geo-insights/{level}")
def get_geo_insights(level: str, db: Session = Depends(get_db)):
    if level not in ["state", "district", "city"]:
        raise HTTPException(status_code=400, detail="Invalid level")

    # Mock response depending on the scope
    if level == "state":
        states = db.query(State).all()
        return [
            {"name": s.name, "avg_temperature": 24.5, "avg_humidity": 55.0, "risk_level": "MODERATE", "sensor_count": 50, "warehouse_count": 10, "lat": 20.0, "lng": 77.0} for s in states
        ]
    elif level == "district":
        dists = db.query(District).all()
        return [
            {"name": d.name, "avg_temperature": 25.1, "avg_humidity": 50.0, "risk_level": "LOW", "sensor_count": 15, "warehouse_count": 3, "lat": 19.5, "lng": 76.5} for d in dists
        ]
    elif level == "city":
        cities = db.query(City).all()
        return [
            {"name": c.name, "avg_temperature": 26.0, "avg_humidity": 45.0, "risk_level": "HIGH", "sensor_count": 5, "warehouse_count": 1, "lat": c.lat, "lng": c.lng} for c in cities
        ]

@router.get("/weather/{location}")
def get_weather(location: str):
    # Mock external weather API
    return {
        "location": location,
        "current": {"temp": 28, "condition": "Sunny", "humidity": 40},
        "forecast": [
            {"hour": "10:00", "temp": 29},
            {"hour": "14:00", "temp": 32},
            {"hour": "18:00", "temp": 27}
        ]
    }
