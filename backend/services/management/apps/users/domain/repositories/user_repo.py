from abc import ABC, abstractmethod
from apps.users.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> User: ...
    @abstractmethod
    def create(self, user: User) -> User: ...
