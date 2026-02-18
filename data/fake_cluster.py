import random
import time


def generate_node(name: str, role: str):
    return {
        "name": name,
        "role": role,
        "status": random.choice(["Ready", "NotReady"]),
        "cpu": random.randint(10, 95),
        "memory": random.randint(10, 95),
        "disk": random.randint(10, 95),
        "pods": random.randint(5, 25),
        "latency_ms": random.randint(1, 15),
        "uptime": random.randint(1000, 20000),
    }


def get_cluster_state():
    nodes = [
        generate_node("master", "master"),
        generate_node("worker-1", "worker"),
        generate_node("worker-2", "worker"),
        generate_node("worker-3", "worker"),
    ]

    summary = {
        "total_nodes": len(nodes),
        "ready_nodes": sum(1 for n in nodes if n["status"] == "Ready"),
        "avg_cpu": sum(n["cpu"] for n in nodes) // len(nodes),
        "avg_memory": sum(n["memory"] for n in nodes) // len(nodes),
        "total_pods": sum(n["pods"] for n in nodes),
    }

    alerts = [
        {
            "node": n["name"],
            "message": "High CPU",
        }
        for n in nodes
        if n["cpu"] > 85
    ]

    return {
        "summary": summary,
        "nodes": nodes,
        "alerts": alerts,
    }
