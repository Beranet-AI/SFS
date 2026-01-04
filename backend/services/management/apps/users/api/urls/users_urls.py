from django.urls import path

from apps.users.api.views.create_user_view import UsersView

urlpatterns = [
    path("", UsersView.as_view()),
]
