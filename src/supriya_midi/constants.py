from enum import IntEnum
from typing import SupportsInt

from typing_extensions import Self


class MidiMessageType(IntEnum):
    """
    MIDI message status byte types.
    """

    NOTE_OFF = 0x80
    NOTE_ON = 0x90
    AFTERTOUCH = 0xA0
    CONTROLLER_CHANGE = 0xB0
    PROGRAM_CHANGE = 0xC0
    CHANNEL_PRESSURE = 0xD0
    PITCH_WHEEL = 0xE0
    SYSTEM_EXCLUSIVE = 0xF0
    MIDI_QUARTER_FRAME = 0xF1
    SONG_POSITION_POINTER = 0xF2
    SONG_SELECT = 0xF3
    TUNE_REQUEST = 0xF6
    MIDI_CLOCK = 0xF8
    MIDI_START = 0xFA
    MIDI_CONTINUE = 0xFB
    MIDI_STOP = 0xFC
    ACTIVE_SENSE = 0xFE
    RESET = 0xFF

    @classmethod
    def parse(cls, value: SupportsInt) -> Self:
        """
        Parse a MIDI message type from ``value``, ommitting channel ID if
        given.

        ::

            >>> MidiMessageType.parse(0x90)
            MidiMessageType.NOTE_ON: 144

        ::

            >>> MidiMessageType.parse(0x90 | 3)  # channel 4
            MidiMessageType.NOTE_ON: 144

        ::

            >>> MidiMessageType.parse(0xFF)
            <MidiMessageType.RESET: 255>
        """
        value_ = int(value)
        try:
            return cls(value_)
        except ValueError:
            return cls(value_ >> 4 << 4)
