from django.urls import path
from events.views import create_category, create_event, dashboard, delete_event, organizer_dashboard, participant_dashboard, rsvp, update_event, view_event

urlpatterns = [
    path("organizer_dashboard/", organizer_dashboard, name="organizer_dashboard"),
    path("create_event/", create_event, name="create_event"),
    path("view_event/<int:id>/", view_event, name="view_event"),
    path("update_event/<int:id>/", update_event, name="update_event"),
    path("delete_event/<int:id>/", delete_event, name="delete_event"),
    path("rsvp/<int:event_id>/", rsvp, name="rsvp"),
    path("participant_dashboard/<int:user_id>", participant_dashboard, name="participant_dashboard"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create_category", create_category, name="create_category")
]
