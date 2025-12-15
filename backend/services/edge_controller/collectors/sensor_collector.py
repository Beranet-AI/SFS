from adapters.labview import fetch_labview_data
from buffer.local_queue import enqueue

def collect():
    data = fetch_labview_data("http://labview:8000/sensors")

    for reading in data:
        enqueue(reading)
