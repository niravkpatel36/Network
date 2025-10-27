from django.urls import path
from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # pages
    path("all", views.index, name="all_posts"),
    path("following", views.following_posts, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),

    # API endpoints
    path("post", views.create_post, name="create_post"),
    path("post/<int:post_id>", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/like", views.toggle_like, name="toggle_like"),
    path("profile/<str:username>/follow", views.toggle_follow, name="toggle_follow"),
]