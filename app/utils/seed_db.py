from sqlalchemy.orm import Session
from app.database import engine, get_db, Base
from app.models import State, District, City, Device, SensorData, RiskAnalysis, Alert

def generate_mock_data():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = next(get_db())
    
    # Check if empty
    if db.query(State).first():
        print("Database already seeded")
        return
        
    s1 = State(name="Maharashtra")
    db.add(s1)
    db.commit()
    db.refresh(s1)
    
    d1 = District(name="Aurangabad", state_id=s1.id)
    d2 = District(name="Pune", state_id=s1.id)
    db.add_all([d1, d2])
    db.commit()
    
    c1 = City(name="Vaijapur", district_id=d1.id, lat=19.92, lng=74.72)
    c2 = City(name="Shirur", district_id=d2.id, lat=18.82, lng=74.37)
    db.add_all([c1, c2])
    db.commit()
    
    # Generate Devices
    dev1 = Device(device_id="DEV001", device_type="Temp & Humidity", warehouse_name="WH-Alpha", capacity_tons=500.0, city_id=c1.id)
    dev2 = Device(device_id="DEV002", device_type="Temp & Humidity", warehouse_name="WH-Beta", capacity_tons=1200.0, city_id=c2.id)
    db.add_all([dev1, dev2])
    db.commit()
    
    # Add some initial sensor data
    sd1 = SensorData(device_id=dev1.id, temperature=28.5, humidity=65.0)
    sd2 = SensorData(device_id=dev2.id, temperature=24.1, humidity=45.0)
    db.add_all([sd1, sd2])
    
    # Add Alerts
    a1 = Alert(device_id=dev1.id, alert_level="Critical", message="Moisture rising rapidly. Ventilation required.", is_active=True)
    a2 = Alert(device_id=dev2.id, alert_level="Warning", message="Temperature nearing 25C limit for stored Wheat.", is_active=True)
    db.add_all([a1, a2])
    
    db.commit()
    print("Database seeding completed.")

if __name__ == "__main__":
    generate_mock_data()
