from rest_framework.generics import GenericAPIView


class BaseController(GenericAPIView):
    """Base controller for shared command API behavior."""

    def get_username(self, request) -> str:
        return str(getattr(request.user, "username", ""))

    @staticmethod
    def require_fields(payload: dict, fields: list[str]) -> None:
        missing = [field for field in fields if field not in payload]
        if missing:
            raise KeyError(", ".join(missing))
