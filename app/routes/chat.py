from fastapi import APIRouter
from app.schemas import AIChatRequest, AIChatResponse

router = APIRouter()

@router.post("/ai-chat", response_model=AIChatResponse)
def ai_chat(request: AIChatRequest):
    bot_reply = "I am the Grain Storage AI. Based on the current parameters, I recommend increasing ventilation in Zone A warehouses as risk is rising due to external temperature spikes."
    
    msg_l = request.message.lower()
    if "district is most at risk" in msg_l:
        bot_reply = "District 'Aurangabad' is showing the highest risk levels with moisture increasing by 5% in the last 12 hours. Check the Alert Panel for more details."
    elif "do today" in msg_l:
        bot_reply = "Your core action items today: 1) Deploy fans in WH-Alpha, 2) Move out the early batch of wheat from WH-Beta as capacity vs sensor coverage is mismatched."
        
    return AIChatResponse(reply=bot_reply)
