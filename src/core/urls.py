from django.contrib.auth import views as auth_views
from django.urls import path
from .views import home_view, register


urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(next_page="/login/", template_name="login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
]
