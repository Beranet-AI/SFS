from collectors.sensor_collector import collect
from buffer.local_queue import dequeue
import requests
import time

INGEST_URL = "https://server/data_ingestion/telemetry"

while True:
    collect()

    item = dequeue()
    if item:
        try:
            requests.post(INGEST_URL, json=item, timeout=2)
        except Exception:
            # دوباره برگرد توی صف
            pass

    time.sleep(1)
