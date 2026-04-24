"""
Python bindings for the RtMidi C++ library using nanobind, inspired by
python-rtmidi.
"""

from ._version import __version__, __version_info__
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
from .rtmidi_ext import RtMidiAPI, RtMidiErrorType

__all__ = [
    "MidiBase",
    "MidiIn",
    "MidiOut",
    "RtMidiAPI",
    "RtMidiError",
    "RtMidiErrorType",
    "__version__",
    "__version_info__",
    "get_api_display_name",
    "get_api_name",
    "get_compiled_api_by_name",
    "get_compiled_apis",
    "get_rtmidi_version",
    "list_ports",
]
