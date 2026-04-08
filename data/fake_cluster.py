"""
data/fake_cluster.py
====================
Fake cluster-state provider for the TUI cluster-monitoring demo.

This module generates a synthetic cluster state suitable for UI development,
layout testing, and demo rendering. It is intentionally non-deterministic and
does not attempt to model real cluster behavior with high fidelity.

The returned cluster state has three top-level sections:
    - summary
    - nodes
    - alerts
"""

import random


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Node readiness probabilities by role.
MASTER_READY_WEIGHTS: tuple[float, float] = (0.95, 0.05)
WORKER_READY_WEIGHTS: tuple[float, float] = (0.90, 0.10)

#: Random utilization ranges for fake metrics.
MIN_UTILIZATION: int = 5
MAX_UTILIZATION: int = 95

#: Fake pod count generation limits.
MIN_PODS: int = 5
MAX_DEMO_PODS: int = 25

#: Fake latency generation range (ms).
MIN_LATENCY_MS: int = 1
MAX_LATENCY_MS: int = 18

#: Fake uptime range (seconds).
MIN_UPTIME_SEC: int = 1000
MAX_UPTIME_SEC: int = 20000

#: Alert thresholds.
WARN_CPU_THRESHOLD: int = 85
CRIT_CPU_THRESHOLD: int = 95

WARN_MEM_THRESHOLD: int = 85
CRIT_MEM_THRESHOLD: int = 95

WARN_DISK_THRESHOLD: int = 90
WARN_LATENCY_THRESHOLD: int = 15


#: Role-based capacity presets.
ROLE_CAPACITY = {
    "master": {
        "cpu_cores": 4,
        "mem_gb": 16,
        "disk_gb": 200,
        "pods_capacity": 110,
    },
    "worker": {
        "cpu_cores": 8,
        "mem_gb": 32,
        "disk_gb": 500,
        "pods_capacity": 220,
    },
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _status_for(role: str) -> str:
    """Return a fake readiness status based on node role."""
    weights = MASTER_READY_WEIGHTS if role == "master" else WORKER_READY_WEIGHTS
    return random.choices(["Ready", "NotReady"], weights=weights, k=1)[0]


def _make_alerts(nodes: list[dict]) -> list[dict]:
    """Generate alert objects from node-state dictionaries."""
    alerts: list[dict] = []

    for node in nodes:
        if node["status"] != "Ready":
            alerts.append(
                {
                    "node": node["name"],
                    "severity": "CRIT",
                    "message": "Node NotReady",
                }
            )

        if node["cpu"] >= WARN_CPU_THRESHOLD:
            severity = "CRIT" if node["cpu"] >= CRIT_CPU_THRESHOLD else "WARN"
            alerts.append(
                {
                    "node": node["name"],
                    "severity": severity,
                    "message": f"High CPU ({node['cpu']}%)",
                }
            )

        if node["memory"] >= WARN_MEM_THRESHOLD:
            severity = "CRIT" if node["memory"] >= CRIT_MEM_THRESHOLD else "WARN"
            alerts.append(
                {
                    "node": node["name"],
                    "severity": severity,
                    "message": f"High MEM ({node['memory']}%)",
                }
            )

        if node["disk"] >= WARN_DISK_THRESHOLD:
            alerts.append(
                {
                    "node": node["name"],
                    "severity": "WARN",
                    "message": f"High Disk ({node['disk']}%)",
                }
            )

        if node["latency_ms"] >= WARN_LATENCY_THRESHOLD:
            alerts.append(
                {
                    "node": node["name"],
                    "severity": "WARN",
                    "message": f"High Latency ({node['latency_ms']}ms)",
                }
            )

    return alerts


def _derive_cluster_health(alerts: list[dict]) -> str:
    """Derive overall cluster health from alert severities."""
    crit_count = sum(1 for alert in alerts if alert["severity"] == "CRIT")
    warn_count = sum(1 for alert in alerts if alert["severity"] == "WARN")

    if crit_count > 0:
        return "CRITICAL"
    if warn_count > 0:
        return "DEGRADED"
    return "HEALTHY"


# ---------------------------------------------------------------------------
# Public builders
# ---------------------------------------------------------------------------


def generate_node(name: str, role: str) -> dict:
    """Generate one fake node-state dictionary."""
    capacity = ROLE_CAPACITY[role]

    return {
        "name": name,
        "role": role,
        "status": _status_for(role),
        "cpu": random.randint(MIN_UTILIZATION, MAX_UTILIZATION),
        "memory": random.randint(MIN_UTILIZATION, MAX_UTILIZATION),
        "disk": random.randint(MIN_UTILIZATION, MAX_UTILIZATION),
        "pods": random.randint(MIN_PODS, min(MAX_DEMO_PODS, capacity["pods_capacity"])),
        "latency_ms": random.randint(MIN_LATENCY_MS, MAX_LATENCY_MS),
        "uptime": random.randint(MIN_UPTIME_SEC, MAX_UPTIME_SEC),
        "cpu_cores": capacity["cpu_cores"],
        "mem_gb": capacity["mem_gb"],
        "disk_gb": capacity["disk_gb"],
        "pods_capacity": capacity["pods_capacity"],
    }


def get_cluster_state() -> dict:
    """Generate a full fake cluster state for the dashboard."""
    nodes = [
        generate_node("master-1", "master"),
        generate_node("worker-1", "worker"),
        generate_node("worker-2", "worker"),
        generate_node("worker-3", "worker"),
    ]

    total_nodes = len(nodes)
    ready_nodes = sum(1 for node in nodes if node["status"] == "Ready")
    notready_names = [node["name"] for node in nodes if node["status"] != "Ready"]

    avg_cpu = sum(node["cpu"] for node in nodes) // total_nodes
    avg_memory = sum(node["memory"] for node in nodes) // total_nodes

    max_cpu_node = max(nodes, key=lambda node: node["cpu"])
    max_mem_node = max(nodes, key=lambda node: node["memory"])

    total_pods = sum(node["pods"] for node in nodes)

    total_cores = sum(node["cpu_cores"] for node in nodes)
    used_cores = round(
        sum((node["cpu"] / 100) * node["cpu_cores"] for node in nodes),
        1,
    )

    total_mem_gb = sum(node["mem_gb"] for node in nodes)
    used_mem_gb = round(
        sum((node["memory"] / 100) * node["mem_gb"] for node in nodes),
        1,
    )

    total_pods_capacity = sum(node["pods_capacity"] for node in nodes)

    alerts = _make_alerts(nodes)
    warn_count = sum(1 for alert in alerts if alert["severity"] == "WARN")
    crit_count = sum(1 for alert in alerts if alert["severity"] == "CRIT")

    summary = {
        "total_nodes": total_nodes,
        "ready_nodes": ready_nodes,
        "avg_cpu": avg_cpu,
        "avg_memory": avg_memory,
        "total_pods": total_pods,
        "notready_names": notready_names,
        "health": _derive_cluster_health(alerts),
        "max_cpu": max_cpu_node["cpu"],
        "max_cpu_node": max_cpu_node["name"],
        "max_memory": max_mem_node["memory"],
        "max_memory_node": max_mem_node["name"],
        "used_cores": used_cores,
        "total_cores": total_cores,
        "used_mem_gb": used_mem_gb,
        "total_mem_gb": total_mem_gb,
        "pods_capacity": total_pods_capacity,
        "alerts_total": len(alerts),
        "alerts_warn": warn_count,
        "alerts_crit": crit_count,
    }

    return {
        "summary": summary,
        "nodes": nodes,
        "alerts": alerts,
    }