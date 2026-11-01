
from app.graph.workflow import run_video_workflow


def test_complete_workflow():

    result = run_video_workflow(
        "छत्रपति शिवाजी महाराज के बारे में एक वीडियो बनाओ।"
    )

    assert result["detected_language_code"] == "hi"
    assert result["video_topic"]
    assert result["narration_language"].lower() == "hindi"
    assert result["video_duration_seconds"] == 35
    assert result["total_sources"] > 0
    assert len(result["research_results"]) > 0
