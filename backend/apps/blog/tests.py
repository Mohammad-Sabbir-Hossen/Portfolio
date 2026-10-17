from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import BlogPost, Category, Comment

User = get_user_model()


class BlogPublicTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_superuser(
            email='admin@test.com', username='admin', password='testpass123', is_owner=True
        )
        self.category = Category.objects.create(name='Python', slug='python')
        self.published_post = BlogPost.objects.create(
            title='Published Post',
            slug='published-post',
            content='This is a published post.',
            status='published',
            author=self.owner,
        )
        self.draft_post = BlogPost.objects.create(
            title='Draft Post',
            slug='draft-post',
            content='This is a draft post.',
            status='draft',
            author=self.owner,
        )

    def test_public_posts_only_published(self):
        resp = self.client.get('/api/blog/posts/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [p['title'] for p in resp.data['results']]
        self.assertIn('Published Post', titles)
        self.assertNotIn('Draft Post', titles)

    def test_draft_not_accessible_by_slug(self):
        resp = self.client.get('/api/blog/posts/draft-post/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_categories_public(self):
        resp = self.client.get('/api/blog/categories/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_submit_comment(self):
        resp = self.client.post(f'/api/blog/posts/{self.published_post.slug}/comments/submit/', {
            'name': 'Test User',
            'email': 'user@test.com',
            'body': 'Great article!'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_comment_requires_moderation(self):
        self.client.post(f'/api/blog/posts/{self.published_post.slug}/comments/submit/', {
            'name': 'Test User',
            'email': 'user@test.com',
            'body': 'Test comment body here'
        })
        # Comment should NOT be in public list yet
        resp = self.client.get(f'/api/blog/posts/{self.published_post.slug}/comments/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_admin_posts_requires_auth(self):
        resp = self.client.get('/api/blog/admin/posts/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_sees_all_posts(self):
        self.client.force_authenticate(user=self.owner)
        resp = self.client.get('/api/blog/admin/posts/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [p['title'] for p in resp.data['results']]
        self.assertIn('Draft Post', titles)
        self.assertIn('Published Post', titles)
