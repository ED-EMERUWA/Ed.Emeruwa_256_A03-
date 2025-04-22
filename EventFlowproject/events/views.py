from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import EventForm
from django.utils import timezone

# Thanks for everything Allan. You'll be missed.

def current_event_list(request):
    if not request.user.is_authenticated:
        return redirect('user_login')  # Replace 'login' with the actual name of your login URL
    
    today = timezone.now().date()
    events = Event.objects.filter(start_date__gte=today).order_by('start_date')
    user_events = request.user.events.all()

    return render(request, 'current_event_list.html', {
        'events': events,
        'user_events': user_events
    })

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.registrants.add(request.user)
    return redirect('event_list')  # or a confirmation page

@login_required
def unregister_from_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.registrants.remove(request.user)
    return redirect('event_list')



def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@login_required
def user_list(request):
    if not user_in_group(request.user, 'Administrators'):
        return render(request, '403_forbidden.html', status=403)

    users = User.objects.all().select_related()
    return render(request, 'user_list.html', {'users': users})

def all_events_list(request):
    if not user_in_group(request.user, 'Administrators'):
        return render(request, '403_forbidden.html', status=403)

    today = timezone.now().date()
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'past':
        events = Event.objects.filter(end_date__lt=today)
    elif filter_type == 'upcoming':
        events = Event.objects.filter(start_date__gt=today)
    elif filter_type == 'current':
        events = Event.objects.filter(start_date__lte=today, end_date__gte=today)
    else:
        events = Event.objects.all()

    events = events.order_by('start_date')
    user_events = request.user.events.all()

    return render(request, 'all_events_list.html', {
        'events': events,
        'user_events': user_events,
        'selected_filter': filter_type,
    })

@login_required
def create_event(request):
    if not user_in_group(request.user, 'Administrators'):
        return render(request, '403_forbidden.html', status=403)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})