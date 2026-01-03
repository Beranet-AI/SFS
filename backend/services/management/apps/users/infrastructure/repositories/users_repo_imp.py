from apps.users.domain.entities.user import User
from apps.users.domain.repositories.user_repo import UserRepository


class UsersRepositoryImpl(UserRepository):
    def get_by_id(self, user_id: str) -> User:
        raise NotImplementedError

    def create(self, user: User) -> User:
        raise NotImplementedError
