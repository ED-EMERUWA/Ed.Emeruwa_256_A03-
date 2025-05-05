from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import EventForm
from django.utils import timezone

# Thanks for everything Allan. You'll be missed.

def current_event_list(request):
    """Display a list of events starting today or later for authenticated users."""
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    today = timezone.now().date()
    events = Event.objects.filter(start_date__gte=today).order_by('start_date')
    user_events = request.user.events.all()

    return render(request, 'current_event_list.html', {
        'events': events,
        'user_events': user_events
    })


@login_required
def register_for_event(request, event_id):
    """Register the current user for the specified event."""
    event = get_object_or_404(Event, pk=event_id)
    event.registrants.add(request.user)
    return redirect('event_list')


@login_required
def unregister_from_event(request, event_id):
    """Unregister the current user from the specified event."""
    event = get_object_or_404(Event, pk=event_id)
    event.registrants.remove(request.user)
    return redirect('event_list')


def user_in_group(user, group_name):
    """Check if a user is part of a specific group."""
    return user.groups.filter(name=group_name).exists()


@login_required
def user_list(request):
    """Display a list of all users (admin only)."""
    if not user_in_group(request.user, 'Administrators'):
        return render(request, '403_forbidden.html', status=403)

    users = User.objects.all().select_related()
    return render(request, 'user_list.html', {'users': users})


def all_events_list(request):
    """Display all events with optional filter: past, current, upcoming (admin only)."""
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
    """Allow admins to create a new event."""
    if not user_in_group(request.user, 'Administrators'):
        return render(request, '403_forbidden.html', status=403)

    error = None

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            today = timezone.now().date()

            if start_date < today:
                error = "Start date cannot be in the past."
            elif end_date < start_date:
                error = "End date cannot be before start date."

            if not error:
                form.save()
                return redirect('all_events_list')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form, 'error': error})


@login_required
def admin_panel(request):
    """Render the admin dashboard if the user is an admin."""
    if not user_in_group(request.user, 'Administrators'):
        return render(request, '403_forbidden.html', status=403)
    
    return render(request, 'admin_panel.html')


@login_required
def edit_event(request, event_id):
    """Allow admins to edit an existing event."""
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})


@login_required
def confirm_delete_event(request, event_id):
    """Render the confirmation page for deleting an event."""
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'confirm_delete.html', {'event': event})


@login_required
def delete_event(request, event_id):
    """Delete the specified event after confirmation."""
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        return redirect('event_list')

    return redirect('confirm_delete_event', event_id=event_id)
