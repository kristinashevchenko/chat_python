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
    date_of_appear = models.DateField(default=None)
    date_of_birth = models.DateField(default=None)
    has_vaccination = models.BooleanField(default=False)
    additional_info = models.CharField(max_length=250)
    is_sterilized = models.BooleanField(default=False)
    is_prioritized = models.BooleanField(default=False)
    breed = models.CharField(max_length=80, default='No breed')
    photo_url = models.CharField(max_length=250)
    is_reserved = models.BooleanField(default=False)
    found_home = models.BooleanField(default=False)

    def calculate_age(self):
        today = date.today()
        date_of_birth = self.date_of_birth
        return today.year - date_of_birth.year - \
               ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    def __repr__(self):
        return f'Type: {self.type}' \
               f'Name:{self.name}' \
               f'Breed {self.breed}' \
               f'Age: {self.calculate_age()}'

    def __str__(self):
        return f'{self.type} {self.name}: breed {self.breed}'
