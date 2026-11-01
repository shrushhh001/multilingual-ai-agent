
from typing import TypedDict, Optional

from app.models.schemas import VideoScript


class VideoAgentState(TypedDict, total=False):

    # Original user request and selected language
    user_input: str
    original_input: str
    expected_language: str

    # Language Agent output
    detected_language: str
    detected_language_code: str
    english_translation: str
    video_topic: str
    narration_language: str

    # Video configuration
    video_duration_seconds: int
    visual_style: str
    additional_requirements: list[str]

    # Research Agent output
    research_results: list[dict]
    total_sources: int

    # Script Agent output
    original_script: Optional[VideoScript]

    # Translation Agent output
    translated_script: Optional[VideoScript]

    # Future video generation outputs
    narration_script: Optional[str]
    scene_prompts: Optional[list[dict]]
