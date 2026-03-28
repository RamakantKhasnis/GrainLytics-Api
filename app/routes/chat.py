import random
import re
from fastapi import APIRouter
from app.schemas import AIChatRequest, AIChatResponse

router = APIRouter()

# --- THE MOCK AI BRAIN ---
# We build a massive "brain" directly into the code so no API keys or costs are needed!

GRAIN_KNOWLEDGE = {
    "wheat": "Wheat requires strict moisture control (below 14%). If humidity spikes above 65%, aeration fans must be activated immediately to prevent fungal growth.",
    "corn": "Corn is highly susceptible to aflatoxin if stored above 15% moisture. Keep temperatures below 15°C (59°F) and run ventilation cycles every 48 hours.",
    "rice": "Rice storage is critical; if relative humidity exceeds 60%, the kernel can crack or grow mold. Ensure constant airflow in your silos.",
    "barley": "Barley is resilient but should be kept around 12% moisture. Watch entirely for heat pockets forming in the center of the storage bin.",
    "oats": "Oats have a thicker husk reducing moisture transfer but are still at risk. Keep storage temperature steady around 10-15°C to avoid rancidity.",
    "sorghum": "Sorghum can rapidly heat up if stored fresh. Ensure it is dried to at least 13% before binning, and monitor the Risk Chart for sudden heat spikes.",
    "rye": "Rye is prone to ergot mold if left in damp conditions. Keep humidity extremely low and use the Alerts Panel to track sudden weather changes.",
    "soybeans": "Soybeans are dangerous if stored too wet; their high oil content can lead to spontaneous combustion. Do not let moisture exceed 13%.",
    "millet": "Millet is a small grain, meaning it compacts tightly. This restricts airflow, so you must use forced-air ventilation to keep moisture below 12%.",
    "quinoa": "Quinoa's outer coating (saponin) protects it slightly, but it must remain exceptionally dry (below 10% moisture) to retain its premium quality."
}

GENERAL_RESPONSES = {
    "temperature": [
        "If you see a temperature spike, I recommend activating the warehouse cooling fans remotely and checking the affected sector on your geo-map.",
        "Your top priority during a temperature rise is ventilation. Move the oldest bags out first.",
        "Elevated temperature means elevated risk. Check the Analytics page to see if this is an isolated incident or affecting the whole warehouse."
    ],
    "humidity": [
        "High humidity causes grain spoilage fast. Turn on the dehumidifiers in the affected zones immediately.",
        "Moisture is the enemy. Ensure all ventilation hatches are open and the current batch is shifted if moisture levels cross 60%."
    ],
    "risk": [
        "Based on current data, Aurangabad and Pune sectors have the highest risk levels right now.",
        "Risk is calculated using a combination of internal temperature, external weather, and silo capacity. You have two severe alerts pending."
    ],
    "hello": [
        "Hello! I am your free, zero-cost Grain Intelligence Assistant. What can I help you with today?",
        "Hi there! Welcome to GrainLytics. Ask me about any grain, storage conditions, or risks!"
    ],
    "who are you": [
        "I am the GrainLytics AI Assistant, specifically designed to help you manage grain warehouses and prevent spoilage.",
        "I am the custom intelligence engine built into GrainLytics. I don't cost a penny, and I know exactly how to manage agricultural storage!"
    ],
}

def analyze_and_respond(message: str) -> str:
    msg = message.lower()
    
    # 1. Check for specific grain names
    for grain, info in GRAIN_KNOWLEDGE.items():
        if grain in msg:
            return f"🌾 **{grain.capitalize()} Intelligence:** {info}"
            
    # 2. Check for general keywords (intents)
    for intent, responses in GENERAL_RESPONSES.items():
        if intent in msg:
            return random.choice(responses)
            
    # 3. Handle random/unrelated questions by pivoting back to the website's expertise
    fallback_responses = [
        "As an expert in Grain Storage on the GrainLytics platform, I focus on temperature, humidity, and preventing spoilage. Could you ask me about your specific warehouses or a grain like Corn or Wheat?",
        "That's an interesting question! However, my core programming is dedicated entirely to agricultural storage analytics. Do you need help with a particular silo's risk levels instead?",
        "I'm dedicated strictly to your GrainLytics data. I can tell you about storage conditions for Wheat, Rice, Soybeans, and more. What would you like to analyze?",
        "I analyze sensor data to save crops from spoiling! If you have any questions about ventilation, alerts, or specific grains, let me know!"
    ]
    return random.choice(fallback_responses)

@router.post("/ai-chat", response_model=AIChatResponse)
def ai_chat(request: AIChatRequest):
    bot_reply = analyze_and_respond(request.message)
    return AIChatResponse(reply=bot_reply)
