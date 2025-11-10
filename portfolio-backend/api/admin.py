from django.contrib import admin
from django.db.utils import OperationalError, ProgrammingError
from django.utils.html import format_html
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
    fieldsets = (
        ('Hero Section', {
            'fields': (
                'hero_name',
                'hero_tagline',
                'hero_bio',
                'hero_profile_image',
                'hero_resume_url',
            ),
            'description': 'Main hero section displayed at the top of the home page.'
        }),
        ('Hero Call-to-Action Buttons', {
            'fields': (
                ('hero_cta_primary_text', 'hero_cta_primary_url'),
                ('hero_cta_secondary_text', 'hero_cta_secondary_url'),
            ),
            'description': 'Primary and secondary CTA buttons in the hero section.'
        }),
        ('About Section', {
            'fields': (
                'about_title',
                'about_paragraphs',
                'about_highlights',
            ),
            'description': 'About section content. Use JSON format for paragraphs and highlights lists.'
        }),
        ('Stats Section', {
            'fields': (
                'stats_years_of_experience',
                'stats_projects_completed',
                'stats_publications',
                'stats_technologies_used',
            ),
            'description': 'Statistics displayed on the home page. Leave blank to hide a stat.'
        }),
        ('Skills Section', {
            'fields': (
                'skills_title',
                'skills_categories',
            ),
            'description': 'Skills section. skills_categories should be a JSON list with format: [{"name": "Category", "icon": "🔧", "skills": ["Skill1", "Skill2"]}]'
        }),
        ('Social Links', {
            'fields': (
                'social_email',
                'social_github',
                'social_linkedin',
                'social_twitter',
                'social_scholar',
            ),
            'description': 'Social media and contact links.'
        }),
        ('Bottom Call-to-Action Section', {
            'fields': (
                'cta_title',
                'cta_paragraph',
                ('cta_primary_text', 'cta_primary_url'),
                ('cta_secondary_text', 'cta_secondary_url'),
            ),
            'description': 'Final CTA section at the bottom of the home page.'
        }),
        ('Featured Sections Toggle', {
            'fields': (
                'show_experience',
                'show_education',
                'show_projects',
                'show_research',
                'show_blog',
            ),
            'description': 'Toggle which sections appear on the home page.'
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        })
    )

    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        # Only allow adding if no record exists (singleton)
        try:
            return not HomeData.objects.exists()
        except (OperationalError, ProgrammingError):
            return True  # Allow if table doesn't exist yet

    def has_delete_permission(self, request, obj=None):
        # Never allow deleting the home data
        return False


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


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = (
        'title_or_filename',
        'file_type',
        'file_preview',
        'slug',
        'file_size_display_field',
        'is_public',
        'uploaded_at',
        'copy_url_button'
    )

    list_filter = (
        'file_type',
        'is_public',
        'uploaded_at',
    )

    search_fields = (
        'slug',
        'title',
        'original_filename',
        'uuid',
    )

    readonly_fields = (
        'uuid',
        'original_filename',
        'file_size',
        'file_size_display_field',
        'uploaded_at',
        'updated_at',
        'file_preview_large',
        'cdn_url_display',
        'api_url_display'
    )

    ordering = ('-uploaded_at',)

    fieldsets = (
        ('File Upload', {
            'fields': ('file', 'file_type'),
            'description': 'Upload your file and select the appropriate type.'
        }),
        ('URL & Identification', {
            'fields': ('slug', 'uuid', 'cdn_url_display', 'api_url_display'),
            'description': 'Custom URL slug for accessing this file. Leave blank to auto-generate from UUID.'
        }),
        ('File Information', {
            'fields': ('original_filename', 'file_size', 'file_size_display_field', 'mime_type'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('title', 'alt_text'),
            'description': 'Optional metadata for better organization and accessibility.'
        }),
        ('Preview', {
            'fields': ('file_preview_large',),
            'description': 'Preview of the uploaded file (for images).'
        }),
        ('Access Control', {
            'fields': ('is_public',),
            'description': 'Control who can access this file.'
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    actions = ['make_public', 'make_private', 'copy_cdn_urls']

    def title_or_filename(self, obj):
        """Show title if available, otherwise show filename."""
        return obj.title if obj.title else obj.original_filename
    title_or_filename.short_description = "Title / Filename"

    def file_size_display_field(self, obj):
        """Show human-readable file size."""
        return obj.get_file_size_display()
    file_size_display_field.short_description = "File Size"

    def file_preview(self, obj):
        """Show thumbnail preview for images in list view."""
        if obj.file_type == 'image' and obj.file:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.get_file_url()
            )
        elif obj.file_type == 'video':
            return format_html('🎥')
        elif obj.file_type == 'audio':
            return format_html('🎵')
        elif obj.file_type == 'document':
            return format_html('📄')
        elif obj.file_type == 'archive':
            return format_html('📦')
        else:
            return format_html('📎')
    file_preview.short_description = "Preview"

    def file_preview_large(self, obj):
        """Show larger preview in detail view."""
        if obj.file_type == 'image' and obj.file:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.get_file_url()
            )
        elif obj.file_type == 'video' and obj.file:
            return format_html(
                '<video controls style="max-width: 400px; border-radius: 8px;"><source src="{}"></video>',
                obj.get_file_url()
            )
        elif obj.file_type == 'audio' and obj.file:
            return format_html(
                '<audio controls style="width: 400px;"><source src="{}"></audio>',
                obj.get_file_url()
            )
        else:
            return format_html('<p>Preview not available for this file type.</p>')
    file_preview_large.short_description = "File Preview"

    def cdn_url_display(self, obj):
        """Display the CDN URL with a copy button."""
        if obj.slug:
            url = obj.get_file_url()
            full_url = f"http://localhost:8000{url}"  # Update this with your domain
            return format_html(
                '<input type="text" value="{}" readonly style="width: 400px; padding: 4px;" '
                'onclick="this.select(); document.execCommand(\'copy\'); alert(\'URL copied!\');" /> '
                '<br><small>Click to copy</small>',
                full_url
            )
        return '-'
    cdn_url_display.short_description = "CDN URL"

    def api_url_display(self, obj):
        """Display the API URL."""
        if obj.slug:
            url = obj.get_api_url()
            full_url = f"http://localhost:8000{url}"  # Update this with your domain
            return format_html(
                '<input type="text" value="{}" readonly style="width: 400px; padding: 4px;" '
                'onclick="this.select(); document.execCommand(\'copy\'); alert(\'URL copied!\');" /> '
                '<br><small>Click to copy</small>',
                full_url
            )
        return '-'
    api_url_display.short_description = "API URL"

    def copy_url_button(self, obj):
        """Show a copy URL button in list view."""
        if obj.slug:
            url = obj.get_file_url()
            full_url = f"http://localhost:8000{url}"
            return format_html(
                '<button onclick="navigator.clipboard.writeText(\'{}\'); alert(\'URL copied!\');" '
                'style="padding: 4px 8px; cursor: pointer;">Copy URL</button>',
                full_url
            )
        return '-'
    copy_url_button.short_description = "Actions"

    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f'{updated} file(s) made public.')
    make_public.short_description = "Make selected files public"

    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f'{updated} file(s) made private.')
    make_private.short_description = "Make selected files private"

    def copy_cdn_urls(self, request, queryset):
        """Copy all CDN URLs to clipboard (via message)."""
        urls = [f"http://localhost:8000{obj.get_file_url()}" for obj in queryset]
        urls_text = '\n'.join(urls)
        self.message_user(request, f'CDN URLs:\n{urls_text}')
    copy_cdn_urls.short_description = "Show CDN URLs for selected files"