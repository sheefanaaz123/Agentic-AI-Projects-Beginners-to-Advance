
"""Gemini agent: tool calling and structured response synthesis."""

import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from schemas import TravelAdvice, TravelRequest
from tools.weather import get_weather


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)


SYSTEM_INSTRUCTION = """
You are a careful weather and travel advice assistant.

Your responsibilities:
1. Use the get_weather tool to obtain weather for the user's
   requested destination and date.
2. Never invent weather observations, forecasts, or API results.
3. Base weather-related advice only on the tool output.
4. Distinguish forecast-based guidance from general travel advice.
5. If data is missing, say that it is unavailable.
6. Do not claim that an activity is completely safe.
7. Give practical packing, outdoor activity, and safety guidance.
8. Do not provide emergency alerts unless they appear in the
   supplied data. Recommend checking official local advisories
   for high-risk outdoor activities.

The user may provide interests such as hiking or sightseeing.
Address those interests where relevant.
"""


def generate_travel_advice(
    request: TravelRequest,
) -> TravelAdvice:
    """Run tool calling, then generate a validated travel report."""

    user_request = request.model_dump(mode="json")

    # Phase 1: Let Gemini choose and execute the weather tool.
    tool_response = client.models.generate_content(
        model=MODEL,
        contents=[
            json.dumps(user_request),
            (
                "Use get_weather for the exact city and travel date. "
                "Return a concise factual summary of the tool result. "
                "If the tool fails or data is unavailable, state that."
            ),
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[get_weather],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False,
                maximum_remote_calls=3,
            ),
            temperature=0.2,
        ),
    )

    weather_facts = tool_response.text or ""

    if not weather_facts.strip():
        raise RuntimeError(
            "The tool-enabled model call returned no text."
        )

    # Phase 2: Synthesize a report using a strict output schema.
    synthesis_prompt = f"""
User request:
{json.dumps(user_request, ensure_ascii=False)}

Weather tool result summary:
{weather_facts}

Create a travel advice report.

Rules:
- Preserve the destination and date from the user request.
- Use only the supplied weather summary for weather measurements.
- Do not invent missing values.
- If weather data is unavailable, explain this in the report.
- Packing suggestions and activity advice must be reasonable
  and clearly grounded in the available information.
- Return every field required by the schema.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=synthesis_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=TravelAdvice,
            temperature=0.2,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty structured response."
        )

    # Validate the model output again at the application boundary.
    return TravelAdvice.model_validate_json(response.text)