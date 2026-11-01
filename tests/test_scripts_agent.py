from app.agents.research_agent import research_topic
from app.agents.scripts_agent import generate_video_script


def test_hindi_video_script():

    research = research_topic("Chhatrapati Shivaji Maharaj")

    result = generate_video_script(
        video_topic="Chhatrapati Shivaji Maharaj",
        research_results=research["research_results"],
        narration_language="Hindi",
        visual_style="Cinematic"
    )

    # Print the generated output
    print("\n========== GENERATED VIDEO SCRIPT ==========")
    print(f"\nTitle: {result.video_title}")
    print(f"Language: {result.narration_language}")
    print(f"Duration: {result.total_duration_seconds} seconds")

    for scene in result.scenes:
        print(f"\n========== SCENE {scene.scene_number} ==========")
        print(f"Duration: {scene.duration_seconds} seconds")
        print(f"\nNarration:\n{scene.narration}")
        print(f"\nVisual Prompt (English):\n{scene.visual_prompt}")
        print(f"\nOn-screen Text:\n{scene.on_screen_text}")

    print("\n=============================================")

    # Validations
    assert result.total_duration_seconds == 35
    assert len(result.scenes) == 5

    for scene in result.scenes:
        assert scene.duration_seconds == 7
        assert scene.narration
        assert scene.visual_prompt