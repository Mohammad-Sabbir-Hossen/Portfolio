from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender='blog.Comment')
def notify_owner_on_comment(sender, instance, created, **kwargs):
    """Send email to owner when a new comment is submitted."""
    if created:
        try:
            send_mail(
                subject=f'[Portfolio] New comment on "{instance.post.title}"',
                message=(
                    f'Name: {instance.name}\n'
                    f'Email: {instance.email}\n\n'
                    f'Comment:\n{instance.body}\n\n'
                    f'Post: {instance.post.title}\n'
                    f'Approve or reject from the admin panel.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.OWNER_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            logger.warning('Failed to send comment notification email: %s', e)
