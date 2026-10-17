from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Category, Tag, BlogPost, Comment
from .serializers import (
    CategorySerializer, TagSerializer,
    BlogPostListSerializer, BlogPostDetailSerializer, BlogPostAdminSerializer,
    CommentSerializer, CommentAdminSerializer
)


class CommentThrottle(AnonRateThrottle):
    rate = '10/hour'
    scope = 'comment'


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, 'is_owner', False)
        )


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class PublicBlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """Public blog post listing — only published posts visible."""
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'tags__slug', 'is_featured']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'views', 'published_at']
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('category').prefetch_related('tags')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        BlogPost.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        instance.views += 1
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AdminBlogPostViewSet(viewsets.ModelViewSet):
    """Owner-only blog post management — all statuses visible."""
    serializer_class = BlogPostAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_featured', 'category']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'views']
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, 'is_owner', False):
            return BlogPost.objects.all().select_related('category').prefetch_related('tags')
        return BlogPost.objects.none()

    def perform_create(self, serializer):
        data = {}
        if serializer.validated_data.get('status') == 'published' and not serializer.validated_data.get('published_at'):
            data['published_at'] = timezone.now()
        serializer.save(**data)

    def perform_update(self, serializer):
        data = {}
        if (serializer.validated_data.get('status') == 'published' and
                not serializer.instance.published_at):
            data['published_at'] = timezone.now()
        serializer.save(**data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def post_comments(request, slug):
    """GET: list approved comments for a published post."""
    try:
        post = BlogPost.objects.get(slug=slug, status='published')
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    comments = post.comments.filter(is_approved=True)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([CommentThrottle])
def submit_comment(request, slug):
    """POST: submit a new comment (goes to moderation queue)."""
    try:
        post = BlogPost.objects.get(slug=slug, status='published')
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(post=post)
    return Response(
        {'detail': 'Comment submitted and awaiting moderation. Thank you!'},
        status=status.HTTP_201_CREATED
    )


class AdminCommentViewSet(viewsets.ModelViewSet):
    """Owner-only comment moderation."""
    serializer_class = CommentAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_approved', 'post']
    search_fields = ['name', 'email', 'body']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, 'is_owner', False):
            return Comment.objects.all().select_related('post')
        return Comment.objects.none()
