from monitoring.infrastructure.cache.livestatus_store import LiveStatusStore
from monitoring.domain.livestatus import LiveStatus

class LiveStatusService:
    """
    Orchestrates read/write of live status snapshots.
    """

    def __init__(self, store: LiveStatusStore):
        self.store = store

    def update(self, status: LiveStatus):
        self.store.set(status)

    def get_by_livestock(self, livestock_id):
        return self.store.get_by_livestock(livestock_id)
