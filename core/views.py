from urllib.parse import urlencode
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from events.models import Category, Event
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    user = request.user
    search_event = request.GET.get("search")
    ctg = request.GET.get("category")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    categories = Category.objects.all()
    events_qs = Event.objects.select_related("category").all()

    if ctg:
        events_qs = events_qs.filter(category__name=ctg)

    if start_date and end_date:
        events_qs = events_qs.filter(date__range=[start_date, end_date])

    if search_event:
        events_qs = events_qs.filter(
            Q(name__icontains=search_event) | Q(location__icontains=search_event)
        )

    paginator = Paginator(events_qs, 8) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    params = request.GET.copy()
    if "page" in params:
        params.pop("page")
    querystring = params.urlencode()  

    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "events": page_obj,       
            "page_obj": page_obj,
            "search_event": search_event,
            "user": user,
            "category": ctg,
            "start_date": start_date,
            "end_date": end_date,
            "querystring": querystring,
        },
    )


def no_permission(request):
    return render(request, "no_permission.html")
