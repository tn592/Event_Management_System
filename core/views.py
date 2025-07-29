from django.shortcuts import render
from django.db.models import Q
from events.models import Category, Event
from django.contrib.auth import get_user_model


User = get_user_model()


# Create your views here.
def home(request):
    user = request.user
    search_event = request.GET.get("search")
    ctg = request.GET.get("category")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    categories = Category.objects.all()
    events = Event.objects.select_related("category")

    if ctg:
        events = events.filter(category__name=ctg)

    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    if search_event:
        events = events.filter(
            Q(name__icontains=search_event) | Q(location__icontains=search_event)
        )

    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "events": events,
            "search_event": search_event,
            "user": user,
        },
    )


def no_permission(request):
    return render(request, "no_permission.html")
