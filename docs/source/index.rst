:hero: a Python binding for RtMidi

Supriya MIDI (|release|)
========================

Supriya MIDI is a `nanobind`_-based Python binding for the C++ `RtMidi`_
library, providing a simple cross-platform API for realtime MIDI input and
output.

This library is heavily inspired by the venerable `python-rtmidi`_ library,
which, at the time of this writing, hasn't seen a release in a number of years.
I started this library so that I could have pre-compiled binary wheels
for Python 3.13+.

I've tried to keep this library's API very close to its inspiration's, but
there are some minor differences:

- Supriya MIDI uses integer enums for the API and error type constants.
- Supriya MIDI's MIDI message callback takes three arguments (message,
  timestamp, data) vs python-rtmidi's two argument callback (message/timestamp
  pair, data).
- Supriya MIDI has a single custom exception class vs python-rtmidi's variety
  of exceptions.

Most code that works with `python-rtmidi`_ should be easily adaptable to
Supriya MIDI.

| xoxo,
| `joséphine`_

..  toctree::
    :maxdepth: 2
    :hidden:

    installation
    basic-usage
    api/index
    changelog

..  _RtMidi: https://github.com/thestk/rtmidi
..  _joséphine: https://josephine-wolf-oberholtzer.com/
..  _nanobind: https://github.com/wjakob/nanobind
..  _python-rtmidi: https://spotlightkid.github.io/python-rtmidi/
