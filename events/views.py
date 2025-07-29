from django.shortcuts import render
from django.contrib import messages
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render
from events.forms import CategoryForm, EventModelForm
from events.models import Event
from datetime import date
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from users.views import is_admin
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.contrib.auth import get_user_model


User = get_user_model()


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def is_participant(user):
    return user.groups.filter(name='User').exists()


is_organizer_decorator = user_passes_test(is_organizer, login_url='no_permission')


@method_decorator(is_organizer_decorator, name='dispatch')
class OrganizerDashboard(ListView):
    model = Event
    template_name = 'dashboard/organizer-dashboard.html'
    context_object_name = 'events' 

    def get_queryset(self):
        type = self.request.GET.get('type', 'all')
        base_query = Event.objects.select_related('category').prefetch_related('participant')
        if type == 'upcoming':
            return base_query.filter(date__gte=date.today()).order_by('date')
        elif type == 'past':
            return base_query.filter(date__lt=date.today()).order_by('-date')
        elif type == 'total':
            return base_query.order_by('date')
        else:
            return base_query.filter(date=date.today())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counts'] = Event.objects.aggregate(
            total_events=Count('id', distinct=True),
            total_participants=Count('participant', distinct=True),  
            upcoming_events=Count('id', filter=Q(date__gte=date.today()), distinct=True),
            past_events=Count('id', filter=Q(date__lt=date.today()), distinct=True)
        )
        return context


is_organizer_decorator = user_passes_test(is_organizer, login_url='no_permission')


@method_decorator(is_organizer_decorator, name='dispatch')
class CreateEvent(ContextMixin, LoginRequiredMixin, View):
    login_url = 'sign_in'
    template_name = 'event_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = kwargs.get('event_form', EventModelForm)
        return context 

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request, "Event Created Successfully")
            context = self.get_context_data(event_form=event_form)
            return render(request, self.template_name, context)


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
    event_update_form = EventModelForm(instance=event) 
    
    if request.method == "POST":
        event_update_form = EventModelForm(request.POST, request.FILES, instance=event)
        if event_update_form.is_valid():
            event = event_update_form.save()
            messages.success(request, "event Updated Successfully")
            return redirect(
                'update_event', id
            )

    context = {"event_update_form": event_update_form}
    return render(request, "update_event_form.html", context)


@user_passes_test(is_organizer, login_url='no_permission')
def delete_event(request, id): 
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('organizer_dashboard')
    else:
        messages.error(request, "something went wrong")
        return redirect('organizer_dashboard')


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