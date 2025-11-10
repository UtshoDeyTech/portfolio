from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import FileResponse, Http404
import mimetypes
import os

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
    BlogSettings,
    BlogView,
    BlogLike,
    MediaFile,
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
    MediaFileSerializer,
    MediaFileListSerializer,
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


class BlogSettingsView(APIView):
    """
    GET /api/blog-settings/
    Returns blog configuration settings (duration update interval, etc.).
    """
    def get(self, request):
        settings = BlogSettings.get_settings()
        return Response({
            'duration_update_interval': settings.duration_update_interval,
            'inactivity_threshold': settings.inactivity_threshold,
        }, status=http_status.HTTP_200_OK)


class BlogIncrementViewAPIView(APIView):
    """
    Increment view count for a blog post using device fingerprint.
    POST /api/blog-posts/<slug>/increment-view/

    Request body:
    {
        "fingerprint": "fp_abc123...",
        "session_id": "session_xyz..."
    }

    Counts one view per device per day (resets daily for better analytics).
    Same device viewing on different days will increment the view count.
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

        # Get today's date
        today = timezone.now().date()

        # Check if this fingerprint has already viewed this blog TODAY
        view_record, created = BlogView.objects.get_or_create(
            blog=blog,
            fingerprint=fingerprint,
            viewed_date=today,
            defaults={
                'session_id': session_id,
                'ip_address': ip_address,
                'user_agent': user_agent,
            }
        )

        if created:
            # This is a new view for today, increment the counter
            blog.views += 1
            blog.save(update_fields=['views'])
            message = 'View count incremented'
        else:
            # This fingerprint has already viewed this blog today
            message = 'View already counted for this device today'

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


class BlogUpdateDurationAPIView(APIView):
    """
    Update time spent on a blog post.
    POST /api/blog-posts/<slug>/update-duration/

    Request body:
    {
        "fingerprint": "fp_abc123...",
        "duration": 45  // seconds spent on this visit
    }

    Accumulates total time spent and updates last_seen timestamp.
    """
    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_published=True)

        # Get fingerprint and duration from request
        fingerprint = request.data.get('fingerprint', '')
        duration = request.data.get('duration', 0)

        if not fingerprint:
            return Response({
                'success': False,
                'message': 'Fingerprint is required'
            }, status=http_status.HTTP_400_BAD_REQUEST)

        try:
            duration = int(duration)
            if duration < 0:
                duration = 0
        except (ValueError, TypeError):
            duration = 0

        # Get today's date
        today = timezone.now().date()

        # Try to get today's view record for this fingerprint
        try:
            view_record = BlogView.objects.get(
                blog=blog,
                fingerprint=fingerprint,
                viewed_date=today
            )

            # Update duration and last_seen (last_seen auto-updates with save())
            view_record.duration_seconds += duration
            view_record.save()

            return Response({
                'success': True,
                'message': 'Duration updated',
                'total_duration': view_record.duration_seconds,
                'total_duration_display': view_record.get_duration_display(),
                'last_seen': view_record.last_seen.isoformat()
            }, status=http_status.HTTP_200_OK)

        except BlogView.DoesNotExist:
            # No view record for today, can't update duration
            return Response({
                'success': False,
                'message': 'No view record found for today'
            }, status=http_status.HTTP_404_NOT_FOUND)

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


class BlogViewStatsAPIView(APIView):
    """
    Get user's view statistics for a specific blog post.
    GET /api/blog-posts/<slug>/view-stats/?fingerprint=<fingerprint>

    Returns:
    {
        "first_viewed_at": "2024-01-15T10:30:00Z",
        "last_seen": "2024-01-15T11:45:00Z",
        "total_duration": 450,
        "total_duration_display": "7m 30s",
        "viewed_date": "2024-01-15",
        "has_viewed": true
    }
    """
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_published=True)

        # Get fingerprint from query params
        fingerprint = request.GET.get('fingerprint', '')

        if not fingerprint:
            return Response({
                'success': False,
                'message': 'Fingerprint is required',
                'has_viewed': False
            }, status=http_status.HTTP_400_BAD_REQUEST)

        # Get today's date
        today = timezone.now().date()

        # Try to get today's view record for this fingerprint
        try:
            view_record = BlogView.objects.get(
                blog=blog,
                fingerprint=fingerprint,
                viewed_date=today
            )

            return Response({
                'success': True,
                'has_viewed': True,
                'first_viewed_at': view_record.viewed_at.isoformat(),
                'last_seen': view_record.last_seen.isoformat(),
                'total_duration': view_record.duration_seconds,
                'total_duration_display': view_record.get_duration_display(),
                'viewed_date': view_record.viewed_date.isoformat()
            }, status=http_status.HTTP_200_OK)

        except BlogView.DoesNotExist:
            # No view record for today
            return Response({
                'success': True,
                'has_viewed': False,
                'message': 'No view record found for today'
            }, status=http_status.HTTP_200_OK)


class MediaFileListView(generics.ListAPIView):
    """
    List all media files.
    GET /api/media-files/

    Query parameters:
    - file_type: Filter by file type (image, audio, video, document, archive, other)
    """
    serializer_class = MediaFileListSerializer

    def get_queryset(self):
        queryset = MediaFile.objects.filter(is_public=True)

        # Filter by file type if provided
        file_type = self.request.query_params.get('file_type', None)
        if file_type:
            queryset = queryset.filter(file_type=file_type)

        return queryset.order_by('-uploaded_at')


class MediaFileDetailView(generics.RetrieveAPIView):
    """
    Get details of a specific media file by slug or UUID.
    GET /api/media-files/{slug_or_uuid}/
    """
    serializer_class = MediaFileSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return MediaFile.objects.filter(is_public=True)

    def get_object(self):
        """
        Allow lookup by either slug or UUID.
        """
        lookup_value = self.kwargs.get(self.lookup_field)

        try:
            # Try to get by slug first
            return self.get_queryset().get(slug=lookup_value)
        except MediaFile.DoesNotExist:
            # Try to get by UUID
            try:
                return self.get_queryset().get(uuid=lookup_value)
            except (MediaFile.DoesNotExist, ValueError):
                raise Http404("Media file not found")


class ServeMediaFileView(APIView):
    """
    Serve media files through a secure endpoint.
    GET /cdn/{slug}

    This endpoint serves files without exposing the direct file path.
    Files are served with appropriate content-type headers.
    """
    def get(self, request, slug):
        # Get media file by slug or UUID
        try:
            media_file = MediaFile.objects.get(slug=slug)
        except MediaFile.DoesNotExist:
            # Try by UUID
            try:
                media_file = MediaFile.objects.get(uuid=slug)
            except (MediaFile.DoesNotExist, ValueError):
                raise Http404("File not found")

        # Check if file is public (optional: add authentication check here)
        if not media_file.is_public:
            # TODO: Add authentication check
            return Response({
                'success': False,
                'message': 'File is not public'
            }, status=http_status.HTTP_403_FORBIDDEN)

        # Check if file exists
        if not media_file.file:
            raise Http404("File not found")

        try:
            # Open the file
            file_handle = media_file.file.open('rb')

            # Determine MIME type
            mime_type = media_file.mime_type
            if not mime_type:
                # Guess MIME type from file extension
                mime_type, _ = mimetypes.guess_type(media_file.file.path)
                if not mime_type:
                    mime_type = 'application/octet-stream'

            # Create file response
            response = FileResponse(file_handle, content_type=mime_type)

            # Set content disposition (inline for display, attachment for download)
            # Images, videos, audio should be inline; others should be attachment
            if media_file.file_type in ['image', 'video', 'audio']:
                response['Content-Disposition'] = f'inline; filename="{media_file.original_filename}"'
            else:
                response['Content-Disposition'] = f'attachment; filename="{media_file.original_filename}"'

            # Set cache headers (optional - cache for 1 day)
            response['Cache-Control'] = 'public, max-age=86400'

            return response

        except Exception as e:
            raise Http404(f"Error serving file: {str(e)}")
