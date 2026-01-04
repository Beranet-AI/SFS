from django.contrib.auth import get_user_model
from django.db import transaction

from apps.users.domain.entities.user import User
from apps.users.domain.repositories.user_repo import UserRepository
from apps.users.infrastructure.mappers.users_mapper import to_domain, to_orm_data


class UsersRepositoryImpl(UserRepository):
    def __init__(self, user_model=None) -> None:
        self._user_model = user_model or get_user_model()

    def get_by_id(self, user_id: str) -> User | None:
        try:
            return to_domain(self._user_model.objects.get(id=user_id))
        except self._user_model.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> User | None:
        try:
            return to_domain(self._user_model.objects.get(email=email))
        except self._user_model.DoesNotExist:
            return None

    @transaction.atomic
    def create(self, user: User, password: str) -> User:
        user_model = self._user_model.objects.create_user(
            **to_orm_data(user),
            password=password,
        )
        return to_domain(user_model)

    @transaction.atomic
    def update(self, user_id: str, **fields) -> User:
        user_model = self._user_model.objects.get(id=user_id)
        if not fields:
            return to_domain(user_model)
        for field_name, value in fields.items():
            setattr(user_model, field_name, value)
            if field_name == "email":
                user_model.username = value
        user_model.save(update_fields=fields.keys())
        return to_domain(user_model)

    @transaction.atomic
    def deactivate(self, user_id: str) -> User:
        user_model = self._user_model.objects.get(id=user_id)
        user_model.is_active = False
        user_model.is_active_account = False
        user_model.save(update_fields=["is_active", "is_active_account"])
        return to_domain(user_model)

    @transaction.atomic
    def delete(self, user_id: str) -> bool:
        deleted_count, _ = self._user_model.objects.filter(id=user_id).delete()
        return deleted_count > 0
