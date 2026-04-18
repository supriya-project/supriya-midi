Basic usage
===========

Output
------

Open an output port and send MIDI messages out of it:

..  code:: python

    import time
    from supriya_midi import MidiOut

    midi_out = MidiOut()

    if midi_out.get_ports():
        midi_out.open_port(0)
    else:
        midi_out.open_virtual_port("My virtual output")

    with midi_out:
        note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
        note_off = [0x80, 60, 0]
        midi_out.send_message(note_on)
        time.sleep(0.5)
        midi_out.send_message(note_off)
        time.sleep(0.1)

    del midiout

Input
-----

Open an input port and handle incoming MIDI messages with a custom callback:

..  code:: python

    from supriya_midi import MidiIn

Loopback
--------

Connect a virtual output to an input:

..  code:: python

    from supriya_midi import MidiIn, MidiOut
