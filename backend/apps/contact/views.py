from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import logging

from .models import ContactMessage
from .serializers import ContactMessageSerializer, ContactMessageAdminSerializer

logger = logging.getLogger(__name__)


class ContactThrottle(AnonRateThrottle):
    rate = '5/hour'
    scope = 'contact'


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([ContactThrottle])
def submit_contact(request):
    """Public: submit a contact message."""
    serializer = ContactMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()

    # Notify owner
    try:
        send_mail(
            subject=f'[Portfolio] New Message: {instance.subject}',
            message=(
                f'From: {instance.name} <{instance.email}>\n\n'
                f'Subject: {instance.subject}\n\n'
                f'Message:\n{instance.message}'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.OWNER_EMAIL],
            fail_silently=True,
        )
    except Exception as e:
        logger.warning('Failed to send contact notification: %s', e)

    return Response(
        {'detail': 'Message sent successfully! I will get back to you soon.'},
        status=status.HTTP_201_CREATED
    )


class AdminContactViewSet(viewsets.ModelViewSet):
    """Owner-only: view and manage contact messages."""
    serializer_class = ContactMessageAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_read']
    search_fields = ['name', 'email', 'subject']
    ordering_fields = ['created_at']
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, 'is_owner', False):
            return ContactMessage.objects.all()
        return ContactMessage.objects.none()
