from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, no_permission
from users.views import sign_in
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("users/", include("users.urls")),
    path('', home, name='home'),
    path('no_permission/', no_permission, name='no_permission'),
    path('sign_in/', sign_in, name='sign_in')
] + debug_toolbar_urls()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)