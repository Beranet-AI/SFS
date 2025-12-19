from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.infrastructure.repositories.user_repo_impl import DjangoUserRepository
from apps.users.application.use_cases.create_user import CreateUserUseCase

class UsersView(APIView):
    repo = DjangoUserRepository()

    def get(self, request):
        return Response({"detail": "users endpoint"})

    def post(self, request):
        uc = CreateUserUseCase(self.repo)
        created = uc.execute(id="tmp", email=request.data["email"], role=request.data["role"])
        return Response({"id": created.id, "email": created.email, "role": created.role.value, "is_active": created.is_active})
