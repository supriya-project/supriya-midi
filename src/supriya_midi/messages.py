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

    raw_message: tuple[int, ...] | None = dataclasses.field(default=None, kw_only=True)
    type_: ClassVar[MidiMessageType]

    def __iter__(self) -> Iterator[int]:
        raise NotImplementedError

    @classmethod
    def parse(cls, message: Sequence[int]) -> "MidiMessage":
        message_class: Type[MidiMessage] = {
            MidiMessageType.NOTE_OFF: NoteOffMessage,
            MidiMessageType.NOTE_ON: NoteOnMessage,
            MidiMessageType.AFTERTOUCH: AftertouchMessage,
            MidiMessageType.CONTROLLER_CHANGE: ControllerChangeMessage,
            MidiMessageType.PROGRAM_CHANGE: ProgramChangeMessage,
            MidiMessageType.CHANNEL_PRESSURE: ChannelPressureMessage,
            MidiMessageType.PITCH_WHEEL: PitchWheelMessage,
        }[MidiMessageType.parse(message[0])]
        return message_class.parse(message)


@dataclasses.dataclass(frozen=True)
class VoiceMessage(MidiMessage):
    """
    A voice MIDI message.

    Voice messages are associated with one of 16 channel IDs.
    """

    channel_id: int


@dataclasses.dataclass(frozen=True)
class NoteOffMessage(VoiceMessage):
    """
    A note off MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.NOTE_OFF
    note_number: int
    velocity: int

    def __iter__(self) -> Iterator[int]:
        yield self.type_ | self.channel_id
        yield self.note_number
        yield self.velocity

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
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
            raw_message=tuple(message),
        )


@dataclasses.dataclass(frozen=True)
class NoteOnMessage(VoiceMessage):
    """
    A note on MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.NOTE_ON
    note_number: int
    velocity: int

    def __iter__(self) -> Iterator[int]:
        yield self.type_ | self.channel_id
        yield self.note_number
        yield self.velocity

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
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
            raw_message=tuple(message),
        )


@dataclasses.dataclass(frozen=True)
class AftertouchMessage(VoiceMessage):
    """
    An aftertouch MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.AFTERTOUCH
    note_number: int
    pressure: int

    def __iter__(self) -> Iterator[int]:
        yield self.type_ | self.channel_id
        yield self.note_number
        yield self.pressure

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
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
            raw_message=tuple(message),
        )


@dataclasses.dataclass(frozen=True)
class ControllerChangeMessage(VoiceMessage):
    """
    A controller change MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.CONTROLLER_CHANGE
    controller_number: int
    controller_value: int

    def __iter__(self) -> Iterator[int]:
        yield self.type_ | self.channel_id
        yield self.controller_number
        yield self.controller_value

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
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
            raw_message=tuple(message),
        )


@dataclasses.dataclass(frozen=True)
class ProgramChangeMessage(VoiceMessage):
    """
    A program change MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.PROGRAM_CHANGE
    program_number: int

    def __iter__(self) -> Iterator[int]:
        yield self.type_ | self.channel_id
        yield self.program_number

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            program_number=message[1],
            raw_message=tuple(message),
        )


@dataclasses.dataclass(frozen=True)
class ChannelPressureMessage(VoiceMessage):
    """
    A channel pressure MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.CHANNEL_PRESSURE
    pressure: int

    def __iter__(self) -> Iterator[int]:
        yield self.type_ | self.channel_id
        yield self.pressure

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        if len(message) != 2:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            pressure=message[1],
            raw_message=tuple(message),
        )


@dataclasses.dataclass(frozen=True)
class PitchWheelMessage(VoiceMessage):
    """
    A pitch/modulation wheel MIDI message.
    """

    type_: ClassVar[MidiMessageType] = MidiMessageType.PITCH_WHEEL
    transposition: int

    def __iter__(self) -> Iterator[int]:
        yield self.type_ | self.channel_id
        yield self.transposition & 127
        yield self.transposition & (127 << 7)

    @classmethod
    def parse(cls, message: Sequence[int]) -> Self:
        if len(message) != 3:
            raise ValueError
        if any(x > 127 for x in message):
            raise ValueError
        if (message_type := MidiMessageType.parse(message[0])) is not cls.type_:
            raise ValueError
        return cls(
            channel_id=message[0] ^ message_type,
            transposition=message[0] | (message[1] << 7),
            raw_message=tuple(message),
        )


__all__ = [
    "AftertouchMessage",
    "ChannelPressureMessage",
    "ControllerChangeMessage",
    "MidiMessage",
    "NoteOffMessage",
    "NoteOnMessage",
    "PitchWheelMessage",
    "ProgramChangeMessage",
    "VoiceMessage",
]
