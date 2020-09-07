
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API Routes
    path("create", views.create_post, name="create"),
    path("modify", views.modify_post, name="modify"),
    path("posts/<str:post_type>/<int:get_page_no>", views.get_posts, name="get_posts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("profile/<int:user_pk>", views.profile, name="profile")
]
