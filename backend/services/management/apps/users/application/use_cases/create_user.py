from apps.users.domain.entities.user import User

class CreateUserUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, id: str, email: str, role, is_active: bool = True) -> User:
        user = User(id=id, email=email, role=role, is_active=is_active)
        return self.repo.create(user)
