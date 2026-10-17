from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('admin', views.AdminContactViewSet, basename='admin-contact')

urlpatterns = [
    path('', views.submit_contact, name='contact-submit'),
    path('', include(router.urls)),
]
