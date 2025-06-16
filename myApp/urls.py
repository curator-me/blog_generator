from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("blog_generate/", views.generate_blog, name="generate_blog"),
    path("accounts/register/", views.register_user, name="register_user"),
    path("accounts/login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("blogs/<int:pk>/", views.saved_blog, name="saved_blog"),
    path("blogs/blog/<int:pk>/", views.show_blog, name="show_blog"),
    path("blogs/blog/delete/<int:pk>/", views.delete_blog, name="delete_blog"),
    path("user/accounts/change-password/", views.change_password, name="change_password"),
    path("user/profile/", views.profile, name="profile"),
    path("user/profile/edit/", views.edit_profile, name="edit_profile"),

    path("user/account/reset-password/", views.reset_password, name="reset_password"),
    path("user/account/reset-password/", views.new_password, name="new_password"),
]

