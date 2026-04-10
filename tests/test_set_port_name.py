import pytest

from supriya_midi import MidiIn, MidiOut, RtMidiAPI

from .conftest import OUT_CLIENT_NAME, OUT_PORT_NAME, TESTED_APIS


@pytest.fixture(params=TESTED_APIS)
def api(request) -> RtMidiAPI:
    if (api := request.param) not in [RtMidiAPI.LINUX_ALSA, RtMidiAPI.UNIX_JACK]:
        pytest.xfail(f"API {api} does not support setting port names.")
    return api


def test_set_port_name(midi_in: MidiIn, midi_out: MidiOut) -> None:
    midi_out.open_virtual_port(port_name=OUT_PORT_NAME)
    for port in midi_in.get_ports():
        client, port = port.split(":", 1)
        if client.startswith(OUT_CLIENT_NAME) and port.startswith(OUT_PORT_NAME):
            break
    else:
        raise Exception("No matching port found")
    midi_out.set_port_name("new_port")
    for port in midi_in.get_ports():
        client, port = port.split(":", 1)
        if client.startswith(OUT_CLIENT_NAME) and port.startswith("new_port"):
            break
