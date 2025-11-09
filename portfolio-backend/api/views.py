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
    Increment view count for a blog post.
    POST /api/blog-posts/<slug>/increment-view/
    """
    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_published=True)
        blog.views += 1
        blog.save(update_fields=['views'])
        return Response({
            'success': True,
            'message': 'View count incremented',
            'views': blog.views
        }, status=http_status.HTTP_200_OK)


class BlogLikeToggleAPIView(APIView):
    """
    Toggle like for a blog post.
    POST /api/blog-posts/<slug>/toggle-like/

    Request body: { "action": "like" } or { "action": "unlike" }
    """
    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_published=True)
        action = request.data.get('action', 'like')

        if action == 'like':
            blog.likes += 1
            message = 'Blog liked'
        elif action == 'unlike':
            blog.likes = max(0, blog.likes - 1)  # Prevent negative likes
            message = 'Blog unliked'
        else:
            return Response({
                'success': False,
                'message': 'Invalid action. Use "like" or "unlike"'
            }, status=http_status.HTTP_400_BAD_REQUEST)

        blog.save(update_fields=['likes'])
        return Response({
            'success': True,
            'message': message,
            'likes': blog.likes
        }, status=http_status.HTTP_200_OK)


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
