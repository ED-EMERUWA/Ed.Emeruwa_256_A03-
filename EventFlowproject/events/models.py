from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    registrants = models.ManyToManyField(User, related_name='events', blank=True)

    def __str__(self):
        return self.name
