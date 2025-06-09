from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from cfg import logger
from src.services import gemini_service

router = APIRouter()


class ProcessTicketRequest(BaseModel):
    image_base64: str
    model_prompt: str = "Extract product names, quantities, unit prices, and totals from this purchase receipt. Provide the result in JSON format. Include the purchase date if available."


class VoiceCommandRequest(BaseModel):
    command_text: str


@router.post("/process_ticket")
async def process_ticket_endpoint(request: ProcessTicketRequest):
    """
    Endpoint to process a ticket image using  AI.
    Expects a Base64 encoded image and a prompt for to extract data.
    Returns a JSON response with the extracted data.
    If an error occurs, it raises an HTTPException with a 500 status code.
    """
    try:
        # This is a json
        model_response_data = await gemini_service.process_image_with_gemini(
            base64_image=request.image_base64, prompt=request.model_prompt
        )

        # TODO BD logic
        # example: crud.save_ticket_data(db, gemini_response_data)

        return {
            "status": "success",
            "message": "Model correctly processed the ticket image.",
            "extracted_data": model_response_data,
        }
    except Exception as e:
        logger.exception(f"Error in /process_ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/process_voice_command")
async def process_voice_command_endpoint(request: VoiceCommandRequest):
    """
    Endpoint to process a voice command (text)
    """
    try:
        # TODO: add a generic way for other providers (e.g:local)
        model_interpretation = await gemini_service.process_text_with_gemini(
            text=request.command_text,
            prompt="Interpret this command related to the shopping list or home inventory. Respond in JSON format with 'action' and 'details'.",
        )
        # TODO: properly handle the modelinterpretation response
        # Ejemplo:
        if model_interpretation.get("action") == "get_shopping_list":
            # items = crud.get_shopping_list(db)
            return {
                "status": "success",
                "response": "Your current shopping list is... (items from DB would go here)",
            }
        elif model_interpretation.get("action") == "add_item":
            # crud.add_item(db, gemini_interpretation.get("details").get("item"))
            return {
                "status": "success",
                "response": f"I added {model_interpretation.get('details', {}).get('item', 'something')}.",
            }
        else:
            return {
                "status": "success",
                "response": f"Received command: '{request.command_text}'. The Model interpreted it as: {model_interpretation}",
                "model_interpretation": model_interpretation,
            }

    except Exception as e:
        logger.exception(f"Error en /procesar_comando_voz: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# ... (otros endpoints si los tienes)
