
from pydantic import BaseModel, Field, model_validator


class LanguageAnalysis(BaseModel):
    detected_language: str
    detected_language_code: str
    english_translation: str
    video_topic: str
    narration_language: str

    video_duration_seconds: int = Field(
        default=35,
        ge=25,
        le=40
    )

    visual_style: str = "Cinematic"
    additional_requirements: list[str] = Field(default_factory=list)


class VideoScene(BaseModel):
    scene_number: int = Field(ge=1, le=5)
    duration_seconds: int = Field(ge=1, le=40)
    narration: str
    visual_prompt: str
    on_screen_text: str = ""


class VideoScript(BaseModel):
    video_title: str
    narration_language: str

    total_duration_seconds: int = Field(
        ge=25,
        le=40
    )

    scenes: list[VideoScene]

    @model_validator(mode="after")
    def validate_video_structure(self):

        # Exactly 5 scenes
        if len(self.scenes) != 5:
            raise ValueError("Video must contain exactly 5 scenes.")

        # Scene numbering must be sequential
        if [scene.scene_number for scene in self.scenes] != [1, 2, 3, 4, 5]:
            raise ValueError("Scenes must be numbered from 1 to 5.")

        # Total duration must match sum of scene durations
        total_scene_duration = sum(
            scene.duration_seconds for scene in self.scenes
        )

        if total_scene_duration != self.total_duration_seconds:
            raise ValueError(
                "Scene durations must add up to total video duration."
            )

        # Video duration must be between 25 and 40 seconds
        if not 25 <= self.total_duration_seconds <= 40:
            raise ValueError(
                "Video duration must be between 25 and 40 seconds."
            )

        return self
