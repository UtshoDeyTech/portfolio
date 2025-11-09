from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from rest_framework import status as http_status

from .models import (
    EducationEntry,
    ExperienceEntry,
    Project,
    ResearchPublication,
    ResearchIcon,
    HomeData,
    Blog,
    BlogComment,
    BlogsData,
    BlogView,
    BlogLike,
)
from .serializers import (
    EducationEntrySerializer,
    ExperienceEntrySerializer,
    ProjectSerializer,
    ResearchPublicationSerializer,
    ResearchIconSerializer,
    HomeDataSerializer,
    BlogSerializer,
    BlogListSerializer,
    BlogCommentSerializer,
    BlogCommentCreateSerializer,
    BlogsDataSerializer,
)


class IndexView(APIView):
    """Return available endpoints / keys."""

    def get(self, request):
        keys = [
            'education',
            'experience',
            'projects',
            'research_publications',
            'research_icons',
            'home',
            'blogs',
            'blog-posts',
            'trending-blogs',
            'featured-blogs',
        ]
        return Response({'available': keys})


class EducationListView(generics.ListAPIView):
    queryset = EducationEntry.objects.all()
    serializer_class = EducationEntrySerializer


class EducationDetailView(generics.RetrieveAPIView):
    queryset = EducationEntry.objects.all()
    serializer_class = EducationEntrySerializer


class ExperienceListView(generics.ListAPIView):
    queryset = ExperienceEntry.objects.all()
    serializer_class = ExperienceEntrySerializer


class ExperienceDetailView(generics.RetrieveAPIView):
    queryset = ExperienceEntry.objects.all()
    serializer_class = ExperienceEntrySerializer


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'


class ResearchListView(generics.ListAPIView):
    queryset = ResearchPublication.objects.all()
    serializer_class = ResearchPublicationSerializer


class ResearchDetailView(generics.RetrieveAPIView):
    queryset = ResearchPublication.objects.all()
    serializer_class = ResearchPublicationSerializer
    lookup_field = 'slug'


class ResearchIconListView(generics.ListAPIView):
    queryset = ResearchIcon.objects.all()
    serializer_class = ResearchIconSerializer


class HomeDataView(generics.RetrieveAPIView):
    """
    Retrieve the singleton HomeData object.
    """
    queryset = HomeData.objects.all()
    serializer_class = HomeDataSerializer

    def get_object(self):
        """Return the first (and only) HomeData object."""
        return self.queryset.first()


class BlogListView(generics.ListAPIView):
    """
    List all published blogs.
    Uses lightweight serializer without full content.
    """
    serializer_class = BlogListSerializer

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).order_by('-published_date')


class BlogDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single blog by slug with full content (markdown converted to HTML).
    Note: Use the /increment-view/ endpoint to track views from frontend.
    """
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer
    lookup_field = 'slug'


class TrendingBlogsView(generics.ListAPIView):
    """
    List trending blogs.
    """
    serializer_class = BlogListSerializer

    def get_queryset(self):
        return Blog.objects.filter(
            is_published=True,
            is_trending=True
        ).order_by('-views', '-published_date')


class FeaturedBlogsView(generics.ListAPIView):
    """
    List featured blogs.
    """
    serializer_class = BlogListSerializer

    def get_queryset(self):
        return Blog.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('-published_date')


class BlogsByCategoryView(generics.ListAPIView):
    """
    List blogs by category.
    """
    serializer_class = BlogListSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Blog.objects.filter(
            is_published=True,
            category=category
        ).order_by('-published_date')


class BlogsDataView(generics.RetrieveAPIView):
    """
    Retrieve the singleton BlogsData object.
    """
    queryset = BlogsData.objects.all()
    serializer_class = BlogsDataSerializer

    def get_object(self):
        """Return the first (and only) BlogsData object."""
        return self.queryset.first()


class BlogIncrementViewAPIView(APIView):
    """
    Increment view count for a blog post using device fingerprint.
    POST /api/blog-posts/<slug>/increment-view/

    Request body:
    {
        "fingerprint": "fp_abc123...",
        "session_id": "session_xyz..."
    }

    Only counts unique views per fingerprint (prevents duplicate views from same device).
    """
    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_published=True)

        # Get fingerprint from request
        fingerprint = request.data.get('fingerprint', '')
        session_id = request.data.get('session_id', '')

        if not fingerprint:
            return Response({
                'success': False,
                'message': 'Fingerprint is required',
                'views': blog.views
            }, status=http_status.HTTP_400_BAD_REQUEST)

        # Get client IP and user agent
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Check if this fingerprint has already viewed this blog
        view_record, created = BlogView.objects.get_or_create(
            blog=blog,
            fingerprint=fingerprint,
            defaults={
                'session_id': session_id,
                'ip_address': ip_address,
                'user_agent': user_agent,
            }
        )

        if created:
            # This is a new unique view, increment the counter
            blog.views += 1
            blog.save(update_fields=['views'])
            message = 'View count incremented'
        else:
            # This fingerprint has already viewed this blog
            message = 'View already counted for this device'

        return Response({
            'success': True,
            'message': message,
            'views': blog.views,
            'is_new_view': created
        }, status=http_status.HTTP_200_OK)

    @staticmethod
    def get_client_ip(request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class BlogLikeToggleAPIView(APIView):
    """
    Toggle like for a blog post using device fingerprint.
    POST /api/blog-posts/<slug>/toggle-like/

    Request body:
    {
        "action": "like" or "unlike",
        "fingerprint": "fp_abc123..."
    }

    Only allows one like per fingerprint (prevents duplicate likes from same device).
    """
    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_published=True)

        # Get fingerprint from request
        fingerprint = request.data.get('fingerprint', '')
        action = request.data.get('action', 'like')

        if not fingerprint:
            return Response({
                'success': False,
                'message': 'Fingerprint is required',
                'likes': blog.likes
            }, status=http_status.HTTP_400_BAD_REQUEST)

        if action not in ['like', 'unlike']:
            return Response({
                'success': False,
                'message': 'Invalid action. Use "like" or "unlike"'
            }, status=http_status.HTTP_400_BAD_REQUEST)

        # Get client IP and user agent
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Get or create like record for this fingerprint
        like_record, created = BlogLike.objects.get_or_create(
            blog=blog,
            fingerprint=fingerprint,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'is_active': (action == 'like')
            }
        )

        if action == 'like':
            if created:
                # New like
                blog.likes += 1
                message = 'Blog liked'
                is_liked = True
            elif not like_record.is_active:
                # Re-liking after unliking
                like_record.is_active = True
                like_record.save(update_fields=['is_active'])
                blog.likes += 1
                message = 'Blog liked'
                is_liked = True
            else:
                # Already liked
                message = 'Already liked by this device'
                is_liked = True

        else:  # action == 'unlike'
            if like_record.is_active:
                # Unliking
                like_record.is_active = False
                like_record.save(update_fields=['is_active'])
                blog.likes = max(0, blog.likes - 1)  # Prevent negative likes
                message = 'Blog unliked'
                is_liked = False
            else:
                # Already unliked
                message = 'Not currently liked'
                is_liked = False

        blog.save(update_fields=['likes'])

        return Response({
            'success': True,
            'message': message,
            'likes': blog.likes,
            'is_liked': is_liked
        }, status=http_status.HTTP_200_OK)

    @staticmethod
    def get_client_ip(request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class BlogCommentCreateAPIView(generics.CreateAPIView):
    """
    Create a new comment on a blog post.
    POST /api/blog-posts/<slug>/comments/

    Request body:
    {
        "author_name": "John Doe",
        "author_email": "john@example.com",
        "comment_text": "Great article!"
    }
    """
    serializer_class = BlogCommentCreateSerializer

    def create(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blog, slug=slug, is_published=True)

        # Check if blog allows comments
        if not blog.allow_comments:
            return Response({
                'success': False,
                'message': 'Comments are disabled for this blog'
            }, status=http_status.HTTP_403_FORBIDDEN)

        # Add blog to the request data
        data = request.data.copy()
        data['blog'] = blog.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        # Increment comment count on blog
        blog.comments_count += 1
        blog.save(update_fields=['comments_count'])

        return Response({
            'success': True,
            'message': 'Comment added successfully',
            'comment': serializer.data
        }, status=http_status.HTTP_201_CREATED)


class BlogCommentsListAPIView(generics.ListAPIView):
    """
    Get all approved comments for a specific blog post.
    GET /api/blog-posts/<slug>/comments/
    """
    serializer_class = BlogCommentSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blog, slug=slug, is_published=True)
        # Only return approved comments
        return BlogComment.objects.filter(blog=blog, is_approved=True).order_by('-created_at')
