# TUI Monitor Template

A structured and incremental template for building a system monitor TUI using Python and Rich.

---

## Development Philosophy

This project follows a progressive architecture approach:

1. Start simple inside `main.py`
2. Extract logic into functions
3. Separate concerns (data / ui / orchestration)
4. Introduce lifecycle structure
5. Add features incrementally
6. Apply OOP only when complexity requires it

Small commits. Clean separation. Versioned milestones.

---

## Architecture

```
tui-monitor-template/
├── main.py
├── dashboard.py
├── data/
│   ├── fake_provider.py
│   └── fake_metrics.py
└── ui/
├── components.py
└── layout.py
```

### Lifecycle

```
build() → initialize() → run() → shutdown()
````

---

## Features (v0.2)

- Structured layout (header / body / footer)
- Two-column body layout (left:2 / right:1)
- Fake system metrics (CPU / RAM / Disk)
- Fake service status provider
- Color-coded service states
- Dynamic header (current time)
- Dynamic footer (uptime)
- Graceful shutdown
- Full screen rendering without flicker

---

## Tech Stack

- Python 3.10+
- Rich

---

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
````

---

## Versioning Strategy

* `main` → stable releases
* `development` → active work
* Milestones are tagged (v0.x.0)

