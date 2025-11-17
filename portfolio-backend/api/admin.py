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
    BackupRestore,
    NewsletterSubscriber,
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
    change_form_template = 'admin/homedata_change_form.html'

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
    change_form_template = 'admin/blog_change_form.html'

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

    def get_urls(self):
        """Add custom URLs for download/upload JSON and preview."""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:object_id>/download-json/',
                self.admin_site.admin_view(self.download_json_view),
                name='api_blog_download_json',
            ),
            path(
                '<int:object_id>/upload-json/',
                self.admin_site.admin_view(self.upload_json_view),
                name='api_blog_upload_json',
            ),
            path(
                '<int:object_id>/preview/',
                self.admin_site.admin_view(self.preview_blog_view),
                name='api_blog_preview',
            ),
        ]
        return custom_urls + urls

    def download_json_view(self, request, object_id):
        """Download blog content as JSON."""
        from django.http import JsonResponse, HttpResponse
        import json
        from django.core.serializers.json import DjangoJSONEncoder

        try:
            blog = Blog.objects.get(pk=object_id)

            # Create a dictionary with all blog fields
            blog_data = {
                'slug': blog.slug,
                'title': blog.title,
                'subtitle': blog.subtitle,
                'excerpt': blog.excerpt,
                'content_markdown': blog.content_markdown,
                'cover_image': blog.cover_image,
                'featured_image': blog.featured_image,
                'category': blog.category,
                'tags': blog.tags,
                'author': blog.author,
                'published_date': blog.published_date.isoformat() if blog.published_date else None,
                'views': blog.views,
                'likes': blog.likes,
                'comments_count': blog.comments_count,
                'shares': blog.shares,
                'is_published': blog.is_published,
                'is_featured': blog.is_featured,
                'is_trending': blog.is_trending,
                'is_editor_choice': blog.is_editor_choice,
                'allow_comments': blog.allow_comments,
                'display_order': blog.display_order,
                'read_time': blog.read_time,
                'meta_description': blog.meta_description,
                'meta_keywords': blog.meta_keywords,
            }

            # Create JSON response
            response = HttpResponse(
                json.dumps(blog_data, indent=2, cls=DjangoJSONEncoder),
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="blog_{blog.slug}_{blog.id}.json"'
            return response

        except Blog.DoesNotExist:
            return JsonResponse({'error': 'Blog not found'}, status=404)

    def upload_json_view(self, request, object_id):
        """Update blog content from uploaded JSON."""
        from django.http import JsonResponse
        from django.shortcuts import redirect
        from django.contrib import messages
        from django.urls import reverse
        import json
        from datetime import datetime

        if request.method != 'POST':
            return JsonResponse({'error': 'Only POST method allowed'}, status=405)

        try:
            blog = Blog.objects.get(pk=object_id)

            # Get uploaded file
            if 'json_file' not in request.FILES:
                messages.error(request, 'No JSON file uploaded.')
                return redirect(reverse('admin:api_blog_change', args=[object_id]))

            json_file = request.FILES['json_file']

            # Read and parse JSON
            try:
                json_data = json.loads(json_file.read().decode('utf-8'))
            except json.JSONDecodeError as e:
                messages.error(request, f'Invalid JSON file: {str(e)}')
                return redirect(reverse('admin:api_blog_change', args=[object_id]))

            # Update blog fields from JSON
            updateable_fields = [
                'slug', 'title', 'subtitle', 'excerpt', 'content_markdown',
                'cover_image', 'featured_image', 'category', 'tags', 'author',
                'views', 'likes', 'comments_count', 'shares',
                'is_published', 'is_featured', 'is_trending', 'is_editor_choice',
                'allow_comments', 'display_order', 'read_time',
                'meta_description', 'meta_keywords'
            ]

            updated_fields = []
            for field in updateable_fields:
                if field in json_data:
                    # Handle published_date separately (datetime field)
                    if field == 'published_date':
                        continue
                    setattr(blog, field, json_data[field])
                    updated_fields.append(field)

            # Handle published_date separately
            if 'published_date' in json_data and json_data['published_date']:
                try:
                    blog.published_date = datetime.fromisoformat(json_data['published_date'].replace('Z', '+00:00'))
                    updated_fields.append('published_date')
                except (ValueError, AttributeError):
                    messages.warning(request, 'Could not parse published_date from JSON.')

            blog.save()

            messages.success(
                request,
                f'Blog updated successfully! Updated fields: {", ".join(updated_fields)}'
            )
            return redirect(reverse('admin:api_blog_change', args=[object_id]))

        except Blog.DoesNotExist:
            messages.error(request, 'Blog not found.')
            return redirect(reverse('admin:api_blog_changelist'))
        except Exception as e:
            messages.error(request, f'Error updating blog: {str(e)}')
            return redirect(reverse('admin:api_blog_change', args=[object_id]))

    def preview_blog_view(self, request, object_id):
        """Preview blog post by redirecting to the actual frontend page."""
        from django.shortcuts import get_object_or_404, redirect
        from django.contrib import messages

        try:
            blog = get_object_or_404(Blog, pk=object_id)

            # Get the frontend URL
            frontend_url = request.build_absolute_uri('/').rstrip('/')

            if blog.is_published:
                # Redirect to the actual frontend blog page (same page users see)
                preview_url = f"{frontend_url}/blog/{blog.slug}"
                return redirect(preview_url)
            else:
                # For unpublished posts, show helpful message
                messages.warning(
                    request,
                    f'📝 This blog post is UNPUBLISHED. To preview it: '
                    f'1) Mark as "Published", 2) Save, 3) Run deployment to rebuild frontend, '
                    f'4) Then click preview. Or keep it unpublished and preview after publishing.'
                )
                # Redirect back to the change form
                from django.urls import reverse
                return redirect(reverse('admin:api_blog_change', args=[object_id]))

        except Blog.DoesNotExist:
            from django.http import Http404
            raise Http404("Blog not found")


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
        'file_size_display_field',
        'is_public',
        'uploaded_at',
        'copy_url_button',
        'view_file_link'
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
        'mime_type',
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
        if not obj or not obj.pk:
            return '-'
        try:
            return obj.title if obj.title else obj.original_filename
        except Exception:
            return '-'
    title_or_filename.short_description = "Title / Filename"

    def file_size_display_field(self, obj):
        """Show human-readable file size."""
        if not obj or not obj.pk:
            return '-'
        try:
            return obj.get_file_size_display()
        except Exception:
            return '-'
    file_size_display_field.short_description = "File Size"

    def file_preview(self, obj):
        """Show thumbnail preview for images in list view."""
        if not obj or not obj.pk:
            return '-'

        try:
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
        except Exception:
            return '-'
    file_preview.short_description = "Preview"

    def file_preview_large(self, obj):
        """Show larger preview in detail view."""
        if not obj or not obj.pk:
            return format_html('<p style="color: #666; font-style: italic;">Preview will be available after saving</p>')

        try:
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
        except Exception:
            return format_html('<p style="color: #999;">Error loading preview</p>')
    file_preview_large.short_description = "File Preview"

    def cdn_url_display(self, obj):
        """Display the CDN URL with a copy button."""
        # Check if object has been saved (has an ID)
        if not obj or not obj.pk:
            return format_html('<p style="color: #666; font-style: italic;">URL will be available after saving</p>')

        try:
            if obj.slug:
                url = obj.get_file_url()
                # Use JavaScript to construct absolute URL and provide copy functionality
                return format_html(
                    '<div style="display: flex; gap: 8px; align-items: center;">'
                    '<input type="text" id="cdn_url_{}" readonly style="width: 400px; padding: 4px; font-family: monospace;" />'
                    '<button type="button" onclick="'
                    'var input = document.getElementById(\'cdn_url_{}\'); '
                    'navigator.clipboard.writeText(input.value).then(() => {{ '
                    'alert(\'✓ URL copied: \' + input.value); '
                    '}}).catch(() => {{ alert(\'Failed to copy URL\'); }});" '
                    'style="padding: 4px 12px; cursor: pointer; background: #417690; color: white; border: none; border-radius: 4px;">'
                    'Copy</button>'
                    '</div>'
                    '<script>document.getElementById("cdn_url_{}").value = window.location.protocol + "//" + window.location.host + "{}";</script>',
                    obj.id, obj.id, obj.id, url
                )
            return '-'
        except Exception:
            return format_html('<p style="color: #999;">Error generating URL</p>')
    cdn_url_display.short_description = "CDN URL"

    def api_url_display(self, obj):
        """Display the API URL (same as CDN URL for compatibility)."""
        return self.cdn_url_display(obj)
    api_url_display.short_description = "API URL"

    def copy_url_button(self, obj):
        """Show the CDN URL with a copy button in list view."""
        if not obj or not obj.pk or not obj.slug:
            return '-'

        try:
            url = obj.get_file_url()
            # Create an ID for this specific button
            button_id = f"url_{obj.id}"
            # Show URL text and copy button
            return format_html(
                '<div style="display: flex; gap: 4px; align-items: center;">'
                '<code id="{}" style="font-size: 11px; padding: 2px 4px; background: #f0f0f0; border-radius: 2px;"></code>'
                '<button onclick="'
                'var urlElem = document.getElementById(\'{}\'); '
                'navigator.clipboard.writeText(urlElem.textContent).then(() => {{ '
                'alert(\'✓ URL copied: \' + urlElem.textContent); '
                '}}).catch(() => {{ alert(\'Failed to copy\'); }});" '
                'style="padding: 2px 6px; cursor: pointer; font-size: 11px; background: #417690; color: white; border: none; border-radius: 3px;">'
                '📋 Copy</button>'
                '</div>'
                '<script>document.getElementById("{}").textContent = window.location.protocol + "//" + window.location.host + "{}";</script>',
                button_id, button_id, button_id, url
            )
        except Exception:
            return '-'
    copy_url_button.short_description = "CDN URL"

    def view_file_link(self, obj):
        """Show a link to view the file directly."""
        if not obj or not obj.pk or not obj.slug:
            return '-'

        try:
            url = obj.get_file_url()
            return format_html(
                '<a href="{}" target="_blank" style="color: #417690; text-decoration: none; font-weight: 500;">'
                '🔗 Open</a>'
                '<script>document.querySelectorAll(\'a[href="{}"]\').forEach(a => {{ '
                'a.href = window.location.protocol + "//" + window.location.host + "{}"; '
                '}});</script>',
                url, url, url
            )
        except Exception:
            return '-'
    view_file_link.short_description = "View"

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


@admin.register(BackupRestore)
class BackupRestoreAdmin(admin.ModelAdmin):
    """
    Custom admin for Backup & Restore functionality.
    This doesn't manage a real model - just provides a UI for backup/restore.
    """
    change_list_template = 'admin/backup_restore.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        """Return empty queryset since this model has no database table."""
        return self.model.objects.none()

    def changelist_view(self, request, extra_context=None):
        """Override to show our custom backup/restore page without querying database."""
        from django.shortcuts import render

        extra_context = extra_context or {}
        extra_context.update({
            'title': 'Backup & Restore',
            'app_label': self.model._meta.app_label,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request),
            'has_delete_permission': self.has_delete_permission(request),
            'opts': self.model._meta,
        })

        return render(request, self.change_list_template, extra_context)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'confirmed', 'subscribed_at', 'ip_address')
    list_filter = ('is_active', 'confirmed', 'subscribed_at')
    search_fields = ('email', 'ip_address')
    readonly_fields = ('subscribed_at', 'unsubscribed_at', 'ip_address', 'user_agent')
    ordering = ('-subscribed_at',)

    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'is_active', 'confirmed')
        }),
        ('Subscription Details', {
            'fields': ('subscribed_at', 'unsubscribed_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_subscribers', 'deactivate_subscribers', 'export_emails']

    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f'{updated} subscriber(s) activated.')
    activate_subscribers.short_description = "Activate selected subscribers"

    def deactivate_subscribers(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for subscriber in queryset:
            subscriber.unsubscribe()
            updated += 1
        self.message_user(request, f'{updated} subscriber(s) deactivated.')
    deactivate_subscribers.short_description = "Deactivate selected subscribers"

    def export_emails(self, request, queryset):
        emails = list(queryset.filter(is_active=True).values_list('email', flat=True))
        emails_text = ', '.join(emails)
        self.message_user(request, f'Active emails ({len(emails)}): {emails_text}')
    export_emails.short_description = "Export active email addresses"