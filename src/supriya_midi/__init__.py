"""
Python bindings for the RtMidi C++ library using nanobind, inspired by
python-rtmidi.
"""

from typing import Any, Callable, Generic, Iterable, TypeAlias, TypeVar

from typing_extensions import Self

from ._midi import RtMidi, RtMidiAPI, RtMidiErrorType, RtMidiIn, RtMidiOut

Callback: TypeAlias = Callable[[Iterable[int], float, Any], None]
ErrorCallback: TypeAlias = Callable[[RtMidiErrorType, str, Any], None]


def _default_error_callback(
    error_type: RtMidiErrorType, error_text: str, data: Any = None
) -> None:
    raise RuntimeError((error_type, error_text))


def get_api_display_name(api: RtMidiAPI) -> str:
    """
    Get the display name of a backend API.

    Args:
        api: The backend API to describe

    Returns:
        The display name of the backend API
    """
    return RtMidi.get_api_display_name(api)


def get_api_name(api: RtMidiAPI) -> str:
    """
    Get the name of a backend API.

    Args:
        api: The backend API to describe

    Returns:
        The name of the backend API
    """
    return RtMidi.get_api_name(api)


def get_compiled_api() -> list[RtMidiAPI]:
    """
    Get the backend APIs supported by this module.

    Returns:
        A list of supported backend APIs
    """
    return RtMidi.get_compiled_api()


def get_compiled_api_by_name(name: str) -> RtMidiAPI:
    """
    Get a supported backend API by case-insensitive name match.

    Args:
        name: The backend API name

    Returns:
        The matching backend API or UNSPECIFIED
    """
    return RtMidi.get_compiled_api_by_name(name)


def get_rtmidi_version() -> str:
    """
    Get the version of RtMidi compiled with this library.

    Returns:
        The RtMidi version string
    """
    return RtMidi.get_version()


def list_ports() -> list[str]:
    """
    Get a list of available MIDI input or output port names.

    Returns:
        A list of available port names
    """
    midi_in = RtMidiIn()
    ports = [
        midi_in.get_port_name(port_number)
        for port_number in range(midi_in.get_port_count())
    ]
    del midi_in
    return ports


R = TypeVar("R", bound=RtMidi)


class MidiBase(Generic[R]):
    """
    Base class for MIDI input and output clients.
    """

    def __init__(self, rt_midi: R) -> None:
        self._rt_midi = rt_midi
        self._error_callback: tuple[ErrorCallback, Any] | None = None
        self._is_deleted: bool = False
        self._port_number: int | None = None
        self.set_error_callback(_default_error_callback)

    def __enter__(self) -> Self:
        """
        Support the context manager protocol.

        ::

            >>> from supriya_midi import MidiOut
            >>>
            >>> with MidiOut().open_port(0) as midi_out:
            ...     midi_out.send_message([0x90, 48, 100])
            ...

        Returns:
            This MIDI client instance.
        """
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """
        Support the context manager protocol.

        Closes any open port on exit.
        """
        self.close_port()

    def cancel_error_callback(self) -> None:
        """
        Cancel the current error callback function and replace it with the
        default error callback.
        """
        self.set_error_callback(_default_error_callback)

    def close_port(self) -> None:
        """
        Close any MIDI port opened via ``open_port``.

        .. note::

            If a virtual port was opened, the MIDI client instance must be
            deleted to close it.
        """
        if self._port_number != -1:
            self._port_number = None
        self._rt_midi.close_port()

    def delete(self) -> None:
        """
        Immediately delete this client's C++ backend.

        When deleting the client (or simply losing a reference to it), Python's
        garbage collector may delay deleting the underlying C++ backend for an
        arbitrary amount of time. Manually deleting ensures the backend is
        freed exactly when you desire it to be freed. This can be especially
        useful when virtual ports have been opened, as they can only be closed
        by deleting the backend.

        .. warning::

           The client must not be used once deleted for risk of segmentation
           fault.
        """
        if not self._is_deleted:
            del self._rt_midi
            self._is_deleted = True

    def get_current_api(self) -> RtMidiAPI:
        """
        Get the backend API used by this client.

        Returns:
            The backend API
        """
        raise NotImplementedError

    def get_port_count(self) -> int:
        """
        Get the number of available MIDI input or output ports.

        Returns:
            The port count
        """
        return self._rt_midi.get_port_count()

    def get_port_name(self, port_number: int = 0) -> str:
        """
        Get the name of the MIDI input or output port at index ``port_number``.

        Args:
            port_number: The index of the port to describe

        Returns:
            The port name
        """
        return self._rt_midi.get_port_name(port_number)

    def get_ports(self) -> list[str]:
        """
        Get a list of available MIDI input or output port names.

        Returns:
            A list of available port names
        """
        return [
            self.get_port_name(port_number)
            for port_number in range(self.get_port_count())
        ]

    def open_port(self, port_number: int = 0, port_name: str = "RtMidi") -> Self:
        """
        Open a MIDI input or output port with the given ``port_number``.

        Args:
            port_number: The port number to open
            port_name: An optional port name to apply when opening a port for
                the first time

        Returns:
            This MIDI client, to facilitate chaining when entering a context
        """
        if self._port_number is not None:
            raise RuntimeError("Port already opened.")
        self._rt_midi.open_port(port_number, port_name)
        self._port_number = port_number
        return self

    def open_virtual_port(self, port_name: str = "RtMidi") -> Self:
        """
        Open a virtual MIDI input or output port.


        .. note::

            Not supported by the Windows backend API.

        Args:
            port_name: An optional port name to apply when opening a port for
                the first time

        Returns:
            This MIDI client, to facilitate chaining when entering a context
        """
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
        """
        Set the MIDI client name.

        .. note::

            Only supported by the ALSA backend API.

        Args:
            client_name: The client name
        """
        if self.get_current_api() in (
            RtMidiAPI.MACOSX_CORE,
            RtMidiAPI.UNIX_JACK,
            RtMidiAPI.WINDOWS_MM,
        ):
            raise NotImplementedError(
                "API backend does not support changing the client name."
            )
        self._rt_midi.set_client_name(client_name)

    def set_error_callback(self, callback: ErrorCallback, data: Any = None) -> None:
        """
        Register a callback callable for backend API errors.

        Error callbacks fire when the C++ backend raises errors, e.g. when
        opening ports that don't exist. Error callbacks may raise errors.

        .. note::

            MIDI clients are instantiated with a default error callback.

        .. note::

            Only one callback may be registered at a time. Registering a new
            callback replaces any previously registered callback.

        Args:
            callback: The error callback callable
            data: Optional additional data to pass as the third argument to the
                callback when invoked
        """
        self._error_callback = (callback, data)
        self._rt_midi.set_error_callback(callback, data)

    def set_port_name(self, port_name: str) -> None:
        """
        Set the name of the currently opened port.

        .. note::

            Only supported by the ALSA and Jack backend APIs.

        Args:
            port_name: The port name
        """
        if self.get_current_api() in (RtMidiAPI.MACOSX_CORE, RtMidiAPI.WINDOWS_MM):
            raise NotImplementedError(
                "API backend does not support changing the port name."
            )
        if self._port_number is None:
            raise RuntimeError("No port currently opened.")
        self._rt_midi.set_port_name(port_name)

    @property
    def is_deleted(self) -> bool:
        """
        True if the client's backend has been deleted.
        """
        return self._is_deleted

    @property
    def is_port_open(self) -> bool:
        """
        True if the client's has a real or virtual port open.
        """
        return self._port_number is not None

    @property
    def port_number(self) -> int | None:
        """
        The client's current port number (or ``-1`` if a virtual port is open)
        otherwise ``None``.
        """
        return self._port_number


