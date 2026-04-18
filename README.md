# supriya-midi

Supriya MIDI is a [nanobind](https://github.com/wjakob/nanobind)-based Python
binding for the C++ [RtMidi](https://github.com/thestk/rtmidi) library,
providing a simple cross-platform API for realtime MIDI input and output.

This library is heavily inspired by the venerable
[python-rtmidi](https://spotlightkid.github.io/python-rtmidi/) library, which,
at the time of this writing, hasn't seen a release in a number of years. I
started this library so that I could have pre-compiled binary wheels for Python
3.13+.

I've tried to keep this library's API very close to its inspiration's, but
there are some minor differences:

- Supriya MIDI uses integer enums for the API and error type constants.
- Supriya MIDI's MIDI message callback takes three arguments (message,
  timestamp, data) vs python-rtmidi's two argument callback (message/timestamp
  pair, data).
- Supriya MIDI has a single custom exception class vs python-rtmidi's variety
  of exceptions.

Most code that works with
[python-rtmidi](https://spotlightkid.github.io/python-rtmidi/) should be easily
adaptable to Supriya MIDI.

## Installation

Via pip:

```
pip install supriya-midi
```

## Usage

Open an output port and send MIDI messages to it:

```python
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
```

Open an input port and handle incoming MIDI messages with a custom callback:


```python
from supriya_midi import MidiIn

def callback(message, timestamp, data=None):
    print(f"Received {message=}")

midi_in = MidiIn()
midi_in.set_callback(callback)

if midi_in.get_ports():
    midi_in.open_port(0)
else:
    midi_in.open_virtual_port("My virtual output")
```
