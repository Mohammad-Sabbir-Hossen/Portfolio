from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('tags', views.TagViewSet, basename='tag')
router.register('posts', views.PublicBlogPostViewSet, basename='blog-post')
router.register('admin/posts', views.AdminBlogPostViewSet, basename='admin-blog-post')
router.register('admin/comments', views.AdminCommentViewSet, basename='admin-comment')

urlpatterns = [
    path('posts/<slug:slug>/comments/', views.post_comments, name='post-comments'),
    path('posts/<slug:slug>/comments/submit/', views.submit_comment, name='submit-comment'),
    path('', include(router.urls)),
]
