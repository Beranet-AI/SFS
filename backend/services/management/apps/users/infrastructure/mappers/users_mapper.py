from apps.users.domain.entities.user import User
from apps.users.domain.value_objects.email import Email


def to_domain(user_model) -> User:
    return User(
        id=str(user_model.id),
        email=Email(user_model.email),
        phone_number=user_model.phone_number,
        is_staff=user_model.is_staff,
        is_superuser=user_model.is_superuser,
        is_active=user_model.is_active,
        is_active_account=user_model.is_active_account,
    )


def to_orm_data(user: User) -> dict:
    return {
        "email": user.email.value,
        "username": user.email.value,
        "phone_number": user.phone_number,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "is_active": user.is_active,
        "is_active_account": user.is_active_account,
    }
