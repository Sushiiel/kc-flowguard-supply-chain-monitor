import time
import random
from collections import deque

class Engine:
    def __init__(self):
        self.window_size = 50
        self.history = deque(maxlen=self.window_size)
        self.viscosity_series = deque(maxlen=20)
        self.proc_times = deque(maxlen=10)

    def generate_event(self) -> dict:
        return {
            "ts": time.time(),
            "sensor_id": "line-04",
            "viscosity": 40 + random.uniform(-5, 5) + (10 if random.random() > 0.95 else 0)
        }

    def process(self, event: dict) -> dict:
        start = time.perf_counter()
        val = event.get("viscosity", 40)
        self.history.append(val)
        self.viscosity_series.append(val)
        
        avg = sum(self.history) / len(self.history)
        diff = abs(val - avg)
        severity = "ok"
        if diff > 8: severity = "critical"
        elif diff > 4: severity = "warn"
        
        self.proc_times.append((time.perf_counter() - start) * 1000)
        return {"severity": severity, "summary": f"Viscosity {val:.2f} detected at {severity} level", **event}

    def kpis(self) -> dict:
        return {
            "throughput_rate": len(self.history),
            "anomaly_score": 98 if len(self.history) > 0 else 100,
            "avg_latency_ms": sum(self.proc_times) / len(self.proc_times) if self.proc_times else 0
        }

    def snapshot(self) -> dict:
        return {"recent": list(self.history)[-5:], "series": {"viscosity_series": list(self.viscosity_series)}}

engine = Engine()