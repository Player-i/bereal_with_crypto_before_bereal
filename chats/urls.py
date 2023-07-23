# chats/urls.py
from django.urls import path

from . import views

app_name = "chats"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("room/", views.room, name="room"),
]
