from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Day(models.Model):
    day = models.CharField(max_length=10)

    def __str__(self):
        return self.day


class Todo(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True)
    task = models.CharField(max_length=250)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
