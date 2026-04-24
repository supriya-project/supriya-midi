import pytest

from supriya_midi import (
    RtMidiAPI,
    get_api_display_name,
    get_api_name,
    get_compiled_api_by_name,
    get_compiled_apis,
    get_rtmidi_version,
)

pytestmark = pytest.mark.ci


@pytest.mark.parametrize(
    "api, expected_display_name",
    [
        (RtMidiAPI.LINUX_ALSA, "ALSA"),
        (RtMidiAPI.MACOSX_CORE, "CoreMidi"),
        (RtMidiAPI.RTMIDI_DUMMY, "Dummy"),
        (RtMidiAPI.UNIX_JACK, "Jack"),
        (RtMidiAPI.UNSPECIFIED, "Unknown"),
        (RtMidiAPI.WINDOWS_MM, "Windows MultiMedia"),
        (RtMidiAPI.WEB_MIDI, "Web MIDI API"),
    ],
)
def test_get_api_display_name(api: RtMidiAPI, expected_display_name: str) -> None:
    assert get_api_display_name(api) == expected_display_name


@pytest.mark.parametrize(
    "api, expected_name",
    [
        (RtMidiAPI.LINUX_ALSA, "alsa"),
        (RtMidiAPI.MACOSX_CORE, "core"),
        (RtMidiAPI.RTMIDI_DUMMY, "dummy"),
        (RtMidiAPI.UNIX_JACK, "jack"),
        (RtMidiAPI.UNSPECIFIED, "unspecified"),
        (RtMidiAPI.WINDOWS_MM, "winmm"),
        (RtMidiAPI.WEB_MIDI, "web"),
    ],
)
def test_get_api_name(api: RtMidiAPI, expected_name: str) -> None:
    assert get_api_name(api) == expected_name


def test_get_compiled_apis() -> None:
    assert len(compiled_apis := get_compiled_apis()) > 0
    assert all(api <= RtMidiAPI.RTMIDI_DUMMY for api in compiled_apis)
    # validate that a non-dummy API is present
    assert any(api < RtMidiAPI.RTMIDI_DUMMY for api in compiled_apis)


@pytest.mark.parametrize(
    "name, expected_api",
    [
        ("alsa", RtMidiAPI.LINUX_ALSA),
        ("core", RtMidiAPI.MACOSX_CORE),
        ("dummy", RtMidiAPI.RTMIDI_DUMMY),
        ("jack", RtMidiAPI.UNIX_JACK),
        ("winmm", RtMidiAPI.WINDOWS_MM),
        ("web", RtMidiAPI.WEB_MIDI),
    ],
)
def test_get_compiled_api_by_name(name: str, expected_api: RtMidiAPI) -> None:
    api = get_compiled_api_by_name(name)
    if expected_api in get_compiled_apis():
        assert api == expected_api
    else:
        assert api == RtMidiAPI.UNSPECIFIED


def test_get_rtmidi_version() -> None:
    assert get_rtmidi_version() == "6.0.0"
