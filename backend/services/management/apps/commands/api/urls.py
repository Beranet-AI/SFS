from django.urls import include, path

urlpatterns = [
    path("", include("apps.commands.api.urls.commands_urls")),
]
