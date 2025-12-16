import requests

def fetch_commands():
    return requests.get(
        "https://server/edge/commands",
        timeout=2
    ).json()
