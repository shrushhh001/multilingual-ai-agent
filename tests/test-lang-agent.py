import pytest

from app.agents.language_agent import analyze_user_request


def test_hindi_input():

    user_input = "छत्रपति शिवाजी महाराज के बारे में एक वीडियो बनाओ।"

    result = analyze_user_request(user_input)

    assert result.detected_language_code == "hi"
    assert result.narration_language.lower() == "hindi"
    assert result.video_topic
    assert result.video_duration_seconds == 35


def test_english_input():

    user_input = "Create an educational video about the solar system."

    result = analyze_user_request(user_input)

    assert result.detected_language_code == "en"
    assert result.narration_language.lower() == "english"
    assert result.video_duration_seconds == 35


def test_kannada_input():

    user_input = "ಹಂಪಿಯ ಇತಿಹಾಸದ ಬಗ್ಗೆ ಒಂದು ವಿಡಿಯೋ ಮಾಡಿ."

    result = analyze_user_request(user_input)

    assert result.detected_language_code == "kn"
    assert result.narration_language.lower() == "kannada"
    assert result.video_duration_seconds == 35


def test_custom_narration_language():

    user_input = "शिवाजी महाराज के बारे में वीडियो बनाओ, narration English में चाहिए."

    result = analyze_user_request(user_input)

    assert result.detected_language_code == "hi"
    assert result.narration_language.lower() == "english"
    assert result.video_duration_seconds == 35


def test_default_duration():

    user_input = "Explain artificial intelligence."

    result = analyze_user_request(user_input)

    assert result.video_duration_seconds == 35