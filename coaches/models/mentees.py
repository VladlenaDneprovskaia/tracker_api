from django.contrib.auth.models import User
from django.db import models

from coaches.models import Coach


class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.coach} : {self.user}'
