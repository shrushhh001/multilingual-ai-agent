
from langgraph.graph import StateGraph, START, END

from app.graph.state import VideoAgentState
from app.agents.language_agent import analyze_user_request
from app.agents.research_agent import research_topic
from app.agents.scripts_agent import generate_video_script
from app.translation.narration_translator import translate_video_script


# 1. Language Analysis Node
def language_analysis_node(state: VideoAgentState):
    print("\n🌍 Running Language Agent...")

    result = analyze_user_request(state["user_input"])

    return {
        "detected_language": result.detected_language,
        "detected_language_code": result.detected_language_code,
        "english_translation": result.english_translation,
        "video_topic": result.video_topic,

        # User-selected language always takes priority
        "narration_language": (
            state.get("expected_language")
            or result.narration_language
        ),

        "video_duration_seconds": result.video_duration_seconds,
        "visual_style": result.visual_style,
        "additional_requirements": result.additional_requirements
    }


# 2. Research Node
def research_node(state: VideoAgentState):
    print("\n🔎 Running Research Agent...")

    result = research_topic(state["video_topic"])

    return {
        "research_results": result["research_results"],
        "total_sources": result["total_sources"]
    }


# 3. Script Generation Node
def script_generation_node(state: VideoAgentState):
    print("\n📝 Running Script Generation Agent...")

    result = generate_video_script(
        video_topic=state["video_topic"],
        research_results=state["research_results"],
        narration_language="English",
        visual_style=state["visual_style"],
        additional_requirements=state["additional_requirements"]
    )

    return {
        "original_script": result
    }


# 4. Translation Node
def translation_node(state: VideoAgentState):
    target_language = state["expected_language"]

    print(f"\n🌐 Translating script into {target_language}...")

    original_script = state["original_script"]

    if target_language.strip().lower() == "english":
        translated = original_script
    else:
        translated = translate_video_script(
            video_script=original_script,
            target_language=target_language
        )

    return {
        "translated_script": translated
    }


# 5. Build Workflow
def build_video_workflow():

    workflow = StateGraph(VideoAgentState)

    workflow.add_node("language_analysis", language_analysis_node)
    workflow.add_node("research", research_node)
    workflow.add_node("script_generation", script_generation_node)
    workflow.add_node("translation", translation_node)

    workflow.add_edge(START, "language_analysis")
    workflow.add_edge("language_analysis", "research")
    workflow.add_edge("research", "script_generation")
    workflow.add_edge("script_generation", "translation")
    workflow.add_edge("translation", END)

    return workflow.compile()


video_workflow = build_video_workflow()


# 6. Run Workflow and Prepare Final JSON
def run_video_workflow(user_input: str, target_language: str):

    initial_state = {
        "user_input": user_input,
        "original_input": user_input,
        "expected_language": target_language,
        "narration_language": target_language
    }

    result = video_workflow.invoke(initial_state)

    # Final JSON output
    result["final_output"] = {
        "original_input": result["original_input"],
        "expected_language": result["expected_language"],
        "video_script": result["translated_script"].model_dump()
    }

    return result
