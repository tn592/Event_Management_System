"""
ASGI config for event_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")

application = get_asgi_application()

try:
    # Only run if running in production
    if os.environ.get("RENDER"):
        print("Loading initial data from db.json...")
        call_command('loaddata', 'db.json')
        print("✅ Initial data loaded successfully.")
except Exception as e:
    print(f"⚠️ Could not load initial data: {e}")
