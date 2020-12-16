import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.authtoken.models import Token
# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_customer(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_customer', True)
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_volonteer(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_volonteer', True)
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    def generate_random_string(self, symbols_count=30):
        return str(uuid.uuid4())[:symbols_count]

    def generate_random_email(self):
        return '{}@{}.ae'.format(
            self.generate_random_string(20),
            self.generate_random_string(10),
        )

    # def create_temp_user(self):
    #     return self.create_user(
    #         username=self.generate_random_string(),
    #         email=self.generate_random_email(),
    #         password=self.generate_random_string(),
    #         is_temporary=True,
    #         is_customer=True,
    #     )


class User(AbstractUser):
    is_customer = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can be managed as customer'),
    )
    is_volonteer = models.BooleanField(default=False)

    objects = UserManager()

    @property
    def token(self):
        try:
            return self.auth_token
        except models.ObjectDoesNotExist:
            return None

    def generate_token(self):
        token, _ = Token.objects.get_or_create(user=self)
        return token.key
