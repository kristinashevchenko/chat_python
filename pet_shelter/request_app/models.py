from django.db import models
from django.contrib.auth import get_user_model
from pet_app.models import Pet

User = get_user_model()

activeStatus = 'A'
closedStatus = 'C'
nonAppearanceStatus = 'N'

statuses = [
            (closedStatus, 'Closed'),
            (activeStatus, 'Active'),
            (nonAppearanceStatus, 'Non-appearance'),
            ]


class PetRequest(models.Model):
    pet = models.ForeignKey(Pet, null=False, on_delete=models.CASCADE, )
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='+',)
    date_arrive = models.DateField(null=False)
    status = models.CharField(choices=statuses, max_length=10, default=activeStatus)
    comment = models.TextField()

    def __repr__(self):
        return f'Pet: {self.pet}' \
               f'User:{self.user}' \
               f'Date_arrive {self.date_arrive}' \
               f'Status: {self.status}' \
               f'Comment: {self.comment}'

    def __str__(self):
        return f'{self.user} takes {self.pet} at {self.date_arrive}'
