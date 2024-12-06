from django.urls import path

from account.views import (ActivateUser, Disable2fa, PasswordResetView,
                           UserLoginView, UserLogoutView, UserRegistrationView,
                           VerifyMfa, profile)

app_name: str = "account"

urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("verify-mfa/", VerifyMfa.as_view(), name="verify_mfa"),
    path("disable-2fa/", Disable2fa.as_view(), name="disable_2fa"),
    path("activate/<str:uuid64>/<str:token>/", ActivateUser.as_view(), name="activate_user"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
]
