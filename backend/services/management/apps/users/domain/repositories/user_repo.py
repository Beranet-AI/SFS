from abc import ABC, abstractmethod

from apps.users.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> User | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def create(self, user: User, password: str) -> User: ...

    @abstractmethod
    def update(self, user_id: str, **fields) -> User: ...

    @abstractmethod
    def deactivate(self, user_id: str) -> User: ...

    @abstractmethod
    def delete(self, user_id: str) -> bool: ...
