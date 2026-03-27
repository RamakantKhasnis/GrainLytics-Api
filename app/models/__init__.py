from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    districts = relationship("District", back_populates="state")

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    state_id = Column(Integer, ForeignKey("states.id"))
    state = relationship("State", back_populates="districts")
    cities = relationship("City", back_populates="district")

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"))
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    district = relationship("District", back_populates="cities")
    devices = relationship("Device", back_populates="city")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    device_type = Column(String)  # "Temperature & Humidity"
    warehouse_name = Column(String)
    capacity_tons = Column(Float, default=0.0)
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City", back_populates="devices")
    sensor_data = relationship("SensorData", back_populates="device")
    alerts = relationship("Alert", back_populates="device")
    risk_analysis = relationship("RiskAnalysis", back_populates="device")

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    device = relationship("Device", back_populates="sensor_data")

class RiskAnalysis(Base):
    __tablename__ = "risk_analysis"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    risk_level = Column(String) # LOW, MODERATE, HIGH
    reason = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    device = relationship("Device", back_populates="risk_analysis")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    alert_level = Column(String) # Safe, Warning, Critical
    message = Column(String)
    is_active = Column(Boolean, default=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    device = relationship("Device", back_populates="alerts")
