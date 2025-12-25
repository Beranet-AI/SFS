from apps.users.domain.entities.user import User
from apps.users.models import UserModel
from apps.users.domain.enums.role import Role

class DjangoUserRepository:
    def get_by_id(self, user_id: str) -> User:
        obj = UserModel.objects.get(id=user_id)
        return User(id=str(obj.id), email=obj.email, role=Role(obj.role), is_active=obj.is_active)

    def create(self, user: User) -> User:
        obj = UserModel.objects.create(email=user.email, role=user.role.value, is_active=user.is_active)
        return User(id=str(obj.id), email=obj.email, role=Role(obj.role), is_active=obj.is_active)
