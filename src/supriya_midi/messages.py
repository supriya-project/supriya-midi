"""
MIDI message classes.

Support parsing raw integer sequendces from the RtMidi backend into dataclasses
representing each message type in the MIDI spec, and support serializing those
message dataclasses back into raw integers for sending.
"""

import dataclasses
from collections.abc import Sequence
from typing import ClassVar

from typing_extensions import Self

from .constants import MetaMessageType, MidiMessageType


@dataclasses.dataclass(frozen=True)
class MidiMessage:
    """
    A MIDI message.
    """

    type_: ClassVar[MidiMessageType]

    @classmethod
    def parse(cls, message: Sequence[int]) -> "MidiMessage":
        """
        Parse a sequence of integers into a MIDI message.

        Use this method on the parent class to parse any valid sequence of
        integers into the appropriate subclass.
        """
        message_class: type[MidiMessage] = {
            MidiMessageType.ACTIVE_SENSE: ActiveSenseMessage,
            MidiMessageType.AFTERTOUCH: AftertouchMessage,
            MidiMessageType.CHANNEL_PRESSURE: ChannelPressureMessage,
            MidiMessageType.CLOCK: ClockMessage,
            MidiMessageType.CONTINUE: ContinueMessage,
            MidiMessageType.CONTROLLER_CHANGE: ControllerChangeMessage,
            MidiMessageType.NOTE_OFF: NoteOffMessage,
            MidiMessageType.NOTE_ON: NoteOnMessage,
            MidiMessageType.PITCH_WHEEL: PitchWheelMessage,
            MidiMessageType.PROGRAM_CHANGE: ProgramChangeMessage,
            MidiMessageType.QUARTER_FRAME: QuarterFrameMessage,
            MidiMessageType.RESET: ResetMessage,
            MidiMessageType.SONG_POSITION: SongPositionMessage,
            MidiMessageType.SONG_REQUEST: SongRequestMessage,
            MidiMessageType.START: StartMessage,
            MidiMessageType.STOP: StopMessage,
            MidiMessageType.SYSTEM_EXCLUSIVE: SystemExclusiveMessage,
            MidiMessageType.TUNE_REQUEST: TuneRequestMessage,
        }[MidiMessageType.parse(message[0])]
        if message_class is ResetMessage and len(message) > 1:
            return MetaMessage.parse(message)
        return message_class.parse(message)

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this MIDI message into a sequence of integers.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class NoteOffMessage(MidiMessage):
    """
    A note off MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.NOTE_OFF
    channel_id: int
    note_number: int
    velocity: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a note off message.

        ::

            >>> MidiMessage.parse([0x83, 0x3E, 0x78])
            NoteOffMessage(channel_id=3, note_number=62, velocity=120)

        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            note_number=message[1],
            velocity=message[2],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this note off message into a sequence of integers.

        ::

            >>> NoteOffMessage(channel_id=3, note_number=62, velocity=120).serialize()
            (131, 62, 120)

        """
        return (
            self.type_ | self.channel_id,
            self.note_number,
            self.velocity,
        )


@dataclasses.dataclass(frozen=True)
class NoteOnMessage(MidiMessage):
    """
    A note on MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.NOTE_ON
    channel_id: int
    note_number: int
    velocity: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a note on message.

        ::

            >>> MidiMessage.parse([0x92, 0x3D, 0x78])
            NoteOnMessage(channel_id=2, note_number=61, velocity=120)

        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            note_number=message[1],
            velocity=message[2],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this note on message into a sequence of integers.

        ::

            >>> NoteOnMessage(channel_id=2, note_number=61, velocity=120).serialize()
            (146, 61, 120)

        """
        return (
            self.type_ | self.channel_id,
            self.note_number,
            self.velocity,
        )


