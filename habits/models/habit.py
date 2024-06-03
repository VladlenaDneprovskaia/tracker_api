from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Habit(models.Model):
    class Frequency(models.TextChoices):
        DAY = 'DD', _('Day')
        WEEK = 'WW', _('Week')
        MONTH = 'MM', _('Month')
        YEAR = 'YY', _('Year')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(
        max_length=2,
        choices=Frequency.choices,
        default=Frequency.DAY,
    )

    def __str__(self):
        return f'{self.user} : {self.name}'
