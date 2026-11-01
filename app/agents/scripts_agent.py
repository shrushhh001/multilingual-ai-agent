
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
# 3. SCRIPT GENERATION AGENT
# -----------------------------------------

def generate_video_script(
    video_topic: str,
    research_results: list[dict],
    narration_language: str,
    visual_style: str = "Cinematic",
    additional_requirements: list[str] | None = None
) -> VideoScript:

    if not video_topic or not video_topic.strip():
        raise ValueError("Video topic cannot be empty.")

    if not research_results:
        raise ValueError("Research results cannot be empty.")

    additional_requirements = additional_requirements or []

    research_context = json.dumps(
        research_results,
        ensure_ascii=False,
        indent=2
    )

    instructions = """
    You are an expert educational video scriptwriter.

    Your task is to create a factual, engaging, short educational
    video script using the supplied research.

    VIDEO STRUCTURE:
    - Total duration must be exactly 35 seconds.
    - Create exactly 5 scenes.
    - Each scene must be exactly 7 seconds.
    - Number scenes from 1 to 5.
    - Narration must fit naturally within each 7-second scene.
    - Keep the complete narration concise and easy to speak.

    LANGUAGE:
    - Write narration entirely in the requested narration language.
    - Do not translate the narration into English unless English
      is the requested narration language.
    - Keep visual prompts entirely in English.
    - On-screen text should use the narration language.

    VISUAL PROMPTS:
    - Create a detailed visual prompt for every scene.
    - Prompts must be suitable for WAN 2.2 video generation.
    - Include subject, setting, action, lighting, camera movement,
      composition and atmosphere where appropriate.
    - Maintain character, clothing, location and visual consistency
      across all five scenes.
    - Avoid anachronisms in historical videos.
    - Do not include narration or dialogue inside visual prompts.

    FACTUAL ACCURACY:
    - Use the supplied research as the factual basis.
    - Do not invent dates, events, quotations or historical claims.
    - If a detail is uncertain, avoid presenting it as fact.

    STORYTELLING:
    - Scene 1: Strong opening hook.
    - Scene 2: Background and context.
    - Scene 3: Important event or explanation.
    - Scene 4: Key achievement or development.
    - Scene 5: Conclusion and memorable takeaway.

    OUTPUT:
    Return only a valid JSON object.
    Do not include Markdown or explanations.

    Required JSON structure:
    {
        "video_title": "Title",
        "narration_language": "Language",
        "total_duration_seconds": 35,
        "scenes": [
            {
                "scene_number": 1,
                "duration_seconds": 7,
                "narration": "Narration in selected language",
                "visual_prompt": "Detailed English visual prompt",
                "on_screen_text": "Short text in narration language"
            }
        ]
    }

    The scenes array must contain exactly 5 scenes.
    """

    user_message = f"""
    VIDEO TOPIC:
    {video_topic}

    NARRATION LANGUAGE:
    {narration_language}

    VISUAL STYLE:
    {visual_style}

    ADDITIONAL REQUIREMENTS:
    {json.dumps(additional_requirements, ensure_ascii=False)}

    RESEARCH INFORMATION:
    {research_context}

    Generate the complete 35-second educational video script.
    Return the result in JSON format.
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
        temperature=0.3
    )

    # -----------------------------------------
    # 5. VALIDATE GENERATED SCRIPT
    # -----------------------------------------

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The AI returned an empty script.")

    try:
        result = json.loads(content)
        return VideoScript.model_validate(result)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"The AI returned invalid JSON: {error}"
        ) from error
