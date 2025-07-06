"""
WSGI config for event_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")

application = get_wsgi_application()

if os.environ.get("RENDER"):
    try:
        print("📦 Running populate_db.py to seed database...")
        exec(open("populate_db.py").read())
        print("✅ Database seeded successfully.")
    except Exception as e:
        print(f"⚠️ Error running populate_db.py: {e}")