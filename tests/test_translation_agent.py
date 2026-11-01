
from app.models.schemas import VideoScript
from app.translation.narration_translator import translate_video_script


def test_hindi_to_kannada_translation():

    hindi_script = VideoScript(
        video_title="छत्रपति शिवाजी महाराज",
        narration_language="Hindi",
        total_duration_seconds=35,
        scenes=[
            {
                "scene_number": 1,
                "duration_seconds": 7,
                "narration": "क्या आप शिवाजी महाराज के बारे में जानते हैं?",
                "visual_prompt": "A cinematic view of Shivaji Maharaj at a fort.",
                "on_screen_text": "शिवाजी महाराज"
            },
            {
                "scene_number": 2,
                "duration_seconds": 7,
                "narration": "उनका जन्म 1630 में हुआ था।",
                "visual_prompt": "A historical view of Shivneri Fort.",
                "on_screen_text": "जन्म: 1630"
            },
            {
                "scene_number": 3,
                "duration_seconds": 7,
                "narration": "उन्होंने स्वराज्य का सपना देखा।",
                "visual_prompt": "A young warrior looking at a fort.",
                "on_screen_text": "स्वराज्य"
            },
            {
                "scene_number": 4,
                "duration_seconds": 7,
                "narration": "1674 में उनका राज्याभिषेक हुआ।",
                "visual_prompt": "A royal coronation ceremony.",
                "on_screen_text": "राज्याभिषेक: 1674"
            },
            {
                "scene_number": 5,
                "duration_seconds": 7,
                "narration": "उनकी विरासत आज भी जीवित है।",
                "visual_prompt": "People remembering Shivaji Maharaj.",
                "on_screen_text": "ಅವರ ಪರಂಪರೆ"
            }
        ]
    )

    translated = translate_video_script(
        video_script=hindi_script,
        target_language="Kannada"
    )

    assert translated.narration_language == "Kannada"
    assert len(translated.scenes) == 5
    assert translated.total_duration_seconds == 35

    for original, result in zip(hindi_script.scenes, translated.scenes):

        assert result.scene_number == original.scene_number
        assert result.duration_seconds == 7
        assert result.visual_prompt == original.visual_prompt
        assert result.narration.strip()
