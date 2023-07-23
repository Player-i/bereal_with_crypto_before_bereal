from django.contrib import admin
from django.urls import path
from django.urls import include
from accounts.views import home
from chats import views
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import (
    profile_view,
    like_view,
    quiz_score_view,
    user_enter_quiz,
    edit_profile_view,
    delete_post_view,
    quiz_view,
    post_comment,
    clear_view,
    submit_post_view,
    # search_bar,
    drop_box,
)

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", home, name="home"),
    path("", include("accounts.urls")),
    path("", include("chats.urls")),
    path("<str:username>/", profile_view, name="profile"),
    path("<str:username>/edit_profile/", edit_profile_view, name="edit_profile"),
    path("like", like_view, name="like"),
    path("post_comment", post_comment, name="post_comment"),
    path("quiz", quiz_view, name="quiz_view"),
    path("quiz_score", quiz_score_view, name="quiz_score"),
    path("user_enter_quiz", user_enter_quiz, name="user_enter_quiz"),
    path("<str:post_id>/delete/", delete_post_view, name="delete"),
    path("<str:post_id>/clear/", clear_view, name="clear"),
    path("submit_post", submit_post_view, name="submit_post"),
    # path("search_bar", search_bar, name="search_bar"),
    path("drop_box", drop_box, name="drop_box"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
