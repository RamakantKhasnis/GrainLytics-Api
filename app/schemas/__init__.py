from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CityBase(BaseModel):
    name: str
    lat: Optional[float] = None
    lng: Optional[float] = None

class City(CityBase):
    id: int
    district_id: int
    class Config:
        from_attributes = True

class DistrictBase(BaseModel):
    name: str

class District(DistrictBase):
    id: int
    state_id: int
    cities: List[City] = []
    class Config:
        from_attributes = True

class StateBase(BaseModel):
    name: str

class State(StateBase):
    id: int
    districts: List[District] = []
    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    device_id: str
    device_type: str
    warehouse_name: str
    capacity_tons: float
    city_id: int

class Device(DeviceBase):
    id: int
    class Config:
        from_attributes = True

class DeviceCreate(DeviceBase):
    pass

class SensorDataCreate(BaseModel):
    device_id: str
    temperature: float
    humidity: float

class SensorData(BaseModel):
    id: int
    device_id: int
    temperature: float
    humidity: float
    timestamp: datetime
    class Config:
        from_attributes = True

class AlertOut(BaseModel):
    id: int
    alert_level: str
    message: str
    timestamp: datetime
    warehouse_name: str
    class Config:
        from_attributes = True

class GeoInsight(BaseModel):
    name: str
    level: str
    avg_temperature: float
    avg_humidity: float
    risk_level: str
    sensor_count: int
    warehouse_count: int
    lat: Optional[float] = None
    lng: Optional[float] = None

class AIChatRequest(BaseModel):
    message: str

class AIChatResponse(BaseModel):
    reply: str
