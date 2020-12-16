from django.db import models
from datetime import date


class Animal(models.Model):
    animal_type = models.CharField(max_length=100)

    def __repr__(self):
        return self.animal_type

    def __str__(self):
        return self.animal_type


class Pet(models.Model):
    type = models.ForeignKey("Animal", null=False, on_delete=models.PROTECT, related_name="pets")
    name = models.CharField(max_length=60)
    sex = models.CharField(choices=[('M', 'Male'),
                                    ('F', 'Female'),
                                    ], max_length=10)
    date_of_birth = models.DateField(default=None)
    species = models.CharField(max_length=80)
    is_dangerous = models.BooleanField(default=False)
    additional_info = models.CharField(max_length=250)

    def calculate_age(self):
        today = date.today()
        date_of_birth = self.date_of_birth
        return today.year - date_of_birth.year - \
               ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    def __repr__(self):
        return f'Type: {self.type}' \
               f'Name:{self.name}' \
               f'Species {self.species}' \
               f'Age: {self.calculate_age()}'

    def __str__(self):
        return f'{self.type} {self.name}: species {self.species}'
