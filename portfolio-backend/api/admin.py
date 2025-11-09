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