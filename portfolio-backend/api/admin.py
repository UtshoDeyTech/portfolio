from django.contrib import admin
from django.db.utils import OperationalError, ProgrammingError
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
)


@admin.register(EducationEntry)
class EducationEntryAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current', 'display_order')
    list_filter = ('is_current', 'is_visible', 'education_type')
    search_fields = ('institution', 'degree', 'field_of_study')
    ordering = ('display_order', '-start_date')


@admin.register(ExperienceEntry)
class ExperienceEntryAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'role', 'employment_type', 'start_date', 'end_date', 'is_current', 'display_order')
    list_filter = ('is_current', 'is_visible', 'employment_type', 'work_mode')
    search_fields = ('company_name', 'role', 'description')
    ordering = ('display_order', '-start_date')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'type', 'start_date', 'end_date', 'is_visible', 'display_order')
    list_filter = ('is_visible', 'type')
    search_fields = ('title', 'organization', 'short_description', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('display_order',)


@admin.register(ResearchPublication)
class ResearchPublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_type', 'publication_date', 'is_visible', 'display_order')
    list_filter = ('is_visible', 'publication_type')
    search_fields = ('title', 'description', 'authors', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('display_order',)


@admin.register(ResearchIcon)
class ResearchIconAdmin(admin.ModelAdmin):
    list_display = ('key', 'title')
    search_fields = ('key', 'title')


@admin.register(HomeData)
class HomeDataAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        try:
            return not HomeData.objects.exists()
        except (OperationalError, ProgrammingError):
            return True  # Allow if table doesn't exist yet


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'is_published',
        'is_trending',
        'is_featured',
        'views',
        'published_date',
        'display_order'
    )

    list_filter = (
        'is_published',
        'is_trending',
        'is_featured',
        'is_editor_choice',
        'category',
        'allow_comments',
        'published_date',
        'created_at'
    )

    search_fields = (
        'title',
        'subtitle',
        'excerpt',
        'content_markdown',
        'author',
        'tags',
        'category'
    )

    prepopulated_fields = {'slug': ('title',)}

    ordering = ('-published_date', 'display_order')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'slug', 'excerpt', 'author')
        }),
        ('Content', {
            'fields': ('content_markdown',),
            'description': 'Write your blog content in Markdown format. It will be converted to HTML via API.'
        }),
        ('Media', {
            'fields': ('cover_image', 'featured_image'),
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Publishing', {
            'fields': ('published_date', 'is_published')
        }),
        ('Control & Features', {
            'fields': (
                'is_trending',
                'is_featured',
                'is_editor_choice',
                'allow_comments',
                'display_order'
            )
        }),
        ('Engagement Metrics', {
            'fields': ('views', 'likes', 'comments_count', 'shares'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('read_time', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    # Add action to mark blogs as trending
    actions = ['mark_as_trending', 'unmark_as_trending', 'publish_blogs', 'unpublish_blogs']

    def mark_as_trending(self, request, queryset):
        updated = queryset.update(is_trending=True)
        self.message_user(request, f'{updated} blog(s) marked as trending.')
    mark_as_trending.short_description = "Mark selected blogs as trending"

    def unmark_as_trending(self, request, queryset):
        updated = queryset.update(is_trending=False)
        self.message_user(request, f'{updated} blog(s) unmarked as trending.')
    unmark_as_trending.short_description = "Unmark selected blogs as trending"

    def publish_blogs(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} blog(s) published.')
    publish_blogs.short_description = "Publish selected blogs"

    def unpublish_blogs(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} blog(s) unpublished.')
    unpublish_blogs.short_description = "Unpublish selected blogs"


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = (
        'author_name',
        'blog',
        'comment_text_preview',
        'created_at',
        'is_approved'
    )

    list_filter = (
        'is_approved',
        'created_at',
        'blog'
    )

    search_fields = (
        'author_name',
        'author_email',
        'comment_text',
        'blog__title'
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Comment Information', {
            'fields': ('blog', 'author_name', 'author_email', 'comment_text')
        }),
        ('Moderation', {
            'fields': ('is_approved',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    actions = ['approve_comments', 'unapprove_comments']

    def comment_text_preview(self, obj):
        """Show preview of comment text in list view."""
        return obj.comment_text[:50] + '...' if len(obj.comment_text) > 50 else obj.comment_text
    comment_text_preview.short_description = "Comment Preview"

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comment(s) approved.')
    approve_comments.short_description = "Approve selected comments"

    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comment(s) hidden.')
    unapprove_comments.short_description = "Hide selected comments"


@admin.register(BlogsData)
class BlogsDataAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        try:
            return not BlogsData.objects.exists()
        except (OperationalError, ProgrammingError):
            return True  # Allow if table doesn't exist yet


@admin.register(BlogSettings)
class BlogSettingsAdmin(admin.ModelAdmin):
    list_display = ('duration_update_interval', 'inactivity_threshold', 'updated_at')

    fieldsets = (
        ('Time Tracking Settings', {
            'fields': ('duration_update_interval', 'inactivity_threshold'),
            'description': 'Configure how blog post time tracking behaves.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        # Only allow adding if no settings exist
        try:
            return not BlogSettings.objects.exists()
        except (OperationalError, ProgrammingError):
            return True

    def has_delete_permission(self, request, obj=None):
        # Never allow deleting the settings
        return False


@admin.register(BlogView)
class BlogViewAdmin(admin.ModelAdmin):
    list_display = (
        'blog',
        'fingerprint_preview',
        'viewed_date',
        'duration_display',
        'last_seen',
        'ip_address'
    )

    list_filter = (
        'viewed_date',
        'viewed_at',
        'last_seen',
        'blog'
    )

    search_fields = (
        'fingerprint',
        'session_id',
        'ip_address',
        'blog__title'
    )

    readonly_fields = ('blog', 'fingerprint', 'session_id', 'ip_address', 'user_agent', 'viewed_at', 'viewed_date', 'last_seen', 'duration_seconds', 'duration_display')

    ordering = ('-viewed_date', '-viewed_at')

    def duration_display(self, obj):
        """Show human-readable duration."""
        return obj.get_duration_display()
    duration_display.short_description = "Time Spent"

    def has_add_permission(self, request):
        return False  # Views are created automatically

    def fingerprint_preview(self, obj):
        """Show preview of fingerprint."""
        return obj.fingerprint[:30] + '...' if len(obj.fingerprint) > 30 else obj.fingerprint
    fingerprint_preview.short_description = "Fingerprint"

    def session_id_preview(self, obj):
        """Show preview of session ID."""
        if not obj.session_id:
            return '-'
        return obj.session_id[:30] + '...' if len(obj.session_id) > 30 else obj.session_id
    session_id_preview.short_description = "Session ID"


@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = (
        'blog',
        'fingerprint_preview',
        'ip_address',
        'is_active',
        'liked_at'
    )

    list_filter = (
        'is_active',
        'liked_at',
        'blog'
    )

    search_fields = (
        'fingerprint',
        'ip_address',
        'blog__title'
    )

    readonly_fields = ('blog', 'fingerprint', 'ip_address', 'user_agent', 'liked_at')

    ordering = ('-liked_at',)

    def has_add_permission(self, request):
        return False  # Likes are created automatically

    def fingerprint_preview(self, obj):
        """Show preview of fingerprint."""
        return obj.fingerprint[:30] + '...' if len(obj.fingerprint) > 30 else obj.fingerprint
    fingerprint_preview.short_description = "Fingerprint"