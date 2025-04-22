from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from .forms import AuthenticateForm
from .forms import UserCreateForm
from django.contrib.auth import authenticate, login as auth_login
import re

from django.contrib.auth.models import Group


# Create your views here.

def check(request):
     return render(request, 'servercheck.html')

def user_login(request):
    if request.method == "GET":
        return render(request, 'accountlogin.html', {'form':AuthenticateForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'accountlogin.html', {'form':AuthenticateForm(), 'error': 'Invalid user credentials'})
        else:
            login(request,user)
            return redirect('event_list')

def signupaccount(request):
   
    if request.method == "GET":
        return render(request, 'signupaccount.html', {'form':UserCreateForm()})
    else:
       if request.method == "POST":
        form = UserCreateForm()
        
        
        user_email = request.POST['username']  # Username is the email
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name =  request.POST['first_name']
        last_name = request.POST['last_name']


        # Email validation using regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, user_email):
            return render(request, 'signupaccount.html', {'form': form, 'error': 'Invalid email format. Please enter a valid email.'})
        # Password validation (only lowercase letters, 4-8 characters)
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$', password1):
             return render(request, 'signupaccount.html', {
                 'form': form,
                 'error': 'Password must be at least 6 characters long and include at least one uppercase letter, one lowercase letter, and one number.'
             })
# Password match validation
        if password1 != password2:
            return render(request, 'signupaccount.html', {'form': form, 'error': 'Passwords do not match.'})
        # Check if email already exists
        try:
            user = User.objects.create_user(username=user_email,  password=password1, email=user_email, first_name = first_name, last_name =last_name)
            user.save()
            registrant_group, created = Group.objects.get_or_create(name='Registrants')
            user.groups.add(registrant_group)

        except IntegrityError:
            return render(request, 'signupaccount.html', {'form': form, 'error': 'This email is already registered.'})
        # Auto-login after successful registration
        user = authenticate(request, username=user_email, password=password1)
        if user:
            auth_login(request, user)
            return redirect('event_list')  # Redirect to success page
        else:
            return render(request, 'signupaccount.html', {'form': form, 'error': 'Authentication failed. Please log in manually.'})
    

def user_logout(request):
    logout(request)
    return redirect('user_login')
