import time
from typing import Any, Iterable

import pytest

from supriya_midi import MidiIn, MidiOut, RtMidiAPI, list_ports

from .conftest import OUT_PORT_NAME, TESTED_APIS

DELAY = 0.1
NOTE_ON = [0x90, 48, 100]
NOTE_OFF = [0x80, 48, 16]
SYSEX_IDENTITY_REQUEST = [0xF0, 0x7E, 0x7F, 6, 1, 0xF7]


@pytest.fixture(params=TESTED_APIS)
def api(request) -> RtMidiAPI:
    if (api := request.param) not in [
        RtMidiAPI.LINUX_ALSA,
        RtMidiAPI.MACOSX_CORE,
        RtMidiAPI.UNIX_JACK,
    ]:
        pytest.xfail(f"API {api} does not support setting port names.")
    return api


def set_up_loopback(midi_in: MidiIn, midi_out: MidiOut) -> None:
    # TODO: find better solution than this hack-ish strategy to find out
    # the port number of the virtual output port, which we have to use,
    # because for ALSA virtual ports, their name includes the client id.
    # See: https://github.com/thestk/rtmidi/issues/88
    ports_before = list_ports()
    midi_out.open_virtual_port(port_name=OUT_PORT_NAME)
    ports_after = midi_in.get_ports()
    midi_out_port_name = list(set(ports_after).difference(ports_before))[0]
    for port_number, port in enumerate(ports_after):
        if port == midi_out_port_name:
            midi_in.open_port(port_number)
            break
    else:
        raise IOError("Could not find MIDI output port.")


def test_virtual_port_number(midi_in: MidiIn, midi_out: MidiOut) -> None:
    # virtual ports can't be closed
    assert midi_in.port_number is None
    midi_in.open_virtual_port()
    assert midi_in.port_number == -1
    midi_in.close_port()
    assert midi_in.port_number == -1

    assert midi_out.port_number is None
    midi_out.open_virtual_port()
    assert midi_out.port_number == -1
    midi_out.close_port()
    assert midi_out.port_number == -1


def test_send_and_get_message(midi_in: MidiIn, midi_out: MidiOut) -> None:
    set_up_loopback(midi_in, midi_out)
    midi_out.send_message(NOTE_ON)
    midi_out.send_message(NOTE_OFF)
    time.sleep(DELAY)
    event_1 = midi_in.get_message()
    event_2 = midi_in.get_message()
    assert isinstance(event_1, tuple)
    assert isinstance(event_2, tuple)
    assert event_1[0] == NOTE_ON
    assert event_2[0] == NOTE_OFF


def test_send_supports_iterator(midi_in: MidiIn, midi_out: MidiOut) -> None:
    set_up_loopback(midi_in, midi_out)
    midi_out.send_message(iter(NOTE_ON))
    time.sleep(DELAY)
    event = midi_in.get_message()
    assert isinstance(event, tuple)
    assert event[0] == NOTE_ON


def test_send_raises_if_message_too_long(midi_in: MidiIn, midi_out: MidiOut) -> None:
    with pytest.raises(ValueError):
        midi_out.send_message([1, 2, 3, 4])


def test_send_raises_if_message_empty(midi_in: MidiIn, midi_out: MidiOut) -> None:
    with pytest.raises(ValueError):
        midi_out.send_message([])
    with pytest.raises(ValueError):
        midi_out.send_message(iter([]))


def test_send_accepts_sysex(midi_in: MidiIn, midi_out: MidiOut) -> None:
    set_up_loopback(midi_in, midi_out)
    midi_in.ignore_types(sysex=False)
    midi_out.send_message(SYSEX_IDENTITY_REQUEST)
    time.sleep(DELAY)
    event = midi_in.get_message()
    assert isinstance(event, tuple)
    assert event[0] == SYSEX_IDENTITY_REQUEST


def test_callback(midi_in: MidiIn, midi_out: MidiOut) -> None:

    def callback(message: Iterable[int], timestamp: float, data: Any = None) -> None:
        messages.append((message, data))

    set_up_loopback(midi_in, midi_out)

    messages = []
    midi_in.set_callback(callback, data=42)
    midi_out.send_message(NOTE_ON)
    midi_out.send_message(NOTE_OFF)
    time.sleep(DELAY)
    assert messages == [(NOTE_ON, 42), (NOTE_OFF, 42)]

    messages = []
    midi_in.cancel_callback()
    midi_out.send_message(NOTE_ON)
    midi_out.send_message(NOTE_OFF)
    time.sleep(DELAY)
    assert messages == []


def test_set_buffer_size(midi_in: MidiIn, midi_out: MidiOut) -> None:
    midi_in.set_buffer_size(1024, 4)
    test_callback(midi_in, midi_out)
