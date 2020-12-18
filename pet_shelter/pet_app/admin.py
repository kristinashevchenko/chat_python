from django.contrib import admin
from .models import Pet, Animal
from django.utils.translation import gettext_lazy as _


class PetAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Pet Info'), {'fields': (
            'name',
            'sex',
            'date_of_birth',
            'date_of_appear',
        )}),
        (_('Spec'), {'fields': (
            'breed',
        )}),
        (_('Animal spec'), {'fields': (
            'type',
        )}),
    )

    list_filter = ('date_of_birth', 'date_of_appear', )

    ordering = ('date_of_birth', 'date_of_appear', 'name', )
    search_fields = ('name', 'sex', 'breed' )


# Register your models here.
admin.site.register(Pet, PetAdmin)
admin.site.register(Animal)
