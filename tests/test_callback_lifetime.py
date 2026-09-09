import gc
import weakref
from typing import Any

import pytest

from supriya_midi import RtMidiAPI
from supriya_midi.rtmidi_ext import RtMidiIn, RtMidiOut


class Callback:
    def __call__(self, *args: Any) -> None:
        pass


class Data:
    pass


def collect() -> None:
    gc.collect()
    gc.collect()


def test_message_callback_owns_and_releases_python_objects(api: RtMidiAPI) -> None:
    midi_in = RtMidiIn(api)
    callback = Callback()
    data = Data()
    callback_ref = weakref.ref(callback)
    data_ref = weakref.ref(data)

    midi_in.set_callback(callback, data)
    del callback, data
    collect()
    assert callback_ref() is not None
    assert data_ref() is not None

    midi_in.cancel_callback()
    collect()
    assert callback_ref() is None
    assert data_ref() is None


@pytest.mark.parametrize("midi_type", [RtMidiIn, RtMidiOut])
def test_replacing_error_callback_releases_previous_objects(
    api: RtMidiAPI, midi_type: Any
) -> None:
    midi = midi_type(api)
    first_callback = Callback()
    first_data = Data()
    first_callback_ref = weakref.ref(first_callback)
    first_data_ref = weakref.ref(first_data)

    midi.set_error_callback(first_callback, first_data)
    del first_callback, first_data
    collect()
    assert first_callback_ref() is not None
    assert first_data_ref() is not None

    midi.set_error_callback(Callback(), Data())
    collect()
    assert first_callback_ref() is None
    assert first_data_ref() is None


def test_deleting_midi_input_releases_callback_objects(api: RtMidiAPI) -> None:
    midi_in = RtMidiIn(api)
    message_callback = Callback()
    message_data = Data()
    error_callback = Callback()
    error_data = Data()
    refs = [
        weakref.ref(message_callback),
        weakref.ref(message_data),
        weakref.ref(error_callback),
        weakref.ref(error_data),
    ]

    midi_in.set_callback(message_callback, message_data)
    midi_in.set_error_callback(error_callback, error_data)
    del message_callback, message_data, error_callback, error_data
    del midi_in
    collect()
    assert all(ref() is None for ref in refs)
