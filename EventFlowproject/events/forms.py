"""Defining forms for the events app"""

from django import forms
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Validate start_date is not in the past
        if start_date and start_date < timezone.now().date():
            self.add_error('start_date', "Start date cannot be in the past.")

        # Validate end_date is not before start_date
        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', "End date cannot be before start date.")

        return cleaned_data
