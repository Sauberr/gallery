import base64
import io

import pyotp
import qrcode
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, UpdateView, View

from account.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from account.services.verify_2fa_otp import verify_2fa_otp
from account.tasks import send_registration_email
from common.mixins import TitleMixin
from core.utils.token_generator import TokenGenerator


class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    """Handle user authentication with remember me and 2FA support"""

    template_name: str = "registration/login.html"
    title: str = "Login"
    model = get_user_model()
    form_class = UserLoginForm
    success_message: str = "You are successfully logged in"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        """Process valid login form and handle remember me and 2FA verification"""

        remember_me = form.cleaned_data["remember_me"]
        if remember_me:
            self.request.session.set_expiry(2592000)
        else:
            self.request.session.set_expiry(0)

        self.request.session.modified = True

        user = form.get_user()
        if user is not None:
            if user.mfa_enabled:
                return render(
                    self.request,
                    "registration/2FA/otp_verify.html",
                    {"user_id": user.id},
                )
            login(self.request, user)
            messages.success(self.request, "Login successful!")
            return redirect("account:profile")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle invalid login form submission and display error message"""
        messages.error(self.request, "Please, write valid email or password")
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """Handle user logout and session termination"""
    pass


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    """Handle new user registration with email verification"""

    template_name: str = "registration/registration.html"
    title: str = "Registration"
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = reverse_lazy("account:login")

    def form_valid(self, form):
        """Save inactive user and send registration email for verification"""

        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email.delay(self.object.pk)
        return super().form_valid(form)


class ActivateUser(RedirectView):
    """Handle user account activation via email link"""

    url = reverse_lazy("core:index")

    def get(self, request, uuid64, token, *args, **kwargs):
        """Verify activation token and activate user account"""

        try:
            pk = force_str(urlsafe_base64_decode(uuid64))
            current_user = get_user_model().objects.get(pk=pk)
        except (ValueError, get_user_model().DoesNotExist, TypeError):
            return HttpResponse("Activation link is invalid")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(
                request,
                current_user,
                backend="django.contrib.auth.backends.ModelBackend",
            )

            return super().get(request, *args, **kwargs)

        return HttpResponse("Activation link is invalid")


class ResetPasswordView(TitleMixin, SuccessMessageMixin, PasswordResetView):
    """Handle password reset request and send reset email"""

    template_name: str = "registration/password/password_reset.html"
    title: str = "Reset Password"
    success_url = reverse_lazy("account:login")
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    subject_template_name: str = "registration/password/password_reset_subject.html"
    email_template_name: str = "registration/password/password_reset_email.txt"


class ProfileView(LoginRequiredMixin, TitleMixin, UpdateView):
    """Handle user profile viewing and updating with avatar and 2FA QR code"""

    template_name: str = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")
    title: str = "Profile"

    def get_object(self):
        """Return the current authenticated user"""

        return self.request.user

    def get_initial(self):
        """Load initial form data from user and profile fields"""

        user = self.request.user
        profile = user.profile
        return {
            **{
                field: (user.format_phone_number() if field == "phone_number" else getattr(user, field))
                for field in ["first_name", "last_name", "email", "phone_number"]
            },
            **{field: getattr(profile, field) for field in ["birth_date", "sex", "location", "status"]},
        }

    def _update_profile(self, form):
        """Update user and profile fields from form data"""

        user = form.save(commit=False)
        profile = user.profile

        for field in ["first_name", "last_name", "phone_number"]:
            setattr(user, field, form.cleaned_data[field])
        user.save()

        for field in ["birth_date", "sex", "location", "status"]:
            setattr(profile, field, form.cleaned_data[field])

        if "avatar" in self.request.FILES:
            profile.avatar = self.request.FILES["avatar"]

        profile.save()

    def _has_changes(self, form, user):
        """Check if form data differs from current user and profile data"""

        profile = user.profile

        user_changed = any(
            form.cleaned_data[field] != getattr(user, field) for field in ["first_name", "last_name", "phone_number"]
        )

        profile_changed = any(
            form.cleaned_data[field] != getattr(profile, field) for field in ["birth_date", "sex", "location", "status"]
        )

        avatar_changed = "avatar" in self.request.FILES

        return user_changed or profile_changed or avatar_changed

    def form_valid(self, form):
        """Process valid profile form and update user data if changes detected"""

        if self._has_changes(form, self.request.user):
            self._update_profile(form)
            messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)

    def _generate_qr_code(self):
        """Generate QR code for 2FA setup and return as base64 encoded image"""

        user = self.request.user
        if not user.mfa_secret:
            user.mfa_secret = pyotp.random_base32()
            user.save()

        otp_uri = pyotp.totp.TOTP(user.mfa_secret).provisioning_uri(name=user.email, issuer_name="Test Assignment")

        qr = qrcode.make(otp_uri)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    def get_context_data(self, **kwargs):
        """Add QR code to template context for 2FA setup"""

        context = super().get_context_data(**kwargs)
        context["qrcode"] = self._generate_qr_code()
        return context


class VerifyMfa(View):
    """Handle 2FA verification using OTP code"""

    template_name: str = "registration/2FA/otp_verify.html"
    success_url = reverse_lazy("account:profile")
    auth_backend: str = "django.contrib.auth.backends.ModelBackend"

    def post(self, request, *args, **kwargs):
        """Verify OTP code and enable 2FA or login user"""

        otp = request.POST.get("otp_code")
        user_id = request.POST.get("user_id")

        if not user_id:
            messages.error(request, "Invalid user id. Please try again.")
            return render(request, self.template_name, {"user_id": user_id})

        user = get_user_model().objects.get(id=user_id)
        if verify_2fa_otp(user, otp):
            if not request.user.is_authenticated:
                login(request, user, backend=self.auth_backend)
            messages.success(request, "2FA enabled successfully!")

        else:
            messages.success(request, "Login successful!")
            return redirect("account:profile")

        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        """Render OTP verification page."""
        user_id = request.GET.get("user_id")
        return render(request, self.template_name, {"user_id": user_id})


class Disable2fa(LoginRequiredMixin, View):
    """Handle disabling 2FA for user account"""

    success_url = reverse_lazy("account:profile")

    def get(self, request, *args, **kwargs):
        """Disable 2FA for the authenticated user"""

        user = request.user
        if user.mfa_enabled:
            user.mfa_enabled = False
            user.save()
            messages.success(request, "2FA disabled successfully!")
        else:
            messages.error(request, "2FA is not enabled for this account!")

        return redirect(self.success_url)
