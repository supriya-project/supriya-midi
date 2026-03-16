from typing import Any, Callable, Generic, Sequence, TypeVar

from typing_extensions import Self

from ._midi import RtMidi, RtMidiAPI, RtMidiErrorType, RtMidiIn, RtMidiOut


def _default_error_callback(error_type: RtMidiErrorType, message: str) -> None:
    raise RuntimeError((message, error_type))


def get_api_display_name(api: RtMidiAPI) -> str:
    return RtMidi.get_api_display_name(api)


def get_api_name(api: RtMidiAPI) -> str:
    return RtMidi.get_api_name(api)


def get_compiled_api() -> list[RtMidiAPI]:
    return RtMidi.get_compiled_api()


def get_compiled_api_by_name(name: str) -> RtMidiAPI:
    return RtMidi.get_compiled_api_by_name(name)


def get_version() -> str:
    return RtMidi.get_version()


R = TypeVar("R", bound=RtMidi)


class MidiBase(Generic[R]):
    def __init__(self, rt_midi: R) -> None:
        self._rt_midi = rt_midi
        self._error_callback: Callable[[RtMidiErrorType, str], None] | None = None
        self._is_deleted: bool = False
        self._port_number: int | None = None
        self.set_error_callback(_default_error_callback)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close_port()

    def cancel_error_callback(self) -> None:
        self.set_error_callback(_default_error_callback)

    def close_port(self) -> None:
        self._port_number = None
        self._rt_midi.close_port()

    def delete(self) -> None:
        if not self._is_deleted:
            del self._rt_midi
            self._is_deleted = True

    def get_current_api(self) -> RtMidiAPI:
        raise NotImplementedError

    def get_port_count(self) -> int:
        return self._rt_midi.get_port_count()

    def get_port_name(self, port_number: int = 0) -> str:
        return self._rt_midi.get_port_name(port_number)

    def list_ports(self) -> list[str]:
        return [
            self.get_port_name(port_number)
            for port_number in range(self.get_port_count())
        ]

    def open_port(self, port_number: int = 0, port_name: str = "RtMidi") -> Self:
        if self._port_number is not None:
            raise RuntimeError("Port already opened.")
        self._rt_midi.open_port(port_number, port_name)
        self._port_number = port_number
        return self

    def open_virtual_port(self, port_name: str = "RtMidi") -> Self:
        if self.get_current_api() == RtMidiAPI.WINDOWS_MM:
            raise NotImplementedError(
                "Virtual ports are not supported by the Windows MultiMedia API."
            )
        if self._port_number is not None:
            raise RuntimeError("Port already opened.")
        self._rt_midi.open_virtual_port(port_name)
        self._port_number = -1
        return self

    def set_client_name(self, client_name: str) -> None:
        if self.get_current_api() in (
            RtMidiAPI.MACOSX_CORE,
            RtMidiAPI.UNIX_JACK,
            RtMidiAPI.WINDOWS_MM,
        ):
            raise NotImplementedError(
                "API backend does not support changing the client name."
            )
        self._rt_midi.set_client_name(client_name)

    def set_error_callback(
        self, callback: Callable[[RtMidiErrorType, str], None]
    ) -> None:
        self._error_callback = callback
        self._rt_midi.set_error_callback(callback)

    def set_port_name(self, port_name: str) -> None:
        if self.get_current_api() in (RtMidiAPI.MACOSX_CORE, RtMidiAPI.WINDOWS_MM):
            raise NotImplementedError(
                "API backend does not support changing the port name."
            )
        if self._port_number is None:
            raise RuntimeError("No port currently opened.")
        self._rt_midi.set_port_name(port_name)

    @property
    def is_deleted(self) -> bool:
        return self._is_deleted

    @property
    def port_number(self) -> int | None:
        return self._port_number


class MidiIn(MidiBase[RtMidiIn]):
    def __init__(
        self,
        api: RtMidiAPI = RtMidiAPI.UNSPECIFIED,
        name: str | None = None,
        queue_size_limit: int = 1024,
    ) -> None:
        super().__init__(RtMidiIn(api, name or "RtMidi Input Client", queue_size_limit))
        self._callback: Callable[[Sequence[int], float], None] | None = None

    def cancel_callback(self) -> None:
        self._rt_midi.cancel_callback()
        self._callback = None

    def get_current_api(self) -> RtMidiAPI:
        return self._rt_midi.get_current_api()

    def get_message(self) -> tuple[list[int], float]:
        return self._rt_midi.get_message()

    def ignore_types(
        self, sysex: bool = True, timing: bool = True, active_sense: bool = True
    ) -> None:
        self._rt_midi.ignore_types(sysex, timing, active_sense)

    def set_buffer_size(self, size: int = 1024, count: int = 4) -> None:
        self._rt_midi.set_buffer_size(size, count)

    def set_callback(self, callback: Callable[[Sequence[int], float], None]) -> None:
        if self._callback:
            self.cancel_callback()
        self._callback = callback
        self._rt_midi.set_callback(callback)


class MidiOut(MidiBase[RtMidiOut]):
    def __init__(
        self, api: RtMidiAPI = RtMidiAPI.UNSPECIFIED, name: str | None = None
    ) -> None:
        super().__init__(RtMidiOut(api, name or "RtMidi Output Client"))

    def get_current_api(self) -> RtMidiAPI:
        return self._rt_midi.get_current_api()

    def send_message(self, message: Sequence[int]) -> None:
        if not message:
            raise ValueError("Message must not be empty.")
        self._rt_midi.send_message(message)


__all__ = [
    "MidiBase",
    "MidiIn",
    "MidiOut",
    "RtMidiAPI",
    "RtMidiErrorType",
    "get_api_display_name",
    "get_api_name",
    "get_compiled_api",
    "get_compiled_api_by_name",
    "get_version",
]
