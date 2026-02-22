import random


def _status_for(role: str) -> str:
    # Master a bit more stable (demo)
    weights = [0.95, 0.05] if role == "master" else [0.90, 0.10]
    return random.choices(["Ready", "NotReady"], weights=weights, k=1)[0]


def generate_node(name: str, role: str) -> dict:
    cpu_cores = 4 if role == "master" else 8
    mem_gb = 16 if role == "master" else 32
    disk_gb = 200 if role == "master" else 500
    pods_capacity = 110 if role == "master" else 220

    return {
        "name": name,
        "role": role,
        "status": _status_for(role),
        "cpu": random.randint(5, 95),
        "memory": random.randint(5, 95),
        "disk": random.randint(5, 95),
        "pods": random.randint(5, min(25, pods_capacity)),
        "latency_ms": random.randint(1, 18),
        "uptime": random.randint(1000, 20000),
        # capacities (for capacity view)
        "cpu_cores": cpu_cores,
        "mem_gb": mem_gb,
        "disk_gb": disk_gb,
        "pods_capacity": pods_capacity,
    }


def _make_alerts(nodes: list[dict]) -> list[dict]:
    alerts: list[dict] = []

    for n in nodes:
        if n["status"] != "Ready":
            alerts.append(
                {"node": n["name"], "severity": "CRIT", "message": "Node NotReady"}
            )

        if n["cpu"] >= 85:
            sev = "CRIT" if n["cpu"] >= 95 else "WARN"
            alerts.append(
                {"node": n["name"], "severity": sev, "message": f"High CPU ({n['cpu']}%)"}
            )

        if n["memory"] >= 85:
            sev = "CRIT" if n["memory"] >= 95 else "WARN"
            alerts.append(
                {
                    "node": n["name"],
                    "severity": sev,
                    "message": f"High MEM ({n['memory']}%)",
                }
            )

        if n["disk"] >= 90:
            alerts.append(
                {"node": n["name"], "severity": "WARN", "message": f"High Disk ({n['disk']}%)"}
            )

        if n["latency_ms"] >= 15:
            alerts.append(
                {
                    "node": n["name"],
                    "severity": "WARN",
                    "message": f"High Latency ({n['latency_ms']}ms)",
                }
            )

    return alerts


def get_cluster_state() -> dict:
    nodes = [
        generate_node("master-1", "master"),
        generate_node("worker-1", "worker"),
        generate_node("worker-2", "worker"),
        generate_node("worker-3", "worker"),
    ]

    total_nodes = len(nodes)
    ready_nodes = sum(1 for n in nodes if n["status"] == "Ready")
    notready_names = [n["name"] for n in nodes if n["status"] != "Ready"]

    avg_cpu = sum(n["cpu"] for n in nodes) // total_nodes
    avg_memory = sum(n["memory"] for n in nodes) // total_nodes

    max_cpu_node = max(nodes, key=lambda n: n["cpu"])
    max_mem_node = max(nodes, key=lambda n: n["memory"])

    total_pods = sum(n["pods"] for n in nodes)

    # capacity view (approximate)
    total_cores = sum(n["cpu_cores"] for n in nodes)
    used_cores = round(sum((n["cpu"] / 100) * n["cpu_cores"] for n in nodes), 1)

    total_mem_gb = sum(n["mem_gb"] for n in nodes)
    used_mem_gb = round(sum((n["memory"] / 100) * n["mem_gb"] for n in nodes), 1)

    total_pods_capacity = sum(n["pods_capacity"] for n in nodes)

    alerts = _make_alerts(nodes)
    warn_count = sum(1 for a in alerts if a["severity"] == "WARN")
    crit_count = sum(1 for a in alerts if a["severity"] == "CRIT")

    # cluster health
    if crit_count > 0:
        health = "CRITICAL"
    elif warn_count > 0:
        health = "DEGRADED"
    else:
        health = "HEALTHY"

    summary = {
        # existing keys (keep compatibility)
        "total_nodes": total_nodes,
        "ready_nodes": ready_nodes,
        "avg_cpu": avg_cpu,
        "avg_memory": avg_memory,
        "total_pods": total_pods,
        # new keys
        "notready_names": notready_names,
        "health": health,
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

    return {"summary": summary, "nodes": nodes, "alerts": alerts}