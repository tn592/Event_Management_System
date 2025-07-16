import os
import django
from faker import Faker
import random
from events.models import Event, Category

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()


# Function to populate the database
def populate_db():
    
    # Event.objects.all().delete()
    # Participant.objects.all().delete()
    # Category.objects.all().delete()

    # Initialize Faker
    fake = Faker()

    adjectives = [
        "Cosmic",
        "Neon",
        "Quantum",
        "Dreamwalk",
        "Stellar",
        "Aurora",
        "Ethereal",
        "Prismatic",
        "Mystic",
        "Radiant",
        "Celestial",
        "Vibrant",
    ]

    nouns1 = [
        "Mindscape",
        "Jungle",
        "Pulse",
        "Rhythm",
        "Fusion",
        "Odyssey",
        "Bloom",
        "Symphony",
        "Mirage",
        "Flux",
        "Nexus",
        "Flow",
    ]
    nouns2 = [
        "Gathering",
        "Festival",
        "Experience",
        "Confluence",
        "Assembly",
        "Collective",
        "Carnival",
        "Expedition",
        "Voyage",
        "Celebration",
    ]

    category_name = [
        "Technologies",
        "Arts",
        "Holidays",
        "Business",
        "Food&Drink"
    ]

    def random_event_name():
        return f"{random.choice(adjectives)} {random.choice(nouns1)} {random.choice(nouns2)}"

    def random_event_description():
        return (
            f"{fake.sentence()} Experience {random.choice(['immersive', 'vibrant', 'transformative'])} "
            f"moments with {random.choice(['art installations', 'interactive performances', 'visionary workshops'])}. "
            f"Connect with {random.choice(['like-minded explorers', 'kindred spirits', 'fellow adventurers'])} "
            f"and {random.choice(['expand awareness', 'ignite creativity', 'celebrate the extraordinary'])}."
        )

    # Create Category
    categories = []
    for name in category_name:
        ctg = Category.objects.create(
            name=name,
            description=fake.sentence()
        )
        categories.append(ctg)

    # Create Events
    events = []
    for _ in range(20):
        event = Event.objects.create(
            name=random_event_name(),
            description=random_event_description(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories),
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    print("Database populated successfully!")
