from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .models import CustomUser
from apps.common.utils import Validators
from .mixings import is_authenticated
from django.db import transaction


@method_decorator(is_authenticated, name="dispatch")
class RegisterUserView(generic.CreateView):
    model = CustomUser
    fields = '__all__'
    template_name = "users/register.html"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_data = {
            "first_name": request.POST.get("first-name"),
            "last_name": request.POST.get("last-name"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }
        confirm_password = request.POST.get("confirm-password")

        email = user_data.get("email")

        if not self.validate_email(email):
            messages.error(self.request, f"email: {email} already exist.")
            return redirect("create_account")

        if not Validators.validate_password(user_data.get("password"), confirm_password):
            messages.error(
                self.request, "password and confirm password do not match, please try again.")
            return redirect("create_account")

        if not Validators.validate_password_length(user_data.get("password")):
            messages.error(self.request, "password lenght cannot be less than 8, please try again.")
            return redirect("create_account")

        user: CustomUser = self.model.objects.create(**user_data)
        user.set_password(user_data.get("password"))
        user.save()
        messages.success(self.request, "registration successful.")
        return redirect("user_login")

    def validate_email(self, email):
        if self.model.objects.filter(email=email).exists():
            return False
        return True


class UserProfileView(LoginRequiredMixin, generic.UpdateView):
    """
    Users can view their profiles and perform updates.
    """
    model = CustomUser
    fields = "__all__"
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user

    def patch_user(self, user, user_data):
        for key, value in user_data.items():
            setattr(user, key, value)
        user.save()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_data = {
            "first_name": request.POST.get("first-name"),
            "last_name": request.POST.get("last-name"),
            "email": request.POST.get("email"),
        }

        profile_picture = request.FILES.get("profile-picture")

        if profile_picture:
            user_data["profile_picture"] = profile_picture

        user = self.get_object()
        self.patch_user(user, user_data)
        messages.success(request, "Profile updated successfully")
        return redirect("user_profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        return context


class DeleteUserView(LoginRequiredMixin, generic.DeleteView):
    """
    users can delete their profile, but this button doesn't exist on template. (optional)
    """
    queryset = CustomUser.objects.all()
    template_name = "users/delete.html"
    success_url = reverse_lazy("user_login")


@method_decorator(is_authenticated, name="dispatch")
class UserLoginView(generic.TemplateView):
    model = CustomUser
    template_name = "users/login.html"

    @transaction.atomic
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 8:
            messages.error(self.request, "password cannot be less than 8.")
            return redirect("user_login")

        if not CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "Email does not exist.")
            return redirect("user_login")

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if "next" in request.POST:
                messages.success(request, f"Login successful.")
                return redirect(request.POST.get("next"))
            return redirect("user_profile")

        messages.error(request, "Login unsuccessful, please try again.")
        return redirect("user_login")


class UserLogoutView(generic.TemplateView):
    def get(self, request):
        logout(request)
        messages.success(self.request, "logout successful.")
        return redirect('user_login')


class ChangePasswordView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy("user_profile")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        old_password: str = request.POST.get("old-password")
        new_password: str = request.POST.get('new-password')
        confirm_new_password: str = request.POST.get('confirm-new-password')

        user: CustomUser = request.user

        if not user.check_password(old_password):
            messages.warning(request, "old password doesn't match.")
            return redirect("change_password")

        if len(new_password) < 8:
            messages.warning(
                request, "password length should not be less than 8.")
            return redirect("change_password")

        if old_password == new_password:
            messages.warning(
                request, "your new password cannot be the same as your old password.")
            return redirect("change_password")

        if new_password != confirm_new_password:
            messages.warning(
                request, "password and confirm password do not match.")
            return redirect("change_password")

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(
            request, "password change successfull. your new password would take effect on next login.")
        return redirect("user_profile")
