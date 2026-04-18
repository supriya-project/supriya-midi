from typing import Generator

import pytest

from supriya_midi import MidiIn, MidiOut, RtMidi, RtMidiAPI

TESTED_APIS = [
    api
    for api in RtMidi.get_compiled_api()
    if api
    in [
        RtMidiAPI.LINUX_ALSA,
        RtMidiAPI.MACOSX_CORE,
        RtMidiAPI.UNIX_JACK,
        RtMidiAPI.WINDOWS_MM,
    ]
]

IN_CLIENT_NAME = "RtMidi Test Input"
OUT_CLIENT_NAME = "RtMidi Test Output"
IN_PORT_NAME = "testin"
OUT_PORT_NAME = "testout"


@pytest.fixture(params=TESTED_APIS)
def api(request) -> RtMidiAPI:
    return request.param


@pytest.fixture
def midi_in(api: RtMidiAPI) -> Generator[MidiIn, None, None]:
    midi_in = MidiIn(api=api, client_name=IN_CLIENT_NAME)
    assert midi_in.get_current_api() == api
    yield midi_in
    if not midi_in.is_deleted:
        midi_in.close_port()
    del midi_in


@pytest.fixture
def midi_out(api: RtMidiAPI) -> Generator[MidiOut, None, None]:
    midi_out = MidiOut(api=api, client_name=OUT_CLIENT_NAME)
    assert midi_out.get_current_api() == api
    yield midi_out
    if not midi_out.is_deleted:
        midi_out.close_port()
    del midi_out
