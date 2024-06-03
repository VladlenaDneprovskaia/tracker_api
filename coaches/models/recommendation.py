from django.db import models

from .coach import Coach
from .mentees import Mentee


class Recommendation(models.Model):
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
    message = models.TextField()

    def __str__(self):
        return f'{self.mentee} : {self.message}'
