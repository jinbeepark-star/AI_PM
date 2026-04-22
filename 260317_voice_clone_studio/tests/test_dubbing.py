import pytest
from src.voice_clone.cloner import VoiceCloner
from src.voice_clone.dubbing import DubbingPipeline


@pytest.fixture
def cloner() -> VoiceCloner:
    return VoiceCloner()


@pytest.fixture
def profile_id(cloner: VoiceCloner) -> str:
    return cloner.create_profile("sample.wav", name="Narrator")["profile_id"]


@pytest.fixture
def pipeline(cloner: VoiceCloner) -> DubbingPipeline:
    return DubbingPipeline(cloner=cloner)


def test_dub_returns_list(pipeline: DubbingPipeline, profile_id: str) -> None:
    results = pipeline.dub(["Hello", "World"], profile_id)
    assert isinstance(results, list)


def test_dub_length_matches_input(pipeline: DubbingPipeline, profile_id: str) -> None:
    lines = ["Line one", "Line two", "Line three"]
    results = pipeline.dub(lines, profile_id)
    assert len(results) == len(lines)


def test_dub_each_entry_has_required_keys(pipeline: DubbingPipeline, profile_id: str) -> None:
    results = pipeline.dub(["Test"], profile_id)
    required = {"index", "text", "profile_id", "duration_ms", "offset_ms", "format", "status"}
    for entry in results:
        assert required.issubset(entry.keys())


def test_dub_offsets_are_cumulative(pipeline: DubbingPipeline, profile_id: str) -> None:
    results = pipeline.dub(["First line", "Second line"], profile_id)
    assert results[1]["offset_ms"] == results[0]["duration_ms"]


def test_dub_status_success(pipeline: DubbingPipeline, profile_id: str) -> None:
    results = pipeline.dub(["안녕하세요"], profile_id)
    assert results[0]["status"] == "success"


def test_dub_empty_line_skipped(pipeline: DubbingPipeline, profile_id: str) -> None:
    results = pipeline.dub(["Hello", "  ", "World"], profile_id)
    assert results[1]["status"] == "skipped"
    assert results[1]["duration_ms"] == 0


def test_dub_raises_on_empty_list(pipeline: DubbingPipeline, profile_id: str) -> None:
    with pytest.raises(ValueError):
        pipeline.dub([], profile_id)


def test_dub_raises_on_non_list(pipeline: DubbingPipeline, profile_id: str) -> None:
    with pytest.raises(TypeError):
        pipeline.dub("not a list", profile_id)  # type: ignore[arg-type]


def test_dub_raises_on_unknown_profile(pipeline: DubbingPipeline) -> None:
    with pytest.raises(KeyError):
        pipeline.dub(["text"], "bad-id")


def test_total_duration_ms(pipeline: DubbingPipeline, profile_id: str) -> None:
    results = pipeline.dub(["Hello", "World"], profile_id)
    total = pipeline.total_duration_ms(results)
    assert total == results[-1]["offset_ms"] + results[-1]["duration_ms"]


def test_total_duration_ms_empty(pipeline: DubbingPipeline) -> None:
    assert pipeline.total_duration_ms([]) == 0
