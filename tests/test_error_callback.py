import os
from typing import Any
from unittest import mock

import pytest

from supriya_midi import MidiIn, MidiOut, RtMidiErrorType


def test_MidiIn_default_error_callback(midi_in: MidiIn) -> None:
    with pytest.raises(RuntimeError):
        midi_in.open_port(midi_in.get_port_count() + 1)


def test_MidiOut_default_error_callback(midi_out: MidiOut) -> None:
    with pytest.raises(RuntimeError):
        midi_out.open_port(midi_out.get_port_count() + 1)


@pytest.mark.parametrize("data", [None, 42, "foo bar"])
def test_MidiIn_set_error_callback(midi_in: MidiIn, data: Any) -> None:
    error_callback = mock.Mock()
    midi_in.set_error_callback(error_callback, data=data)
    midi_in.open_port(midi_in.get_port_count() + 1)
    expected_error_type = (
        RtMidiErrorType.NO_DEVICES_FOUND
        if os.environ.get("CI")
        else RtMidiErrorType.INVALID_PARAMETER
    )
    assert error_callback.mock_calls == [
        mock.call(
            expected_error_type,
            mock.ANY,
            data,
        )
    ]


@pytest.mark.parametrize("data", [None, 42, "foo bar"])
def test_MidiOut_set_error_callback(midi_out: MidiOut, data: Any) -> None:
    error_callback = mock.Mock()
    midi_out.set_error_callback(error_callback, data=data)
    midi_out.open_port(midi_out.get_port_count() + 1)
    expected_error_type = (
        RtMidiErrorType.NO_DEVICES_FOUND
        if os.environ.get("CI")
        else RtMidiErrorType.INVALID_PARAMETER
    )
    assert error_callback.mock_calls == [
        mock.call(
            expected_error_type,
            mock.ANY,
            data,
        )
    ]


def test_MidiIn_cancel_error_callback(midi_in: MidiIn) -> None:
    error_callback = mock.Mock()
    midi_in.set_error_callback(error_callback)
    midi_in.cancel_error_callback()
    with pytest.raises(RuntimeError):
        midi_in.open_port(midi_in.get_port_count() + 1)
    assert error_callback.mock_calls == []


def test_MidiOut_cancel_error_callback(midi_out: MidiOut) -> None:
    error_callback = mock.Mock()
    midi_out.set_error_callback(error_callback)
    midi_out.cancel_error_callback()
    with pytest.raises(RuntimeError):
        midi_out.open_port(midi_out.get_port_count() + 1)
    assert error_callback.mock_calls == []
