import platform

import pytest

from supriya_midi import RtMidiAPI, get_compiled_api


@pytest.mark.skipif(platform.system() != "Linux", reason="Requires Linux")
def test_linux_supports_alsa():
    assert RtMidiAPI.LINUX_ALSA in get_compiled_api()


@pytest.mark.skipif(platform.system() != "Linux", reason="Requires Linux")
def test_linux_supports_jack():
    assert RtMidiAPI.UNIX_JACK in get_compiled_api()


@pytest.mark.skipif(platform.system() != "Darwin", reason="Requires OSX")
def test_macos_supports_coremidi():
    assert RtMidiAPI.MACOSX_CORE in get_compiled_api()


@pytest.mark.skipif(platform.system() != "Windows", reason="Requires Windows")
def test_windows_supports_winmm():
    assert RtMidiAPI.WINDOWS_MM in get_compiled_api()
