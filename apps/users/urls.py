from django.urls import path
from .import views


urlpatterns = [
    path('create-users', views.RegisterUserView.as_view(), name="create_user"),
    path('user-profile', views.UserProfileView.as_view(), name="user_profile"),
    path('<str:id>/delete-user', views.DeleteUserView.as_view(), name="delete_profile"),
    path('user-login', views.UserLoginView.as_view(), name="user_login"),
    path('user-logout', views.UserLogoutView.as_view(), name="user_logout"),
    path('change-password', views.ChangePasswordView.as_view(), name="change_password")
]
