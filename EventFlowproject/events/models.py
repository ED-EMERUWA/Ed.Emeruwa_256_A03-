from django.db import models

# Create your models here
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    registrants = models.ManyToManyField(User, related_name='events', blank=True)

    def clean(self):
        today = timezone.now().date()

        if self.start_date and self.start_date < today:
            raise ValidationError({
                'start_date': "Start date cannot be in the past."
            })
        
      
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': "End date cannot be before start date."
            })
        
    def __str__(self):
        return self.name
