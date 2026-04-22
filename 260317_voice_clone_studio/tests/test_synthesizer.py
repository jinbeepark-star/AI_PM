import pytest
from src.voice_clone.synthesizer import TtsSynthesizer, SUPPORTED_FORMATS


@pytest.fixture
def synth() -> TtsSynthesizer:
    return TtsSynthesizer()


def test_synthesize_returns_dict(synth: TtsSynthesizer) -> None:
    result = synth.synthesize("안녕하세요")
    assert isinstance(result, dict)


def test_synthesize_contains_required_keys(synth: TtsSynthesizer) -> None:
    result = synth.synthesize("Hello world")
    required = {"text", "voice_id", "speed", "format", "sample_rate", "duration_ms", "char_count"}
    assert required.issubset(result.keys())


def test_synthesize_duration_ms_positive(synth: TtsSynthesizer) -> None:
    result = synth.synthesize("Test sentence for duration")
    assert result["duration_ms"] > 0


def test_synthesize_speed_affects_duration(synth: TtsSynthesizer) -> None:
    slow = synth.synthesize("same text", speed=0.5)
    fast = synth.synthesize("same text", speed=2.0)
    assert slow["duration_ms"] > fast["duration_ms"]


def test_synthesize_custom_voice_id(synth: TtsSynthesizer) -> None:
    result = synth.synthesize("voice test", voice_id="male_warm")
    assert result["voice_id"] == "male_warm"


def test_synthesize_custom_format(synth: TtsSynthesizer) -> None:
    result = synth.synthesize("format test", format="wav")
    assert result["format"] == "wav"


def test_synthesize_char_count(synth: TtsSynthesizer) -> None:
    text = "12345"
    result = synth.synthesize(text)
    assert result["char_count"] == len(text)


def test_synthesize_raises_on_empty_text(synth: TtsSynthesizer) -> None:
    with pytest.raises(ValueError):
        synth.synthesize("   ")


def test_synthesize_raises_on_non_string(synth: TtsSynthesizer) -> None:
    with pytest.raises(TypeError):
        synth.synthesize(123)  # type: ignore[arg-type]


def test_synthesize_raises_on_invalid_speed(synth: TtsSynthesizer) -> None:
    with pytest.raises(ValueError):
        synth.synthesize("text", speed=-1.0)


def test_synthesize_raises_on_invalid_format(synth: TtsSynthesizer) -> None:
    with pytest.raises(ValueError):
        synth.synthesize("text", format="flac")  # type: ignore[arg-type]


def test_list_voices_returns_list(synth: TtsSynthesizer) -> None:
    voices = synth.list_voices()
    assert isinstance(voices, list)
    assert len(voices) >= 1


def test_list_voices_have_voice_id(synth: TtsSynthesizer) -> None:
    for voice in synth.list_voices():
        assert "voice_id" in voice
