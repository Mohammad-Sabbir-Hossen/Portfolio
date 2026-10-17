from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('skills', views.SkillViewSet, basename='skill')
router.register('projects', views.ProjectViewSet, basename='project')
router.register('education', views.EducationViewSet, basename='education')
router.register('experience', views.ExperienceViewSet, basename='experience')

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('admin/profile/', views.admin_profile_view, name='admin-profile'),
    path('', include(router.urls)),
]