@dataclasses.dataclass(frozen=True)
class AftertouchMessage(MidiMessage):
    """
    An aftertouch MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.AFTERTOUCH
    channel_id: int
    note_number: int
    pressure: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into an aftertouch message.

        ::

            >>> MidiMessage.parse([0xA4, 0x3F, 0x79])
            AftertouchMessage(channel_id=4, note_number=63, pressure=121)

        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            note_number=message[1],
            pressure=message[2],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this after touch message into a sequence of integers.

        ::

            >>> AftertouchMessage(channel_id=4, note_number=63, pressure=121).serialize()
            (164, 63, 121)

        """
        return (
            self.type_ | self.channel_id,
            self.note_number,
            self.pressure,
        )


@dataclasses.dataclass(frozen=True)
class ControllerChangeMessage(MidiMessage):
    """
    A controller change MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.CONTROLLER_CHANGE
    channel_id: int
    controller_number: int
    controller_value: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a controller change message.

        ::

            >>> MidiMessage.parse([0xB6, 0x07, 0x10])
            ControllerChangeMessage(channel_id=6, controller_number=7, controller_value=16)

        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            controller_number=message[1],
            controller_value=message[2],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this controller change message into a sequence of integers.

        ::

            >>> ControllerChangeMessage(channel_id=6, controller_number=7, controller_value=16).serialize()
            (182, 7, 16)

        """
        return (
            self.type_ | self.channel_id,
            self.controller_number,
            self.controller_value,
        )


@dataclasses.dataclass(frozen=True)
class ProgramChangeMessage(MidiMessage):
    """
    A program change MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.PROGRAM_CHANGE
    channel_id: int
    program_number: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a program change message.

        ::

            >>> MidiMessage.parse([0xC6, 0x07])
            ProgramChangeMessage(channel_id=6, program_number=7)

        """
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            program_number=message[1],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this program change message into a sequence of integers.

        ::

            >>> ProgramChangeMessage(channel_id=6, program_number=7).serialize()
            (198, 7)

        """
        return (
            self.type_ | self.channel_id,
            self.program_number,
        )


@dataclasses.dataclass(frozen=True)
class ChannelPressureMessage(MidiMessage):
    """
    A channel pressure MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.CHANNEL_PRESSURE
    channel_id: int
    pressure: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a channel pressure message.

        ::

            >>> MidiMessage.parse([0xD6, 0x35])
            ChannelPressureMessage(channel_id=6, pressure=53)

        """
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            pressure=message[1],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this channel pressure message into a sequence of integers.

        ::

            >>> ChannelPressureMessage(channel_id=6, pressure=53).serialize()
            (214, 53)

        """
        return (
            self.type_ | self.channel_id,
            self.pressure,
        )


@dataclasses.dataclass(frozen=True)
class PitchWheelMessage(MidiMessage):
    """
    A pitch/modulation wheel MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.PITCH_WHEEL
    channel_id: int
    transposition: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a pitch wheel message.

        ::

            >>> MidiMessage.parse([0xE3, 0x54, 0x39])
            PitchWheelMessage(channel_id=3, transposition=7380)

        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            transposition=message[1] | (message[2] << 7),
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this pitch wheel message into a sequence of integers.

        ::

            >>> PitchWheelMessage(channel_id=3, transposition=7380).serialize()
            (227, 84, 57)

        """
        return (
            self.type_ | self.channel_id,
            self.transposition & 127,
            self.transposition >> 7,
        )


