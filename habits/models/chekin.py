from django.db import models

from .habit import Habit


class CheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.habit} : ${self.created_at}'
