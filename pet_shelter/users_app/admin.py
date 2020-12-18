from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from .models import User
from .signals import create_auth_token
from rest_framework.authtoken.models import Token


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_volunteer', 'is_superuser', 'is_customer'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_volunteer', 'is_active', 'is_customer',)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_volunteer',
        'is_superuser',
        'is_active',
        'is_customer',
    )
    ordering = ('username',)
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        post_save.connect(create_auth_token, sender=get_user_model())


admin.site.register(User, CustomUserAdmin)
