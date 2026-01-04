from django.urls import path

from apps.users.api.views.create_user_view import CreateUserView
from apps.users.api.views.delete_user_view import DeleteUserView
from apps.users.api.views.update_user_view import UpdateUserView

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="users-create"),
    path("<str:user_id>/update/", UpdateUserView.as_view(), name="users-update"),
    path("<str:user_id>/delete/", DeleteUserView.as_view(), name="users-delete"),
]
