import base64
import json
from typing import List, Optional

from google import genai
from google.genai import types
from pydantic import BaseModel

from cfg import logger, settings

# Cargar variables de entorno
# load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

if not settings.gemini_api_key:
    raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")


client = genai.Client(api_key=settings.gemini_api_key)


class InvoiceItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float


class InvoiceData(BaseModel):
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    total_amount: Optional[float] = None
    items: List[InvoiceItem] = []


async def process_image_with_gemini(base64_image: str, prompt: str):
    """
    sends a Base64 encoded image to Gemini Pro along with a prompt.
    The prompt should instruct Gemini to extract specific data from the image.
    Returns a JSON response with the extracted data.
    """
    try:
        logger.info("🔍 Starting image processing")
        logger.debug(f"📏 Base64 length: {len(base64_image)}")
        logger.debug(f"💬 Prompt: {prompt[:100]}...")

        # Decode the Base64 image
        try:
            image_bytes = base64.b64decode(base64_image)
            logger.info(
                f"✅ Base64 decoded successfully. Size: {len(image_bytes)} bytes"
            )
        except Exception as e:
            logger.error(f"❌ Error decoding Base64: {e}")
            raise ValueError(f"Error decoding Base64 image: {e}")

        # Create the content for Gemini using the correct syntax
        logger.info("📤 Sending request to Gemini...")
        if not image_bytes:
            raise ValueError("Image bytes are empty after decoding Base64")
        try:
            logger.info("⏳ Waiting for response from Gemini...")
            # Structured response with schema
            response = client.models.generate_content(
                model=settings.model_id,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(text=prompt),
                            types.Part(
                                inline_data=types.Blob(
                                    mime_type="image/jpeg", data=image_bytes
                                )
                            ),
                        ],
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=InvoiceData,
                ),
            )

            logger.info("✅ Response received from Gemini")

            try:
                result = response.model_dump_json()
                logger.info(f"✅ JSON parsed successfully: {type(result)}")
                return result
            except Exception as json_error:
                logger.warning(f"⚠️ Error parsing JSON: {json_error}")
                # Fallback: return text response if JSON parsing fails
                return {
                    "raw_gemini_response": response.text,
                    "error": f"Could not parse Gemini response as JSON: {json_error}",
                }

        except Exception as api_error:
            # Log the error and try a fallback
            logger.error(f"❌ Error in Gemini API call: {api_error}")

            # Fallback: intentar sin esquema estructurado
            logger.info("🔄 Trying without structured schema...")
            try:
                response = client.models.generate_content(
                    model=settings.model_id,
                    contents=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part(
                                    text=prompt
                                    + "\n\nPlease return the response in valid JSON format."
                                ),
                                types.Part(
                                    inline_data=types.Blob(
                                        mime_type="image/jpeg", data=image_bytes
                                    )
                                ),
                            ],
                        )
                    ],
                )

                # response.resolve()
                text_response = response.text.strip()
                logger.info(f"📝 Text response received: {text_response[:200]}...")

                # Clean response if it comes in Markdown code blocks
                if text_response.startswith("```json") and text_response.endswith(
                    "```"
                ):
                    text_response = text_response[7:-3].strip()
                elif text_response.startswith("```") and text_response.endswith("```"):
                    # Remove any code block
                    text_response = text_response[3:-3].strip()

                # Try to parse as JSON
                try:
                    return json.loads(text_response)
                except json.JSONDecodeError as parse_error:
                    logger.warning(f"⚠️ Error parsing JSON: {parse_error}")
                    return {
                        "raw_gemini_response": text_response,
                        "error": f"Could not parse Gemini response as JSON: {parse_error}",
                    }

            except Exception as fallback_error:
                logger.error(f"❌ Error in fallback: {fallback_error}")
                raise Exception(
                    f"Error in both Gemini methods: {api_error}, {fallback_error}"
                )

    except Exception as e:
        logger.error(f"❌ General error in process_image_with_gemini: {e}")
        logger.error(f"❌ Error type: {type(e)}")
        raise Exception(f"Error processing image with Gemini: {e}")


async def process_text_with_gemini(text: str, prompt: str):
    """
    Send a text to Gemini Pro along with a text prompt.
    """
    try:
        logger.info("🔍 Starting text processing with Gemini...")
        logger.info(f"💬 Prompt: {prompt[:100]}...")
        logger.info(f"📝 Text: {text[:100]}...")

        full_prompt = f"{prompt}\n\nText to process: {text}"

        response = client.models.generate_content(
            model=settings.model_id,
            contents=[types.Content(role="user", parts=[types.Part(text=full_prompt)])],
        )

        logger.info("⏳ Waiting for response from Gemini...")
        # response.resolve()
        logger.info("✅ Response received from Gemini")

        text_response = response.text.strip()
        logger.info(f"📝 Text response: {text_response[:200]}...")

        # Clean response if it comes in Markdown code blocks
        if text_response.startswith("```json") and text_response.endswith("```"):
            text_response = text_response[7:-3].strip()
        elif text_response.startswith("```") and text_response.endswith("```"):
            text_response = text_response[3:-3].strip()

        try:
            return json.loads(text_response)
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ Error parsing JSON: {e}")
            return {
                "raw_gemini_response": text_response,
                "error": f"Could not parse Gemini response as JSON: {e}",
            }

    except Exception as e:
        logger.error(f"❌ Error in process_text_with_gemini: {e}")
        raise Exception(f"Error processing text with Gemini: {e}")


# Utility function to test the connection
async def test_gemini_connection():
    """
    Simple function to test that Gemini is working
    """
    try:
        response = client.models.generate_content(
            model=settings.model_id,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text="Say 'Hello, successful connection' in Spanish")
                    ],
                )
            ],
        )
        # response.resolve()
        return {"status": "success", "message": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
