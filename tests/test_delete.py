from supriya_midi import MidiIn, MidiOut


def test_MidiIn_delete(midi_in: MidiIn, midi_out: MidiOut) -> None:
    initial_ports = midi_out.get_ports()
    midi_in.open_virtual_port("My virtual output")
    ports_before = midi_out.get_ports()
    assert len(ports_before) == len(initial_ports) + 1
    midi_in.delete()
    ports_after = midi_out.get_ports()
    assert set(initial_ports) == set(ports_after)
    assert midi_in.is_deleted
    midi_in.delete()
    assert midi_in.is_deleted  # idempotency


def test_MidiOut_delete(midi_in: MidiIn, midi_out: MidiOut) -> None:
    initial_ports = midi_in.get_ports()
    midi_out.open_virtual_port("My virtual output")
    ports_before = midi_in.get_ports()
    assert len(ports_before) == len(initial_ports) + 1
    midi_out.delete()
    ports_after = midi_in.get_ports()
    assert set(initial_ports) == set(ports_after)
    assert midi_out.is_deleted
    midi_out.delete()
    assert midi_out.is_deleted  # idempotency
