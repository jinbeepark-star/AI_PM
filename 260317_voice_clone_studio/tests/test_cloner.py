import pytest
from src.voice_clone.cloner import VoiceCloner


@pytest.fixture
def cloner() -> VoiceCloner:
    return VoiceCloner()


@pytest.fixture
def profile(cloner: VoiceCloner) -> dict:
    return cloner.create_profile("sample/voice.wav", name="Test Speaker")


def test_create_profile_returns_dict(cloner: VoiceCloner) -> None:
    result = cloner.create_profile("audio.wav", name="Alice")
    assert isinstance(result, dict)


def test_create_profile_has_profile_id(cloner: VoiceCloner) -> None:
    result = cloner.create_profile("audio.wav", name="Bob")
    assert "profile_id" in result
    assert isinstance(result["profile_id"], str)
    assert len(result["profile_id"]) > 0


def test_create_profile_status_ready(cloner: VoiceCloner) -> None:
    result = cloner.create_profile("audio.mp3", name="Carol")
    assert result["status"] == "ready"


def test_create_profile_extracts_format(cloner: VoiceCloner) -> None:
    result = cloner.create_profile("path/to/voice.ogg", name="Dan")
    assert result["sample_format"] == "ogg"


def test_create_profile_raises_on_empty_path(cloner: VoiceCloner) -> None:
    with pytest.raises(ValueError):
        cloner.create_profile("", name="Eve")


def test_create_profile_raises_on_empty_name(cloner: VoiceCloner) -> None:
    with pytest.raises(ValueError):
        cloner.create_profile("audio.wav", name="   ")


def test_clone_returns_dict(cloner: VoiceCloner, profile: dict) -> None:
    result = cloner.clone("Hello", profile["profile_id"])
    assert isinstance(result, dict)


def test_clone_status_success(cloner: VoiceCloner, profile: dict) -> None:
    result = cloner.clone("안녕하세요", profile["profile_id"])
    assert result["status"] == "success"


def test_clone_duration_ms_positive(cloner: VoiceCloner, profile: dict) -> None:
    result = cloner.clone("text", profile["profile_id"])
    assert result["duration_ms"] > 0


def test_clone_raises_on_unknown_profile(cloner: VoiceCloner) -> None:
    with pytest.raises(KeyError):
        cloner.clone("text", "nonexistent-id")


def test_clone_raises_on_empty_text(cloner: VoiceCloner, profile: dict) -> None:
    with pytest.raises(ValueError):
        cloner.clone("  ", profile["profile_id"])


def test_get_profile_returns_same_data(cloner: VoiceCloner, profile: dict) -> None:
    fetched = cloner.get_profile(profile["profile_id"])
    assert fetched["profile_id"] == profile["profile_id"]
    assert fetched["name"] == profile["name"]


def test_list_profiles_contains_created(cloner: VoiceCloner, profile: dict) -> None:
    ids = [p["profile_id"] for p in cloner.list_profiles()]
    assert profile["profile_id"] in ids
