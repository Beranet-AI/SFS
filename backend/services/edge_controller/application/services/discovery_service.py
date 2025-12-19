from datetime import datetime
from edge_controller.domain.edge_node import EdgeNode

class DiscoveryService:
    def __init__(self, registry):
        self.registry = registry

    def heartbeat(self, node_id: str, name: str, ip: str):
        node = EdgeNode(
            node_id=node_id,
            name=name,
            ip=ip,
            last_seen=datetime.utcnow(),
            is_online=True,
        )
        self.registry.upsert(node)
        return node

    def report_discovery(self, event):
        self.registry.record_discovery(event)
        return {"ok": True, "node_id": event.node_id, "count": len(event.discovered_devices)}
