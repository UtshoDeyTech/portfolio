from rest_framework import serializers
import markdown
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
    MediaFile,
)


class EducationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationEntry
        fields = '__all__'


class ExperienceEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceEntry
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ResearchPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchPublication
        fields = '__all__'


class ResearchIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchIcon
        fields = '__all__'


class HomeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeData
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model with markdown to HTML conversion.
    The 'content_html' field is automatically generated from 'content_markdown'.
    """
    content_html = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'slug',
            'title',
            'subtitle',
            'excerpt',
            'content_markdown',
            'content_html',  # Generated field
            'cover_image',
            'featured_image',
            'category',
            'tags',
            'author',
            'published_date',
            'created_at',
            'updated_at',
            'views',
            'likes',
            'comments_count',
            'shares',
            'is_published',
            'is_featured',
            'is_trending',
            'is_editor_choice',
            'allow_comments',
            'display_order',
            'read_time',
            'meta_description',
            'meta_keywords',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'content_html']

    def get_content_html(self, obj):
        """
        Convert markdown content to HTML.
        Uses Python-Markdown with extensions for better formatting.
        """
        md = markdown.Markdown(extensions=[
            'extra',  # Includes tables, fenced code blocks, etc.
            'codehilite',  # Syntax highlighting for code blocks
            'toc',  # Table of contents
            'nl2br',  # Convert newlines to <br>
        ])
        return md.convert(obj.content_markdown)


class BlogListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for blog list views.
    Excludes full content for better performance.
    """
    class Meta:
        model = Blog
        fields = [
            'id',
            'slug',
            'title',
            'subtitle',
            'excerpt',
            'cover_image',
            'category',
            'tags',
            'author',
            'published_date',
            'views',
            'likes',
            'comments_count',
            'is_trending',
            'is_featured',
            'read_time',
        ]


class BlogCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for blog comments.
    """
    class Meta:
        model = BlogComment
        fields = [
            'id',
            'blog',
            'author_name',
            'author_email',
            'comment_text',
            'created_at',
            'updated_at',
            'is_approved'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_approved']


class BlogCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating blog comments (hides email in response).
    """
    class Meta:
        model = BlogComment
        fields = [
            'id',
            'blog',
            'author_name',
            'author_email',
            'comment_text',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'author_email': {'write_only': True}
        }


class BlogsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogsData
        fields = '__all__'


class SectionSerializer(serializers.Serializer):
    class Meta:
        fields = ()


class MediaFileSerializer(serializers.ModelSerializer):
    """
    Serializer for MediaFile model.
    Provides file URL, size display, and metadata.
    """
    file_url = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()
    file_size_display = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = [
            'id',
            'uuid',
            'slug',
            'file_type',
            'original_filename',
            'file_size',
            'file_size_display',
            'file_extension',
            'mime_type',
            'title',
            'alt_text',
            'file_url',
            'api_url',
            'is_public',
            'uploaded_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'uuid', 'file_size', 'original_filename', 'uploaded_at', 'updated_at']

    def get_file_url(self, obj):
        """Returns the CDN URL for accessing this file."""
        return obj.get_file_url()

    def get_api_url(self, obj):
        """Returns the API URL for accessing this file."""
        return obj.get_api_url()

    def get_file_size_display(self, obj):
        """Returns human-readable file size."""
        return obj.get_file_size_display()

    def get_file_extension(self, obj):
        """Returns the file extension."""
        return obj.get_file_extension()


class MediaFileListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing media files.
    """
    file_url = serializers.SerializerMethodField()
    file_size_display = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = [
            'id',
            'uuid',
            'slug',
            'file_type',
            'original_filename',
            'file_size_display',
            'file_extension',
            'title',
            'file_url',
            'uploaded_at',
        ]

    def get_file_url(self, obj):
        return obj.get_file_url()

    def get_file_size_display(self, obj):
        return obj.get_file_size_display()

    def get_file_extension(self, obj):
        return obj.get_file_extension()
