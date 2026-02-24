# Blue Ocean Engine

Quick setup and commands for development, testing, linting, and Docker.

Getting started

- Create a virtual environment and install dependencies:

PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements-dev.txt
```

Test

```powershell
pytest -q
```

Lint & format checks

```powershell
black --check .
isort --check-only .
flake8 .
```

Build Docker image

```powershell
docker build -t blue-ocean-engine:latest .
```

Run (adjust module/entrypoint as needed)

```powershell
docker run --rm -it blue-ocean-engine:latest
```

CI

We include a GitHub Actions workflow at `.github/workflows/ci.yml` that runs the linters and tests on `ubuntu-latest`.

Notes

- If your runtime dependencies are in a `requirements.txt` separate from `requirements-dev.txt`, update the `Dockerfile` and CI workflow accordingly.
- Update the Docker `CMD` in `Dockerfile` to point to the correct module or script for starting the engine.
