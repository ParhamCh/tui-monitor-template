# TUI Monitor Template

A terminal-based cluster monitoring demo built with Python and Rich.

This project is designed as a structured learning and development template for building a professional TUI (Text User Interface) monitoring dashboard step by step.

---

## Current Status

This project currently provides a **demo cluster-monitoring dashboard** with:

- Configurable node grid presets:
  - `2x2`
  - `3x2`
  - `3x3`
- Dynamic header with current time
- Dynamic footer with uptime
- Cluster summary panel
- Node panels with:
  - CPU usage
  - Memory usage
  - Disk usage
  - Pod count
  - Latency
- Custom expandable block bars for metrics
- Color-coded metric severity
- Placeholder alerts panel
- Fake cluster-state provider for UI/demo development

---

## Development Philosophy

This project follows an incremental engineering workflow:

1. Start simple
2. Build features directly
3. Extract functions
4. Separate modules
5. Refactor for structure and clarity
6. Introduce stronger abstractions only when needed

The goal is not just to build a UI, but to build it in a clean, maintainable, and reviewable way.

---

## Project Structure

```text
.
├── main.py
├── dashboard.py
├── config.py
├── data/
│   └── fake_cluster.py
└── ui/
    ├── components.py
    ├── layout.py
    └── node_panel.py
````

---

## Architecture

The dashboard lifecycle is intentionally structured as:

```text
build() → initialize() → run() → shutdown()
```

### Responsibilities

* `dashboard.py`

  * lifecycle orchestration
  * runtime context
  * frame updates

* `data/fake_cluster.py`

  * fake cluster-state generation
  * fake node metrics
  * fake alerts and summary data

* `ui/layout.py`

  * dashboard layout
  * configurable grid presets

* `ui/node_panel.py`

  * node renderables
  * custom block bars
  * metric rows and panel styling

* `ui/components.py`

  * cluster summary
  * alerts placeholder
  * small UI helper components

---

## Grid Presets

The node area supports fixed layout presets:

* `2x2`
* `3x2`
* `3x3`

The active preset is selected in `config.py`.

Empty cells are automatically filled with placeholder panels when the number of nodes is lower than grid capacity.

---

## Run

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the dashboard:

```bash
python main.py
```

Exit cleanly with:

```text
Ctrl+C
```

---

## Notes

* This is currently a **demo / fake-data implementation**
* The alerts panel is intentionally a placeholder for now
* The project focuses on architecture, layout design, and incremental refinement before connecting to real metrics

---

## Next Possible Steps

Some possible future directions:

* real cluster metrics integration
* real alerts implementation
* service health monitoring
* richer summary panel
* theme system
* final UI polish for demo/portfolio use

---

## Versioning

This project is being developed incrementally with tagged milestones.

Example milestones:

* `v0.1.0` – Base TUI foundation
* `v0.2.0` – Structured monitor UI
* `v0.3.0` – Cluster-oriented demo design
