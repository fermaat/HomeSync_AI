from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from cfg import logger
from src.database import crud
from src.database.connection import get_db
from src.services import gemini_service

router = APIRouter()


class ProcessTicketRequest(BaseModel):
    image_base64: str
    model_prompt: str = "Extract product names, quantities, unit prices, and totals from this purchase receipt. Provide the result in JSON format. Include the purchase date if available."


class VoiceCommandRequest(BaseModel):
    command_text: str


@router.post("/process_ticket")
async def process_ticket_endpoint(
    request: ProcessTicketRequest, db: Session = Depends(get_db)
):
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
        ticket_db = crud.save_gemini_ticket_data(db, model_response_data)

        return {
            "status": "success",
            "message": "Model correctly processed the ticket image.",
            "extracted_data": model_response_data,
            "ticket_id": str(ticket_db.id),
        }
    except Exception as e:
        logger.exception(f"Error in /process_ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/process_voice_command")
async def process_voice_command_endpoint(
    request: VoiceCommandRequest, db: Session = Depends(get_db)
):
    """
    Endpoint para procesar un comando de voz (texto) usando Gemini
    y realizar acciones/consultas en la BD.
    """
    try:
        model_interpretation = await gemini_service.process_text_with_gemini(
            text=request.command_text,
            prompt="Interpret this command related to the shopping list or home inventory. Respond in JSON format with 'action' and 'details'.",
        )

        action = model_interpretation.get("action")
        details = model_interpretation.get("details", {})
        response_message = "couldn't understand the request."

        if action == "category_spending":
            categoria = details.get("category")
            periodo = details.get("period")
            if categoria and periodo:
                end_date = date.today()
                if periodo == "day":
                    start_date = end_date
                elif periodo == "week":
                    start_date = end_date - timedelta(weeks=1)
                elif periodo == "month":
                    start_date = end_date.replace(day=1)
                elif periodo == "year":
                    start_date = end_date.replace(month=1, day=1)
                else:
                    response_message = (
                        "Periodo no válido. Usa 'day', 'week', 'month' o 'year'."
                    )
                    return {"status": "error", "response": response_message}

                items = crud.get_items_by_category_and_date_range(
                    db, categoria, start_date, end_date
                )
                total_gasto = sum(item.precio_total_linea for item in items)
                response_message = f"Your spending on {categoria} during the last {periodo} is {total_gasto:.2f}€."
            else:
                response_message = (
                    "Need category, period and date range to calculate spending"
                )

        elif action == "recommend_shopping":
            item_name = details.get("item")
            if item_name:
                # TODO: rethink logic
                response_message = f"Recommendation for {item_name}: This is an advanced analysis logic that I haven't fully implemented yet, but it reminds me that I need to buy it."  # Placeholder
            else:
                response_message = "I need the item name to recommend."

        elif action == "get_shopping_list":
            # TODO: rethik logic
            response_message = "Your pending shopping list is... (logic to implement)"

        else:
            response_message = "Received command: '{request.command_text}'. Gemini interpreted it as: {model_interpretation}. I can't perform that action yet."

        return {
            "status": "success",
            "response": response_message,
            "gemini_interpretation": model_interpretation,
        }

    except Exception as e:
        logger.exception(f"Error en /procesar_comando_voz: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
