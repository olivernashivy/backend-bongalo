import random
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.utils import timezone
from django.conf import settings
from django.db import models



class UserManager(DefaultUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:  
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True: 
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return self.email


    @property
    def full_name(self):
        # For _sure_ we can show the first name and last name
        return f"{self.first_name or ''} {(self.last_name and self.last_name) or ''}"



def generate_otp_value():
    return random.randint(0, 10**settings.OTP_DIGITS_QUANTITY - 1)


class OneTimePassword(models.Model):
    user = models.ForeignKey(User, related_name='one_time_passwords', on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    value = models.IntegerField(default=generate_otp_value)
    set_password_key = models.UUIDField(default=uuid.uuid4)
