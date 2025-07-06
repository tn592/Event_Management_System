from django.urls import path
from events.views import create_event, delete_event, home, organizer_dashboard, update_event, view_event
# delete_task, dashboard, update_task,user_dashboard,
urlpatterns = [
    path("home/", home, name="home"),
    path("organizer_dashboard/", organizer_dashboard, name="organizer_dashboard"),
    path("create_event/", create_event, name="create_event"),
    path("view_event/<int:id>/", view_event, name="view_event"),
    path("update_event/<int:id>/", update_event, name="update_event"),
    path("delete_event/<int:id>/", delete_event, name="delete_event"),
    
]
