from django.urls import path
from events.views import CreateEvent, OrganizerDashboard, create_category, dashboard, delete_event, participant_dashboard, rsvp, update_event, view_event

urlpatterns = [
    path("organizer_dashboard/", OrganizerDashboard.as_view(), name="organizer_dashboard"),    
    path("create_event/", CreateEvent.as_view(), name="create_event"),
    path("view_event/<int:id>/", view_event, name="view_event"),
    path("update_event/<int:id>/", update_event, name="update_event"),
    path("delete_event/<int:id>/", delete_event, name="delete_event"),
    path("rsvp/<int:event_id>/", rsvp, name="rsvp"),
    path("participant_dashboard/<int:user_id>", participant_dashboard, name="participant_dashboard"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create_category", create_category, name="create_category")
]
