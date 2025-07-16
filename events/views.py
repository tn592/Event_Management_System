from django.shortcuts import render
from django.contrib import messages
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render
from django.http import HttpResponse
from events.forms import CategoryForm, EventModelForm
from events.models import Event, Category
from datetime import date
from django.db.models import Q
from django.db.models import Prefetch
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from users.views import is_admin

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def is_participant(user):
    return user.groups.filter(name='User').exists()

@user_passes_test(is_organizer, login_url='no_permission')
def organizer_dashboard(request):
    type = request.GET.get('type', 'all')
    base_query = Event.objects.select_related('category').prefetch_related('participant')

    counts = base_query.aggregate(
        total_events=Count('id', distinct=True),
        total_participants=Count('participant', distinct=True),  
        upcoming_events=Count('id', filter=Q(date__gte=date.today()), distinct=True),
        past_events=Count('id', filter=Q(date__lt=date.today()), distinct=True)
    )

    # Retriving event data
    if type == 'upcoming':
        events = base_query.filter(date__gte=date.today()).order_by('date')
    elif type == 'past':
        events = base_query.filter(date__lt=date.today()).order_by('-date')
    elif type == 'total':
        events = base_query.order_by('date')
    else:
        events = base_query.filter(date=date.today())

    context = {
        "events": events,
        "counts":counts
    }
    return render(request, "dashboard/organizer-dashboard.html", context)


@user_passes_test(is_organizer, login_url='no_permission')
def create_event(request):
    event_form = EventModelForm() 
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES)
        
        if event_form.is_valid():
            event = event_form.save()

            messages.success(request, "Event Created Successfully")
            return redirect(
                'home'
            )

    context = {"event_form": event_form}
    return render(request, "event_form.html", context)


def create_category(request):
    ctg_form = CategoryForm
    
    if request.method == "POST":
        ctg_form = CategoryForm(request.POST)
        
        if ctg_form.is_valid():
            ctg = ctg_form.save()

            messages.success(request, "Category Created Successfully")
            return redirect(
                'home'
            )

    context = {"ctg_form": ctg_form}
    return render(request, "category_form.html", context)




@user_passes_test(is_organizer, login_url='no_permission')
def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event) 
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES, instance=event)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request, "event Updated Successfully")
            return redirect(
                'update_event', id
            )

    context = {"event_form": event_form}
    return render(request, "event_form.html", context)


@user_passes_test(is_organizer, login_url='no_permission')
def delete_event(request, id): 
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect(organizer_dashboard)
    else:
        messages.error(request, "something went wrong")
        return redirect(organizer_dashboard)


def view_event(request, id):
    event = Event.objects.get(id=id)
    return render(
        request,
        "show_event.html",
        {"event": event}
    )

@login_required
def rsvp(request, event_id):
    user = request.user
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        event = Event.objects.get(id=event_id)
        prt = event.participant.filter(id=user.id).exists()
        if not prt:
            event.participant.add(user)
            messages.success(request, "RSVP Confirmed")
        else:
            messages.error(request, "This event is already booked")

        return redirect('home')
    else:
        messages.error(request, "something went wrong")
        return redirect('home')


def participant_dashboard(request, user_id):
    user = User.objects.get(id=user_id)
    event = Event.objects.filter(participant=user).select_related('category')

    return render(request, "dashboard/participant_dashboard.html", {"event": event, "user":user})


@login_required 
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer_dashboard')
    elif is_participant(request.user):
        return redirect('participant_dashboard', user_id=request.user.id)
    elif is_admin(request.user):
        return redirect('admin_dashboard')

    return redirect('no_permission')