class MidiIn(MidiBase[RtMidiIn]):
    """
    A MIDI input client.

    Args:
        api: The backend API to use, if specified, otherwise the first compiled
            backend API
        client_name: The client name
        queue_size_limit: The size of the internal ring buffer used with
            ``get_message`` when no callback has been set
    """

    def __init__(
        self,
        api: RtMidiAPI = RtMidiAPI.UNSPECIFIED,
        client_name: str = "RtMidi Input Client",
        queue_size_limit: int = 1024,
    ) -> None:
        super().__init__(RtMidiIn(api, client_name, queue_size_limit))
        self._callback: tuple[Callback, Any] | None = None

    def cancel_callback(self) -> None:
        """
        ...
        """
        self._rt_midi.cancel_callback()
        self._callback = None

    def get_current_api(self) -> RtMidiAPI:
        """
        Get the backend API used by this client.

        Returns:
            The backend API
        """
        return self._rt_midi.get_current_api()

    def get_message(self) -> tuple[list[int], float]:
        """
        ...

        Returns:
            Pair of the MIDI message and delta timestamp
        """
        return self._rt_midi.get_message()

    def ignore_types(
        self, sysex: bool = True, timing: bool = True, active_sense: bool = True
    ) -> None:
        """
        ...

        Args:
            sysex: ...
            timing: ...
            active_sense: ...
        """
        self._rt_midi.ignore_types(sysex, timing, active_sense)

    def set_buffer_size(self, size: int = 1024, count: int = 4) -> None:
        """
        ...

        Args:
            size: ...
            count: ...
        """
        self._rt_midi.set_buffer_size(size, count)

    def set_callback(self, callback: Callback, data: Any = None) -> None:
        """
        Register a callback callable for MIDI messages.

        .. note::

            Only one callback may be registered at a time. Registering a new
            callback replaces any previously registered callback.

        Args:
            callback: The MIDI message callback callable
            data: Optional additional data to pass as the third argument to the
                callback when invoked
        """
        if self._callback:
            self.cancel_callback()
        self._callback = (callback, data)
        self._rt_midi.set_callback(callback, data)


class MidiOut(MidiBase[RtMidiOut]):
    """
    A MIDI output client.

    Args:
        api: The backend API to use, if specified, otherwise the first compiled
            backend API
        client_name: The client name
    """

    def __init__(
        self,
        api: RtMidiAPI = RtMidiAPI.UNSPECIFIED,
        client_name: str = "RtMidi Output Client",
    ) -> None:
        super().__init__(RtMidiOut(api, client_name))

    def get_current_api(self) -> RtMidiAPI:
        """
        Get the backend API used by this client.

        Returns:
            The backend API
        """
        return self._rt_midi.get_current_api()

    def send_message(self, message: Iterable[int]) -> None:
        """
        Send a MIDI message to the client's output port.

        No validation is performed on the message except that if its longer
        than 3 byes (the standard MIDI message length), the first byte must be
        a start-of-sysex status byte, 0xF0.

        Args:
            message: The MIDI message to send
        """
        if not (message_ := list(message)):
            raise ValueError("Message must not be empty.")
        elif len(message_) > 3 and message_[0] != 0xF0:
            raise ValueError("Messages longer than 3 bytes must start with 0xF0.")
        self._rt_midi.send_message(message_)


__all__ = [
    "MidiBase",
    "MidiIn",
    "MidiOut",
    "RtMidiAPI",
    "RtMidiErrorType",
    "get_api_display_name",
    "get_api_name",
    "get_compiled_apis",
    "get_compiled_apis_by_name",
    "get_version",
]
