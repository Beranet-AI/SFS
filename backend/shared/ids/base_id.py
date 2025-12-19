class BaseId(str):
    """
    Base class for all strongly-typed IDs.
    Prevents mixing IDs across domains.
    """

    def __new__(cls, value: str):
        if not value:
            raise ValueError("ID value cannot be empty")
        return str.__new__(cls, value)
