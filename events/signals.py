from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event

@receiver(m2m_changed, sender=Event.participant.through)
def notify_participant_on_rsvp(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        users = []

        for user in instance.participant.all():
            if user.id in pk_set:
                users.append(user)
        for user in users:
	        send_mail(
	            "RSVP Confirmation",
	            f"you have been successfully RSVP'd to the event : {instance.name}, Thank you for joining",
	            "cl1075023@gmail.com",
	            recipient_list=[user.email],
	            fail_silently=False,
	        )