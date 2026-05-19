"""
Python bindings for the RtMidi C++ library using nanobind, inspired by
python-rtmidi.
"""

from ._version import __version__, __version_info__
from .constants import MidiMessageType
from .core import (
    MidiBase,
    MidiIn,
    MidiOut,
    RtMidiError,
    get_api_display_name,
    get_api_name,
    get_compiled_api_by_name,
    get_compiled_apis,
    get_rtmidi_version,
    list_ports,
)
from .messages import (
    AftertouchMessage,
    ChannelPressureMessage,
    ControllerChangeMessage,
    MidiMessage,
    NoteOffMessage,
    NoteOnMessage,
    PitchWheelMessage,
    ProgramChangeMessage,
)
from .rtmidi_ext import RtMidiAPI, RtMidiErrorType

__all__ = [
    "ActiveSenseMessage",
    "AftertouchMessage",
    "ChannelPressureMessage",
    "ClockMessage",
    "ContinueMessage",
    "ControllerChangeMessage",
    "MetaMessage",
    "MidiBase",
    "MidiIn",
    "MidiMessage",
    "MidiMessageType",
    "MidiOut",
    "NoteOffMessage",
    "NoteOnMessage",
    "PitchWheelMessage",
    "ProgramChangeMessage",
    "QuarterFrameMessage",
    "ResetMessage",
    "RtMidiAPI",
    "RtMidiError",
    "RtMidiErrorType",
    "SongPositionMessage",
    "SongRequestMessage",
    "StartMessage",
    "StopMessage",
    "SystemExclusiveMessage",
    "TuneRequestMessage",
    "__version__",
    "__version_info__",
    "get_api_display_name",
    "get_api_name",
    "get_compiled_api_by_name",
    "get_compiled_apis",
    "get_rtmidi_version",
    "list_ports",
]
