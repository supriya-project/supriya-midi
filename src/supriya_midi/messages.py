"""
MIDI message classes.

Support parsing raw integer sequendces from the RtMidi backend into dataclasses
representing each message type in the MIDI spec, and support serializing those
message dataclasses back into raw integers for sending.
"""

import dataclasses
from typing import ClassVar, Iterator, Sequence, Type

from typing_extensions import Self

from .constants import MidiMessageType


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
        """
        message_class: Type[MidiMessage] = {
            MidiMessageType.ACTIVE_SENSE: ActiveSenseMessage,
            MidiMessageType.AFTERTOUCH: AftertouchMessage,
            MidiMessageType.CHANNEL_PRESSURE: ChannelPressureMessage,
            MidiMessageType.CLOCK: ClockMessage,
            MidiMessageType.CONTINUE: ContinueMessage,
            MidiMessageType.CONTROLLER_CHANGE: ControllerChangeMessage,
            MidiMessageType.META: MetaMessage,
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
        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message):
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
        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message):
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
        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message):
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
        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message):
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
        """
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message):
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
        """
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message):
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
        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message):
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
        """
        return (
            self.type_ | self.channel_id,
            self.transposition & 127 < self.transposition & (127 << 7),
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
        """
        if len(message) < 4:
            raise ValueError
        if any(x > 127 for x in message):
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
        """
        return (self.type_, self.manufacturer_id, *self.data, 0xF7)


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
        """
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls(
            data=message[1],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this quarter frame message into a sequence of integers.
        """
        return (
            self.type_,
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
        """
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls(
            position=message[1] | (message[2] << 7),
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this song position message into a sequence of integers.
        """
        return (
            self.type_,
            self.position & 127,
            self.position & (127 << 7),
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
        """
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls(
            song_id=message[1],
        )

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this song request message into a sequence of integers.
        """
        return (
            self.type_,
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
        """
        if len(message) != 1:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this tune request message into a sequence of integers.
        """
        return (self.type_,)


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
        """
        if len(message) != 1:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this clock message into a sequence of integers.
        """
        return (self.type_,)


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
        """
        if len(message) != 1:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this start message into a sequence of integers.
        """
        return (self.type_,)


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
        """
        if len(message) != 1:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this continue message into a sequence of integers.
        """
        return (self.type_,)


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
        """
        if len(message) != 1:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this stop message into a sequence of integers.
        """
        return (self.type_,)


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
        """
        if len(message) != 1:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this active sense message into a sequence of integers.
        """
        return (self.type_,)


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
        """
        if len(message) != 1:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if MidiMessageType.parse(message[0]) is not cls.type_:
            raise ValueError
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this reset message into a sequence of integers.
        """
        return (self.type_,)


@dataclasses.dataclass(frozen=True)
class MetaMessage(MidiMessage):
    """
    A meta MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.META

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        """
        Parse a sequence of integers into a meta message.
        """
        return cls()

    def serialize(self) -> tuple[int, ...]:
        """
        Serialize this meta message into a sequence of integers.
        """
        return (self.type_,)


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
