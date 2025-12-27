from collections import defaultdict
from backend.services.edge_controller.domain.edge_node import EdgeNode

class EdgeRegistry:
    """
    In-memory registry.
    Replace with Redis/DB if needed.
    """
    def __init__(self):
        self.nodes: dict[str, EdgeNode] = {}
        self.discovery_events = defaultdict(list)

    def upsert(self, node: EdgeNode):
        self.nodes[node.node_id] = node

    def get(self, node_id: str):
        return self.nodes.get(node_id)

    def list(self):
        return list(self.nodes.values())

    def record_discovery(self, event):
        self.discovery_events[event.node_id].append(event)

    def list_discoveries(self, node_id: str):
        return self.discovery_events.get(node_id, [])
