## Local Development Setup (macOS)

Follow these steps to get a working local environment for testing.

### 1) Install Python 3.13

- Recommended (pyenv):
  - Install prerequisites: `brew install readline xz zlib openssl bzip2`
  - Install pyenv: `brew install pyenv`
  - Add to shell (if not already): `echo 'eval "$(pyenv init -)"' >> ~/.zshrc && exec zsh`
  - Install Python: `pyenv install 3.13.0`
  - Set local version in this repo: `pyenv local 3.13.0`

- Alternatively (Homebrew):
  - `brew install python@3.13`
  - Ensure `python3 --version` shows 3.13.x

### 2) Install Poetry (dependency manager)

- `curl -sSL https://install.python-poetry.org | python3 -`
- Ensure Poetry is on PATH (restart terminal if needed): `poetry --version`

### 3) Install dependencies

- From the project root:
  - `poetry install`

This creates an isolated virtual environment tied to this project and installs dependencies from `pyproject.toml`.

### 4) Environment variables

- Copy the example env file and set your values:
  - `cp .env.example .env`
  - Set `VSAC_API_KEY` in `.env`.

You can either export variables in your shell or load them with tools like `direnv`. If you export manually for a session:

```bash
export VSAC_API_KEY="<your_key_here>"
```

### 5) Using the environment

- One-off command: `poetry run python -c "import fhir.resources; print('FHIR resources OK')"`
- Interactive shell: `poetry shell` (then run Python or scripts directly)

### 6) Optional: Docker

`docker-compose.yml` exists but is currently empty. If/when services are added, you can start them with:

```bash
docker compose up --build
```

### 7) Repo layout

- Data samples: `data/synthea_sample_data_fhir_latest/`
- Services (WIP): `services/`
- Project config: `pyproject.toml`

### 8) Quick smoke test

Run this to verify the environment resolves dependencies:

```bash
poetry run python - <<'PY'
import os
import importlib

print('Python OK')
assert importlib.import_module('fhir.resources')
print('fhir.resources OK')
print('VSAC_API_KEY set:', bool(os.getenv('VSAC_API_KEY')))
PY
```

If the last line prints `False`, set `VSAC_API_KEY` per step 4 before testing services that require it.


