from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile, Skill, Project

User = get_user_model()


class PortfolioPublicTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_superuser(
            email='admin@test.com', username='admin', password='testpass123', is_owner=True
        )
        self.profile = Profile.objects.create(
            name='Mujahid Islam',
            bio='Test bio',
            email='test@test.com'
        )
        self.skill = Skill.objects.create(name='Python', category='backend', proficiency=85)
        self.project = Project.objects.create(
            title='Test Project',
            slug='test-project',
            description='A test project',
            status='completed',
            is_featured=True
        )

    def test_profile_public(self):
        resp = self.client.get('/api/profile/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'Mujahid Islam')

    def test_skills_public(self):
        resp = self.client.get('/api/skills/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_projects_public(self):
        resp = self.client.get('/api/projects/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_project_create_requires_auth(self):
        resp = self.client.post('/api/projects/', {
            'title': 'Unauthorized Project',
            'slug': 'unauthorized',
            'description': 'test'
        })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_create_project(self):
        self.client.force_authenticate(user=self.owner)
        resp = self.client.post('/api/projects/', {
            'title': 'Owner Project',
            'slug': 'owner-project',
            'description': 'Owner created this',
            'status': 'completed',
            'tech_stack': ['Python', 'Django']
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
