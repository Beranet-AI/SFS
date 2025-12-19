from collections import defaultdict
from monitoring.domain.livestatus import LiveStatus

class LiveStatusStore:
    """
    In-memory store.
    Replace with Redis in production.
    """

    def __init__(self):
        self._store = defaultdict(list)

    def set(self, status: LiveStatus):
        self._store[str(status.livestock_id)].append(status)

    def get_by_livestock(self, livestock_id):
        return self._store.get(str(livestock_id), [])
