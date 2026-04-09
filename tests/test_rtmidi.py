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


@pytest.fixture(params=TESTED_APIS)
def api(request) -> RtMidiAPI:
    return request.param


@pytest.fixture
def midi_in(api: RtMidiAPI) -> Generator[MidiIn, None, None]:
    midi_in = MidiIn(api=api, name="RtMidi Test Input")
    assert midi_in.get_current_api() == api
    yield midi_in
    midi_in.close_port()
    del midi_in


@pytest.fixture
def midi_out(api: RtMidiAPI) -> Generator[MidiOut, None, None]:
    midi_out = MidiOut(api=api, name="RtMidi Test Output")
    assert midi_out.get_current_api() == api
    yield midi_out
    midi_out.close_port()
    del midi_out


def test_MidiIn_port_number(midi_in: MidiIn) -> None:
    assert midi_in.port_number is None
    midi_in.open_port(0)
    assert midi_in.port_number is not None
    midi_in.close_port()
    assert midi_in.port_number is None


def test_MidiOut_port_number(midi_out: MidiOut) -> None:
    assert midi_out.port_number is None
    midi_out.open_port(0)
    assert midi_out.port_number is not None
    midi_out.close_port()
    assert midi_out.port_number is None
