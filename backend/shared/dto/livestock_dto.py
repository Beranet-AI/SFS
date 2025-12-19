from shared.ids.livestock_id import LivestockId
from shared.value_objects.livestock_location import LivestockLocation

class LivestockDTO:
    """
    Contract DTO for Livestock.
    Used across services and frontend.
    """

    def __init__(
        self,
        id: LivestockId,
        tag: str,
        location: LivestockLocation
    ):
        self.id = id
        self.tag = tag
        self.location = location
