# Leightner internal tools

This project is the early scaffold for an internal web application for Leightner Electronics Inc. It is intended to become a simple, on-premise tool for managing orders, issue tracking, and basic operator access without introducing cloud services, build tooling, or unnecessary complexity.

## Requirements

Use Python 3.10 or newer. The current project rules require Python 3.10+.

## Set up a virtual environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app locally

Start the development server:

```bash
uvicorn backend.main:app --reload --port 8000
```

The health check endpoint will be available at `http://localhost:8000/health`.

## Run tests

Automated tests have not been added yet.

