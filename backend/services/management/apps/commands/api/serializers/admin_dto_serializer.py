class AdminDTOSerializer:
    @staticmethod
    def to_dict(obj) -> dict:
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return dict(obj)
