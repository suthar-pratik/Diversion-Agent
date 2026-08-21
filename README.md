# Running the Diversion Agent project on your local system

This guide walks you through cloning the repo, creating a Python virtual environment, installing dependencies, and starting the FastAPI app locally.

---

## 1. Prerequisites

- **Python 3.10 or higher** (the project was built against 3.14). Verify with:
  ```bash
  python --version
  ```
- **Git** to clone the repository.
- A terminal of your choice:
  - Windows: PowerShell or Command Prompt
  - macOS / Linux: Bash / Zsh

---

## 2. Clone the repository

```bash
git clone <your-repo-url>
cd "Diversion-Agent"
```

On Windows PowerShell, use quotes around the folder name because it contains spaces:
```powershell
cd "C:\Users\2159867\Desktop\AI project\Diversion-Agent"
```

---

## 3. Create and activate a virtual environment

The project ships with a `requirement.txt` file listing the runtime dependencies.

### Windows (PowerShell)
```powershell
python -m venv diversion-agent
.\diversion-agent\Scripts\Activate.ps1
```

If PowerShell blocks the activate script, run this once and try again:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (Command Prompt)
```cmd
python -m venv diversion-agent
diversion-agent\Scripts\activate.bat
```

### macOS / Linux
```bash
python3 -m venv diversion-agent
source diversion-agent/bin/activate
```

A successful activation prefixes your shell prompt with `(diversion-agent)`.

---

## 4. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirement.txt
```

> **Note:** The repository file is named `requirement.txt` (singular). If you prefer the conventional name, you can rename or copy it to `requirements.txt` — `pip install -r <file>` accepts any filename.

---

## 5. Run the FastAPI app

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reload on code changes (disable in production).

---

## 6. Verify the service is up

Open any of these URLs in a browser:

| URL                          | Purpose                          |
| ---------------------------- | -------------------------------- |
| http://127.0.0.1:8000/        | Root endpoint                    |
| http://127.0.0.1:8000/health  | Health check                     |
| http://127.0.0.1:8000/docs    | Interactive Swagger UI           |
| http://127.0.0.1:8000/redoc   | ReDoc API reference              |

You should see JSON like `{"status":"ok"}` from `/health` if everything is wired correctly.

---

## 7. Stopping the server

Press `Ctrl + C` in the terminal where Uvicorn is running. To deactivate the virtual environment, run:

```bash
deactivate
```

---

## Troubleshooting

- **`python` not found** — Install Python 3.10+ from python.org and ensure it's added to your PATH.
- **`uvicorn: command not found`** — Make sure the virtual environment is activated (the prompt should start with `(diversion-agent)`).
- **Port 8000 already in use** — Run on another port:
  ```bash
  uvicorn app.main:app --reload --port 8001
  ```
- **Pydantic validation errors** — Confirm `email-validator` is installed (required for `EmailStr` fields).

---

Happy hacking! 🚀
