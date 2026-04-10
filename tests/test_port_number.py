from supriya_midi import MidiIn, MidiOut


def test_MidiIn_port_number(midi_in: MidiIn) -> None:
    assert midi_in.port_number is None
    midi_in.open_port(0)
    assert midi_in.port_number is not None
    midi_in.close_port()
    assert midi_in.port_number is None


def test_MidiOut_port_number(midi_out: MidiOut) -> None:
    assert midi_out.port_number is None
    midi_out.open_port(0)
    assert midi_out.port_number is not None
    midi_out.close_port()
    assert midi_out.port_number is None
