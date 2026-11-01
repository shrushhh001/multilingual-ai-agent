
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from app.models.schemas import VideoScript


# -----------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# -----------------------------------------

load_dotenv(override=True)

API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-4o-mini"
)

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing from .env")


# -----------------------------------------
# 2. INITIALIZE OPENROUTER CLIENT
# -----------------------------------------

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Multilingual AI Video Agent"
    }
)


# -----------------------------------------
# 3. TRANSLATION AGENT
# -----------------------------------------

def translate_video_script(
    video_script: VideoScript,
    target_language: str
) -> VideoScript:

    if not target_language or not target_language.strip():
        raise ValueError("Target language cannot be empty.")

    target_language = target_language.strip()

    # Convert Pydantic model into dictionary
    original_script = video_script.model_dump()

    # Extract only the content requiring translation
    translation_input = {
        "video_title": original_script["video_title"],
        "scenes": [
            {
                "scene_number": scene["scene_number"],
                "narration": scene["narration"],
                "on_screen_text": scene["on_screen_text"]
            }
            for scene in original_script["scenes"]
        ]
    }

    instructions = f"""
    You are an expert multilingual translation agent.

    Translate the supplied educational video script into
    {target_language}.

    RULES:

    1. Translate the video title.
    2. Translate every scene's narration.
    3. Translate every scene's on-screen text.
    4. Preserve the original meaning and factual accuracy.
    5. Use natural, fluent and grammatically correct language.
    6. Use language suitable for spoken educational narration.
    7. Do not summarize or add new information.
    8. Preserve all scene numbers.
    9. Do not modify scene duration.
    10. Do not translate names unnecessarily.
    11. Keep visual prompts in English.
        Visual prompts will be preserved separately by the application.

    Return ONLY a valid JSON object.

    Required structure:

    {{
        "video_title": "Translated title",
        "scenes": [
            {{
                "scene_number": 1,
                "narration": "Translated narration",
                "on_screen_text": "Translated text"
            }}
        ]
    }}

    The output must contain exactly 5 scenes.
    """

    user_message = f"""
    TARGET LANGUAGE: {target_language}

    ORIGINAL VIDEO SCRIPT:

    {json.dumps(translation_input, ensure_ascii=False, indent=2)}

    Translate the complete script.
    """

    # -----------------------------------------
    # 4. CALL OPENROUTER
    # -----------------------------------------

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        response_format={
            "type": "json_object"
        },
        temperature=0.2
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Translation API returned empty output.")

    try:
        translated = json.loads(content)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid translation JSON: {error}"
        ) from error

    # -----------------------------------------
    # 5. VALIDATE AND PRESERVE ORIGINAL DATA
    # -----------------------------------------

    translated_scenes = translated.get("scenes")

    if not isinstance(translated_scenes, list):
        raise ValueError("Translation must contain a scenes list.")

    if len(translated_scenes) != 5:
        raise ValueError("Translation must contain exactly 5 scenes.")

    final_scenes = []

    for original, translated_scene in zip(
        original_script["scenes"],
        translated_scenes
    ):

        if translated_scene.get("scene_number") != original["scene_number"]:
            raise ValueError("Scene numbers were changed during translation.")

        final_scenes.append({
            "scene_number": original["scene_number"],
            "duration_seconds": original["duration_seconds"],
            "narration": translated_scene["narration"],
            "visual_prompt": original["visual_prompt"],
            "on_screen_text": translated_scene["on_screen_text"]
        })

    final_script = {
        "video_title": translated["video_title"],
        "narration_language": target_language,
        "total_duration_seconds": original_script["total_duration_seconds"],
        "scenes": final_scenes
    }

    return VideoScript.model_validate(final_script)
