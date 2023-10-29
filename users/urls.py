from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path(
        "login/", views.CustomLogin.as_view(next_page="posts:post-list"), name="login"
    ),
    path("logout/", views.CustomLogout.as_view(next_page="posts:home"), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("user-profile/<int:pk>", views.UserProfile.as_view(), name="user-profile"),
    path(
        "update-profile/<int:pk>/", views.UpdateProfile.as_view(), name="update-profile"
    ),
    path(
        "delete-account/<int:pk>/", views.DeleteProfile.as_view(), name="delete-account"
    ),
]
