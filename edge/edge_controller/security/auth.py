EDGE_TOKEN = "edge-secret"

def headers():
    return {"Authorization": f"Bearer {EDGE_TOKEN}"}
