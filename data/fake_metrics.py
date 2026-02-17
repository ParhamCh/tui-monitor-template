import random


def get_metrics():
    """
    Return fake system metrics.
    """
    return {
        "CPU": random.randint(0, 100),
        "RAM": random.randint(0, 100),
        "Disk": random.randint(0, 100),
    }
