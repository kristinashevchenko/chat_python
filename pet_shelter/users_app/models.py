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
        extra_fields.setdefault('is_staff', False)
        extra_fields['is_superuser'] = False
        extra_fields['is_volunteer'] = False
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_volunteer(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields['is_superuser'] = False
        extra_fields['is_customer'] = False
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields['is_customer'] = False
        extra_fields['is_volunteer'] = False
        extra_fields['is_superuser'] = True
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    is_customer = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can be managed as customer'),
    )
    is_volunteer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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
