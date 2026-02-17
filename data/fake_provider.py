import random


def get_service_status():
    statuses = ["OK", "WARN", "DOWN"]

    return {
        "API": random.choice(statuses),
        "DB": random.choice(statuses),
        "Cache": random.choice(statuses),
    }

