from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    path("register/", views.registration_view, name="register"),
    path("leaderboard/", views.leaderboard_view, name="leaderboard"),
    path("<str:username>/follow/", views.follow_view, name="follow"),
]
