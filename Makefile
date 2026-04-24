.PHONY: docs

all: stubgen format docs

docs:
	uv run make -C docs/ clean html

format:
	uv run ruff check --select I,RUF022 --fix docs/ src/ tests/
	uv run ruff format docs/ src/ tests/

lint:
	uv run ruff check docs/ src/ tests/

pre-commit-autoupdate:
	uv run pre-commit autoupdate --repo https://github.com/astral-sh/ruff-pre-commit
	uv run pre-commit autoupdate --repo https://github.com/astral-sh/uv-pre-commit
	uv run pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks

pre-commit-install:
	uv run pre-commit install

stubgen:
	 uv run python -m nanobind.stubgen --module supriya_midi.rtmidi_ext --marker-file src/supriya_midi/py.typed --output-dir src/supriya_midi

ty:
	uv run ty check src/ tests/
