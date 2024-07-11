
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name = "newPost"),
    path("addPost", views.addPost, name="addPost"),
    path("profile/<str:userConected>", views.profile, name= "profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path('edit/<int:postId>',views.edit, name ='edit'),
    path('addLike/<int:post_id>',views.addLike, name ='addLike'),
    path('removeLike/<int:post_id>',views.removeLike, name ='removeLike'),



]
