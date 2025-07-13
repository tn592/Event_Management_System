from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
# from core.views import home, no_permission
from core.views import home
from users.views import sign_in
# from events.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("users/", include("users.urls")),
    path('', home, name='home'),
    # path('no_permission/', no_permission, name='no_permission'),
    path('sign_in/', sign_in, name='sign_in')
] + debug_toolbar_urls()