@dataclasses.dataclass(frozen=True)
class SystemExclusiveMessage(MidiMessage):
    """
    A system exclusive MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.SYSTEM_EXCLUSIVE
    manufacturer_id: int
    data: tuple[int, ...]

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a system exclusive message.

        ::

            >>> MidiMessage.parse([0xF0, 0x41, 0x01, 0x34, 0xF7])
            SystemExclusiveMessage(manufacturer_id=65, data=(1, 52))

        """
        if len(message) < 4:
            raise ValueError
        if any(x > 127 for x in message[1:-1]):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        if message[-1] != 0xF7:
            raise ValueError
        return cls(
            manufacturer_id=message[1],
            data=tuple(message[2:-1]),
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this system exclusive message into a sequence of integers.

        ::

            >>> SystemExclusiveMessage(manufacturer_id=65, data=(1, 52)).serialize()
            (240, 65, 1, 52, 247)

        """
        return (int(self.type_), self.manufacturer_id, *self.data, 0xF7)


@dataclasses.dataclass(frozen=True)
class QuarterFrameMessage(MidiMessage):
    """
    A quarter frame MIDI message.

    TODO: Implement second byte parsing usefully.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.QUARTER_FRAME
    data: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a quarter frame message.

        ::

            >>> MidiMessage.parse([0xF1, 0x36])
            QuarterFrameMessage(data=54)

        """
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls(
            data=message[1],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this quarter frame message into a sequence of integers.

        ::

            >>> QuarterFrameMessage(data=54).serialize()
            (241, 54)

        """
        return (
            int(self.type_),
            self.data,
        )


@dataclasses.dataclass(frozen=True)
class SongPositionMessage(MidiMessage):
    """
    A song position MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.SONG_POSITION
    position: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a song position message.

        ::

            >>> MidiMessage.parse([0xF2, 0x00, 0x08])
            SongPositionMessage(position=8)

        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls(
            position=message[2] | (message[1] << 7),
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this song position message into a sequence of integers.

        ::

            >>> SongPositionMessage(position=8).serialize()
            (242, 0, 8)

        """
        return (
            int(self.type_),
            self.position >> 7,
            self.position & 127,
        )


@dataclasses.dataclass(frozen=True)
class SongRequestMessage(MidiMessage):
    """
    A song request MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.SONG_REQUEST
    song_id: int

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a song request message.

        ::

            >>> MidiMessage.parse([0xF3, 0x01])
            SongRequestMessage(song_id=1)

        """
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message[1:]):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls(
            song_id=message[1],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this song request message into a sequence of integers.

        ::

            >>> SongRequestMessage(song_id=1).serialize()
            (243, 1)

        """
        return (
            int(self.type_),
            self.song_id,
        )


@dataclasses.dataclass(frozen=True)
class TuneRequestMessage(MidiMessage):
    """
    A tune request MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.TUNE_REQUEST

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a tune request message.

        ::

            >>> MidiMessage.parse([0xF6])
            TuneRequestMessage()

        """
        if len(message) != 1:
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this tune request message into a sequence of integers.

        ::

            >>> TuneRequestMessage().serialize()
            (246,)

        """
        return (int(self.type_),)


@dataclasses.dataclass(frozen=True)
class ClockMessage(MidiMessage):
    """
    A clock MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.CLOCK

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a clock message.

        ::

            >>> MidiMessage.parse([0xF8])
            ClockMessage()

        """
        if len(message) != 1:
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this clock message into a sequence of integers.

        ::

            >>> ClockMessage().serialize()
            (248,)

        """
        return (int(self.type_),)


@dataclasses.dataclass(frozen=True)
class StartMessage(MidiMessage):
    """
    A start MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.START

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a start message.

        ::

            >>> MidiMessage.parse([0xFA])
            StartMessage()

        """
        if len(message) != 1:
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this start message into a sequence of integers.

        ::

            >>> StartMessage().serialize()
            (250,)

        """
        return (int(self.type_),)


@dataclasses.dataclass(frozen=True)
class ContinueMessage(MidiMessage):
    """
    A continue MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.CONTINUE

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a continue message.

        ::

            >>> MidiMessage.parse([0xFB])
            ContinueMessage()

        """
        if len(message) != 1:
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this continue message into a sequence of integers.

        ::

            >>> ContinueMessage().serialize()
            (251,)

        """
        return (int(self.type_),)


@dataclasses.dataclass(frozen=True)
class StopMessage(MidiMessage):
    """
    A stop MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.STOP

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a stop message.

        ::

            >>> MidiMessage.parse([0xFC])
            StopMessage()

        """
        if len(message) != 1:
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this stop message into a sequence of integers.

        ::

            >>> StopMessage().serialize()
            (252,)

        """
        return (int(self.type_),)


@dataclasses.dataclass(frozen=True)
class ActiveSenseMessage(MidiMessage):
    """
    An active sense MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.ACTIVE_SENSE

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into an active sense message.

        ::

            >>> MidiMessage.parse([0xFE])
            ActiveSenseMessage()

        """
        if len(message) != 1:
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this active sense message into a sequence of integers.

        ::

            >>> ActiveSenseMessage().serialize()
            (254,)

        """
        return (int(self.type_),)


@dataclasses.dataclass(frozen=True)
class ResetMessage(MidiMessage):
    """
    A reset MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.RESET

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a reset message.

        ::

            >>> MidiMessage.parse([0xFF])
            ResetMessage()

        """
        if len(message) != 1:
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this reset message into a sequence of integers.

        ::

            >>> ResetMessage().serialize()
            (255,)

        """
        return (int(self.type_),)


@dataclasses.dataclass(frozen=True)
class MetaMessage(MidiMessage):
    """
    A meta MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.META
    meta_type: MetaMessageType
    data: tuple[int, ...]

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a meta message.

        A time signature meta message:

        ::

            >>> MidiMessage.parse([0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08])
            MetaMessage(meta_type=<MetaMessageType.TIME_SIGNATURE: 88>, data=(4, 2, 24, 8))

        A copyright notice meta message:

        ::

            >>> MidiMessage.parse([0xFF, 0x02, 0x1E, 0xA9, 0x20, 0x32, 0x30, 0x30, 0x39, 0x20, 0x4B, 0x61, 0x6C, 0x69, 0x6F, 0x70, 0x61, 0x20, 0x50, 0x75, 0x62, 0x6C, 0x69, 0x73, 0x68, 0x69, 0x6E, 0x67, 0x2C, 0x20, 0x4C, 0x4C, 0x43])
            MetaMessage(meta_type=<MetaMessageType.COPYRIGHT_NOTICE: 2>, data=(169, 32, 50, 48, 48, 57, 32, 75, 97, 108, 105, 111, 112, 97, 32, 80, 117, 98, 108, 105, 115, 104, 105, 110, 103, 44, 32, 76, 76, 67))

        An end-of-track meta message:

        ::

            >>> MidiMessage.parse([0xFF, 0x2F, 0x00])
            MetaMessage(meta_type=<MetaMessageType.END_OF_TRACK: 47>, data=())

        """
        if len(message) < 3:
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        if any(x > 255 for x in message):
            raise ValueError
        return cls(
            meta_type=MetaMessageType(message[1]),
            data=tuple(message[3:]),
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this meta message into a sequence of integers.

        A time signature meta message:

        ::

            >>> MetaMessage(meta_type=MetaMessageType.TIME_SIGNATURE, data=(4, 2, 24, 8)).serialize()
            (255, 88, 4, 4, 2, 24, 8)

        A copyright notice meta message:

        ::

            >>> MetaMessage(meta_type=MetaMessageType.COPYRIGHT_NOTICE, data=(169, 32, 50, 48, 48, 57, 32, 75, 97, 108, 105, 111, 112, 97, 32, 80, 117, 98, 108, 105, 115, 104, 105, 110, 103, 44, 32, 76, 76, 67)).serialize()
            (255, 2, 30, 169, 32, 50, 48, 48, 57, 32, 75, 97, 108, 105, 111, 112, 97, 32, 80, 117, 98, 108, 105, 115, 104, 105, 110, 103, 44, 32, 76, 76, 67)

        An end-of-track meta message:

        ::

            >>> MetaMessage(meta_type=MetaMessageType.END_OF_TRACK, data=()).serialize()
            (255, 47, 0)

        """
        return (
            int(self.type_),
            int(self.meta_type),
            len(self.data),
            *self.data,
        )


__all__ = [
    "ActiveSenseMessage",
    "AftertouchMessage",
    "ChannelPressureMessage",
    "ClockMessage",
    "ContinueMessage",
    "ControllerChangeMessage",
    "MetaMessage",
    "MidiMessage",
    "MidiMessage",
    "NoteOffMessage",
    "NoteOnMessage",
    "PitchWheelMessage",
    "ProgramChangeMessage",
    "QuarterFrameMessage",
    "ResetMessage",
    "SongPositionMessage",
    "SongRequestMessage",
    "StartMessage",
    "StopMessage",
    "SystemExclusiveMessage",
    "TuneRequestMessage",
]
