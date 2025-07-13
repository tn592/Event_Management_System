from django.shortcuts import render
from django.contrib import messages
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render
from django.http import HttpResponse
from events.forms import EventModelForm
from events.models import Event, Category
from datetime import date
from django.db.models import Q
def home(request):
    search_event = request.GET.get('search')  
    ctg = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    categories = Category.objects.all()
    events = Event.objects.select_related('category')

    if ctg:
        events = events.filter(category__name=ctg)

    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    if search_event:
        events = events.filter(
            Q(name__icontains=search_event) | Q(location__icontains=search_event)
        )

    return render(request, "dashboard/home.html", 
        {
        "categories": categories, 
        "events":events, 
        "search_event": search_event
        })

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


def create_event(request):
    event_form = EventModelForm() 
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        
        if event_form.is_valid():
            event = event_form.save()

            messages.success(request, "Event Created Successfully")
            return redirect(
                'home'
            )

    context = {"event_form": event_form}
    return render(request, "event_form.html", context)


def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event) 
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request, "event Updated Successfully")
            return redirect(
                'update_event', id
            )

    context = {"event_form": event_form}
    return render(request, "event_form.html", context)


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
