from apps.users.domain.entities.user import User


def to_domain(user_model) -> User:
    raise NotImplementedError


def to_orm(user: User):
    raise NotImplementedError
