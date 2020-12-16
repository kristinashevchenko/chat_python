from django.contrib import admin
from .models import Pet, Animal
from django.utils.translation import gettext_lazy as _


class PetAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Pet Info'), {'fields': (
            'name',
            'sex',
            'date_of_birth'
        )}),
        (_('Spec'), {'fields': (
            'species',
        )}),
        (_('Animal spec'), {'fields': (
            'type',
        )}),
    )

    list_filter = ('date_of_birth', )

    ordering = ('date_of_birth', 'name', )
    search_fields = ('name', 'species', 'sex', )


# Register your models here.
admin.site.register(Pet, PetAdmin)
admin.site.register(Animal)
