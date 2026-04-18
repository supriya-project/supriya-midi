Installation
============

From PyPI
---------

Supriya MIDI tries to provide pre-compiled wheels for all current Python
versions and major operating systems.

You can install Supriya MIDI from PyPI:

..  md-tab-set::

    ..  md-tab-item:: Via pip:

        ..  code-block:: console

            josephine@laptop$ pip install supriya-midi

    ..  md-tab-item:: Via `uv`_:

        ..  code-block:: console

            josephine@laptop$ uv add supriya-midi

From source
-----------

You can also build Supriya MIDI locally from source. Make sure you've fulfilled
the :ref:`build requirements <build-requirements>` before proceeding.

Clone the repository (making sure to recursively clone all submodules):

..  code:: bash

    $ git clone --recursive https://github.com/supriya-project/supriya-midi.git

Then install as normal:

..  md-tab-set::

    ..  md-tab-item:: Via pip:

        ..  code-block:: console

            josephine@laptop$ pip install -v -e .

    ..  md-tab-item:: Via `uv`_:

        ..  code-block:: console

            josephine@laptop$ uv pip install -v -e .

.. _build-requirements:

Build requirements
------------------

Supriya MIDI requires a working C++ compiler and build environment, including
CMake.

Supriya MIDI makes use of `scikit-build-core`_ as its build backend.

At least one working backend needs to be available on your system:

- Linux: ALSA and/or Jack
- OSX: CoreMIDI and/or Jack
- Windows: MultiMedia (MM)

..  _scikit-build-core: https://github.com/scikit-build/scikit-build-core
..  _uv: https://docs.astral.sh/uv/
