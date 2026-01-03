from typing import Any, Dict, Type

from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError


class BaseController:
    """Shared controller utilities for data_ingestion presentation layer."""

    @staticmethod
    def validate_payload(
        payload: Dict[str, Any], schema: Type[BaseModel]
    ) -> BaseModel:
        try:
            return schema.parse_obj(payload)
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=exc.errors(),
            )

    @staticmethod
    def response_ok(extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
        response: Dict[str, Any] = {"ok": True}
        if extra:
            response.update(extra)
        return response

    @staticmethod
    def response_error(details: Any) -> Dict[str, Any]:
        return {"ok": False, "details": details}
