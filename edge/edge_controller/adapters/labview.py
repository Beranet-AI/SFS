import requests

def fetch_labview_data(endpoint: str):
    res = requests.get(endpoint, timeout=3)
    res.raise_for_status()
    return res.json()
