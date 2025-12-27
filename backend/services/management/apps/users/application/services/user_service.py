from apps.users.models import UserModel


class CreateUserService:
    """
    Application service for creating users.
    """

    def create_user(
        self,
        *,
        email: str,
        password: str,
        phone_number: str = "",
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> UserModel:

        user = UserModel.objects.create_user(
            email=email,
            password=password,
            username=email,  # الزام Django
            phone_number=phone_number,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            is_active_account=True,
        )
        return user
