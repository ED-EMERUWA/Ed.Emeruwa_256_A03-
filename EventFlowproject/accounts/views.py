from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from .forms import AuthenticateForm, UserCreateForm
from django.contrib.auth import authenticate, login as auth_login
import re

# Create your views here.

def check(request):
    """Simple server check view for testing rendering."""
    return render(request, 'servercheck.html')

def user_login(request):
    """Handle user login with form validation."""
    if request.method == "GET":
        return render(request, 'accountlogin.html', {'form': AuthenticateForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'accountlogin.html', {'form': AuthenticateForm(), 'error': 'Invalid user credentials'})
        else:
            login(request, user)
            return redirect('event_list')

def signupaccount(request):
    """Handle user signup, including form validation, email and password checks, and group assignment."""
    if request.method == "GET":
        return render(request, 'signupaccount.html', {'form': UserCreateForm()})
    else:
        form = UserCreateForm()
        
        user_email = request.POST['username']  # Username is the email
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Email validation using regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, user_email):
            return render(request, 'signupaccount.html', {'form': form, 'error': 'Invalid email format. Please enter a valid email.'})
        
        # Password validation
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$', password1):
            return render(request, 'signupaccount.html', {
                'form': form,
                'error': 'Password must be at least 6 characters long and include at least one uppercase letter, one lowercase letter, and one number.'
            })

        # Password match check
        if password1 != password2:
            return render(request, 'signupaccount.html', {'form': form, 'error': 'Passwords do not match.'})
        
        # Try to create the user
        try:
            user = User.objects.create_user(username=user_email, password=password1, email=user_email,
                                            first_name=first_name, last_name=last_name)
            user.save()
            registrant_group, created = Group.objects.get_or_create(name='Registrants')
            user.groups.add(registrant_group)
        except IntegrityError:
            return render(request, 'signupaccount.html', {'form': form, 'error': 'This email is already registered.'})

        # Auto-login after successful signup
        user = authenticate(request, username=user_email, password=password1)
        if user:
            auth_login(request, user)
            return redirect('event_list')
        else:
            return render(request, 'signupaccount.html', {'form': form, 'error': 'Authentication failed. Please log in manually.'})

def user_logout(request):
    """Log out the current user and redirect to login page."""
    logout(request)
    return redirect('user_login')
