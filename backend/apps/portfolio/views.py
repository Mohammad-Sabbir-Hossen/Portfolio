from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Profile, Skill, Project, Education, Experience
from .serializers import (
    ProfileSerializer, SkillSerializer, ProjectSerializer,
    EducationSerializer, ExperienceSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only the authenticated owner (superuser/is_owner) can write."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.is_superuser or getattr(request.user, 'is_owner', False))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def profile_view(request):
    """Public: get the owner's profile."""
    try:
        profile = Profile.objects.first()
        if not profile:
            return Response({'detail': 'Profile not configured yet.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def admin_profile_view(request):
    """Owner only: update profile."""
    if not (request.user.is_superuser or getattr(request.user, 'is_owner', False)):
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    profile = Profile.objects.first()
    if not profile:
        if request.method in ('PUT', 'PATCH'):
            serializer = ProfileSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Profile not configured yet.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    serializer = ProfileSerializer(profile, data=request.data, partial=(request.method == 'PATCH'), context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.filter(is_visible=True)
    serializer_class = SkillSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['order', 'name', 'proficiency']

    def get_queryset(self):
        if self.request.user.is_authenticated and (self.request.user.is_superuser or getattr(self.request.user, 'is_owner', False)):
            return Skill.objects.all()
        return Skill.objects.filter(is_visible=True)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'is_featured']
    search_fields = ['title', 'description', 'tech_stack']
    ordering_fields = ['order', 'created_at', 'title']
    lookup_field = 'slug'


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsOwnerOrReadOnly]
    ordering_fields = ['order', 'start_year']


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadOnly]
    ordering_fields = ['order', 'start_date']
