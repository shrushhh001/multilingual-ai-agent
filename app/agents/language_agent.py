
import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from app.models.schemas import LanguageAnalysis


# --------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv(override=True)

API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-4o-mini"
)

if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is missing. "
        "Please configure it in your .env file."
    )


# --------------------------------------------------
# 2. INITIALIZE OPENROUTER CLIENT
# --------------------------------------------------

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Multilingual AI Video Agent"
    }
)


# --------------------------------------------------
# 3. LANGUAGE ANALYSIS AGENT
# --------------------------------------------------

def analyze_user_request(user_input: str) -> LanguageAnalysis:

    if not user_input or not user_input.strip():
        raise ValueError("User input cannot be empty.")

    instructions = """
    You are an intelligent multilingual AI agent
    designed to generate educational short videos.

    YOUR RESPONSIBILITIES:

    1. Detect the language of the user's input.
    2. Identify its language code using ISO 639-1
       wherever available.
    3. Translate the complete user request into English.
    4. Identify the main topic of the requested video.
    5. Determine the preferred narration language.
    6. Identify the visual style.
    7. Extract any additional requirements.

    LANGUAGE RULES:

    - Support Hindi, English, Kannada, Urdu
      and other languages.
    - Detect the original input language correctly.
    - If the user specifies a narration language,
      use that language.
    - Otherwise, use the original input language.
    - Keep the English translation accurate.

    VIDEO RULES:

    - Default duration is exactly 35 seconds.
    - Duration must remain between 30 and 40 seconds.
    - Ignore requests for durations longer than 40 seconds.
    - Divide the video into 5 scenes.
    - Each scene should be 7 seconds long.

    VISUAL RULES:

    - Default visual style is Cinematic.
    - Extract any additional visual instructions.

    OUTPUT RULES:

    Return ONLY a valid JSON object.
    Do not return Markdown or explanations.

    The JSON object must contain these fields:

    {
        "detected_language": "Full language name",
        "detected_language_code": "Language code",
        "english_translation": "English translation",
        "video_topic": "Main video topic",
        "narration_language": "Narration language",
        "video_duration_seconds": 35,
        "visual_style": "Cinematic",
        "additional_requirements": []
    }
    """

    # --------------------------------------------------
    # 4. SEND REQUEST TO OPENROUTER
    # --------------------------------------------------

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": (
                    "Analyze this request and return "
                    "the result in JSON format:\n\n"
                    f"{user_input}"
                )
            }
        ],
        response_format={
            "type": "json_object"
        },
        temperature=0.2
    )

    # --------------------------------------------------
    # 5. EXTRACT AND VALIDATE RESPONSE
    # --------------------------------------------------

    response_content = response.choices[0].message.content

    if not response_content:
        raise ValueError("The AI returned an empty response.")

    try:
        result = json.loads(response_content)

        validated_result = LanguageAnalysis.model_validate(result)

        return validated_result

    except json.JSONDecodeError as error:
        raise ValueError(
            f"The AI returned invalid JSON: {error}"
        ) from error
