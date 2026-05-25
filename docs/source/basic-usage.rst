Basic usage
===========

Output
------

Open an output port and send MIDI messages to it:

..  code:: python

    import time
    from supriya_midi import MidiOut

    midi_out = MidiOut()

    if midi_out.get_ports():
        midi_out.open_port(0)
    else:
        midi_out.open_virtual_port("My virtual output")

    with midi_out:
        note_on = [0x90, 60, 112]  # channel 1, middle C, velocity 112
        note_off = [0x80, 60, 0]
        midi_out.send_message(note_on)
        time.sleep(0.5)
        midi_out.send_message(note_off)
        time.sleep(0.1)

    del midi_out

Input
-----

Open an input port and handle incoming MIDI messages with a custom callback:

..  code:: python

    from supriya_midi import MidiIn

    def callback(message, timestamp, data=None):
        print(f"Received {message=}")

    midi_in = MidiIn()
    midi_in.set_callback(callback)

    if midi_in.get_ports():
        midi_in.open_port(0)
    else:
        midi_in.open_virtual_port("My virtual output")


Message dataclasses
-------------------

Open an input port and handle incoming MIDI messages with a custom callback,
converting the raw integer sequence into message dataclasses:

..  code:: python

    from supriya_midi import MidiIn, MidiMessage

    def callback(message, timestamp, data=None):
        message_dataclass = MidiMessage.parse(message)
        print(f"Received {message_dataclass=}")

    midi_in = MidiIn()
    midi_in.set_callback(callback)

    if midi_in.get_ports():
        midi_in.open_port(0)
    else:
        midi_in.open_virtual_port("My virtual output")
