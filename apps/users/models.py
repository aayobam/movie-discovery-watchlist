from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from apps.common import choices
from apps.common.base_model import BaseModel
from apps.users.managers import CustomUserManager


class CustomUser(BaseModel, PermissionsMixin, AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    gender = models.CharField(default="male", choices=choices.GENDER, max_length=10)
    phone_no = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to="profile picture/", default="images/dummy.png")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __str__(self):
        return f"{self.email}"

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"id": self.id})
