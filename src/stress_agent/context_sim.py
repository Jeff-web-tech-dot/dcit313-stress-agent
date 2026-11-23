"""Made-up (simulated) student context. Always labelled as simulated."""
import random


def simulated_context(seed=None):
    rng = random.Random(seed)
    return {
        "simulated": True,
        "exam_week": rng.random() < 0.3,
        "minutes_free": rng.choice([2, 5, 10, 15, 30]),
    }
