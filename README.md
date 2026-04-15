# TUI Monitor Template

A reusable terminal dashboard template built with Python and Rich.

This project is designed as a structured foundation for building professional TUI (Text User Interface) monitoring dashboards with clean architecture, modular UI composition, and incremental development.

---

## Overview

This repository is not just a single-purpose dashboard demo.  
It is a **template-oriented TUI project** built to support:

- reusable layout patterns
- page-based dashboard composition
- sidebar navigation
- modular renderable components
- fake or real data-provider integration
- future extension into richer monitoring views

The current implementation focuses on a cluster-monitoring demo with navigation-ready architecture.

---

## Current Features

### Dashboard Shell
- dynamic header with current time
- dynamic footer with uptime
- left navigation sidebar
- right content area with page-based rendering

### Navigation
- numeric view switching using keyboard shortcuts
- active sidebar item highlighting
- non-blocking terminal input
- clean terminal restoration after exit

### Nodes View
- cluster summary panel
- structured node grid
- configurable grid presets:
  - `2x2`
  - `3x2`
  - `3x3`
- node panels with:
  - CPU
  - memory
  - disk
  - pod count
  - latency
- custom expandable metric bars
- color-coded severity styling
- empty placeholder panels for unused grid cells

### Page Routing
- `Prometheus` page placeholder
- `Nodes` page
- `Cluster` page placeholder
- `Gateway` page placeholder
- `Application` page placeholder

### Data Layer
- fake cluster-state provider
- fake node capacities
- fake health/alert generation
- UI-friendly summary shaping

---

## Architecture

The dashboard lifecycle is intentionally structured as:

```text
build() → initialize() → run() → shutdown()
````

### Responsibility Map

#### `main.py`

Application entry point only.

#### `dashboard.py`

Application orchestration and lifecycle management:

* runtime context creation
* frame updates
* keyboard input wiring
* navigation state mutation
* page rendering coordination

#### `ui/layout.py`

Top-level shell layout:

* header
* sidebar
* content
* footer

#### `ui/sidebar.py`

Navigation sidebar rendering:

* menu items
* active item highlighting

#### `ui/pages.py`

Content-page routing:

* select which page to render for the active view

#### `ui/nodes_page.py`

Full nodes page composition:

* summary
* node grid
* alerts section

#### `ui/components.py`

Reusable high-level UI components:

* cluster summary
* alerts placeholder

#### `ui/node_panel.py`

Node-level renderables:

* custom metric bars
* metric rows
* info rows
* node panels

#### `data/fake_cluster.py`

Fake data provider:

* cluster state
* node data
* alerts
* summary values

#### `terminal_input.py`

Low-level non-blocking terminal key reader.

#### `config.py`

Static configuration values such as grid preset.

---

## Project Structure

```text
.
├── main.py
├── dashboard.py
├── terminal_input.py
├── config.py
├── data/
│   └── fake_cluster.py
└── ui/
    ├── layout.py
    ├── sidebar.py
    ├── pages.py
    ├── nodes_page.py
    ├── components.py
    └── node_panel.py
```

---

## Supported Views

The current navigation menu contains:

* `1` → Prometheus
* `2` → Nodes
* `3` → Cluster
* `4` → Gateway
* `5` → Application

At the moment, only the **Nodes** view is fully implemented.
The remaining views are intentionally placeholders so the navigation and page-routing architecture can be exercised before their detailed content is built.

---

## Grid Presets

The Nodes page supports fixed grid presets:

* `2x2`
* `3x2`
* `3x3`

The active preset is selected in `config.py`.

Unused grid cells are automatically filled with placeholder panels.

---

## Controls

### Keyboard

* `1` to `5` → switch between pages
* `Ctrl+C` → exit cleanly

---

## Run

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## Current Status

This project currently provides a **navigation-capable TUI dashboard template** with a working Nodes page and placeholder pages for future expansion.

What is already solid:

* lifecycle architecture
* sidebar navigation
* page routing
* non-blocking terminal input
* modular UI separation
* reusable node grid rendering
* fake data integration

What is still intentionally incomplete:

* real Prometheus integration
* real Cluster page
* real Gateway page
* real Application page
* real alerts implementation
* richer status/help feedback in footer

---

## Why This Project Exists

This repository is meant to be useful for:

* learning Rich-based TUI architecture
* experimenting with dashboard layouts
* building cluster-monitoring demos
* using as a starter template for future terminal dashboards
* practicing professional refactoring and responsibility separation

---

## Next Possible Directions

Planned or possible future work includes:

* real Prometheus/service status page
* real cluster overview page
* richer alerts implementation
* footer help/status feedback
* page-specific data providers
* theme system
* improved keyboard navigation patterns
* portfolio/demo polish

---

## Versioning

The project is being developed incrementally through milestone-style versions.

Example milestone progression:

* `v0.1.0` – Base TUI foundation
* `v0.2.0` – Structured monitor UI
* `v0.3.0` – Cluster-oriented demo design
* `v0.4.0` – Sidebar navigation and page-based dashboard architecture
