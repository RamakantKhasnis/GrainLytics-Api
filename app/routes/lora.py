import base64
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.emc_calculator import calculate_emc, assess_storage_risk

router = APIRouter()

# Schema for an incoming Webhook from a standard LoRa network (e.g. The Things Network TTN)
class LoraPayload(BaseModel):
    device_id: str
    grain_type: str = "wheat"
    payload_base64: str

@router.post("/webhook")
def receive_lora_uplink(payload: LoraPayload):
    """
    Acts as a Webhook receiver for physical LoRa Hardware. 
    A LoRa antenna on the warehouse roof receives small sensor data packets and forwards them here in Base64 format.
    """
    try:
        # Step 1: Decode the encrypted radio base64 payload
        # Standard LoRa payloads are encoded so they take up less radio bandwidth (bytes).
        decoded_bytes = base64.b64decode(payload.payload_base64)
        decoded_string = decoded_bytes.decode('utf-8')
        
        # Step 2: Parse the JSON (We assume the sensor sent a tiny JSON string like '{"temp": 28, "hum": 65}')
        sensor_data = json.loads(decoded_string)
        
        temperature = sensor_data.get("temp")
        humidity = sensor_data.get("hum")
        
        if temperature is None or humidity is None:
            raise HTTPException(status_code=400, detail="Invalid sensor formatting in payload")
            
        # Step 3: Run the advanced Grain Science Mathematical Equations
        computed_emc = calculate_emc(
            grain_type=payload.grain_type, 
            temperature_c=temperature, 
            humidity_percent=humidity
        )
        
        health_status = assess_storage_risk(computed_emc, payload.grain_type)
        
        # In a complete build, this data would now be pushed into the SQL Database (SensorData table)
        
        return {
            "status": "success",
            "message": "LoRa Payload Decoded and Analyzed",
            "device": payload.device_id,
            "grain": payload.grain_type.capitalize(),
            "raw_temperature": temperature,
            "raw_humidity": humidity,
            "scientific_calculated_emc": computed_emc,
            "biological_risk_status": health_status
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Base64 encoded string is not valid JSON Data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LoRa Gateway Error: {str(e)}")

@router.get("/emc-curve")
def get_emc_curve(grain_type: str = "wheat", temperature_c: float = 25.0):
    """
    Calculates a full EMC curve (10% to 90% humidity) for a given grain at a constant temperature.
    Used for drawing dynamic scientific charts on the frontend.
    """
    curve_data = []
    
    # We plot from 10% to 90% Humidity in steps of 5
    for hum in range(10, 95, 5):
        emc_val = calculate_emc(grain_type, temperature_c, float(hum))
        curve_data.append({
            "humidity": hum,
            "emc": emc_val
        })
        
    return {
        "status": "success",
        "grain_type": grain_type.capitalize(),
        "temperature_c": temperature_c,
        "curve": curve_data
    }
