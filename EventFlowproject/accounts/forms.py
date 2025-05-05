"""Defining forms for the accounts app"""

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

class AuthenticateForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password']:
            self.fields[fieldname].widget.attrs.update({'class':'px-3 py-3 rounded-l-lg'})

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'px-3 py-3 rounded-lg w-full'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'px-3 py-3 rounded-lg w-full'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2', 'first_name', 'last_name']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'px-3 py-3 rounded-lg w-full'})
