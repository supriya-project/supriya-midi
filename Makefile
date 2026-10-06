.PHONY: docs

all: stubgen format docs

docs:
	uv run make -C docs/ clean html

format:
	uv run ruff check --select I,RUF022 --fix docs/ src/ tests/
	uv run ruff format docs/ src/ tests/

lint:
	uv run ruff check docs/ src/ tests/

pre-commit-install:
	uv run pre-commit install

stubgen:
	 uv run python -m nanobind.stubgen --module supriya_midi.rtmidi_ext --marker-file src/supriya_midi/py.typed --output-file src/supriya_midi/rtmidi_ext.pyi
	 uv run ruff format src/supriya_midi/rtmidi_ext.pyi
	 uv run ruff check --fix src/supriya_midi/rtmidi_ext.pyi

ty:
	uv run ty check src/ tests/
