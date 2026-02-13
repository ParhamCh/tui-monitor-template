# TUI Monitor Template

A minimal and structured template for building a system monitor TUI using Python and Rich.

## Philosophy

This project follows an incremental development approach:

1. Start simple in `main.py`
2. Extract logic into functions
3. Move logic into dedicated modules
4. Introduce OOP when structure stabilizes

Small commits. Clean architecture. Progressive complexity.

---

## Tech Stack

- Python 3.10+
- Rich

---

## Setup

```bash
git clone <repo>
cd tui-monitor-template
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
````

---

## Branch Strategy

* `main` → stable
* `development` → active work

---

## Current Features

* Basic layout (header / body / footer)
* Live updating panel
* Graceful shutdown (Ctrl+C)
* Full screen mode with clean exit

---