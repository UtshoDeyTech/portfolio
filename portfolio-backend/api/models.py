from django.db import models
import uuid
import os


class EducationEntry(models.Model):
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True)
    field_of_study = models.CharField(max_length=255, blank=True)
    education_type = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=20, blank=True)
    grade_scale = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_current = models.BooleanField(default=False)
    institution_logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    achievements = models.JSONField(default=list, blank=True)
    certificate_url = models.URLField(blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-start_date']

    def __str__(self):
        return f"{self.institution} - {self.degree}"


class ExperienceEntry(models.Model):
    company_name = models.CharField(max_length=255)
    company_logo_url = models.URLField(blank=True)
    role = models.CharField(max_length=255, blank=True)
    employment_type = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    work_mode = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    achievements = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    tech_stack = models.JSONField(default=list, blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-start_date']

    def __str__(self):
        return f"{self.company_name} - {self.role}"


class Project(models.Model):
    slug = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True)
    short_description = models.TextField(blank=True)
    responsibilities = models.JSONField(default=list, blank=True)
    achievements = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    tech_stack = models.JSONField(default=dict, blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    contributor_count = models.IntegerField(default=0)
    collaboration = models.CharField(max_length=255, blank=True)
    tags = models.JSONField(default=list, blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


class ResearchPublication(models.Model):
    slug = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=500)
    authors = models.JSONField(default=list, blank=True)
    publication_date = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    publication_type = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    objectives = models.JSONField(default=list, blank=True)
    dataset = models.CharField(max_length=255, blank=True)
    metrics = models.JSONField(default=list, blank=True)
    comparison_models = models.JSONField(default=list, blank=True)
    results_summary = models.TextField(blank=True)
    highlights = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    url = models.URLField(blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    cover_image = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


class ResearchIcon(models.Model):
    key = models.CharField(max_length=100, unique=True)
    path = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.key


class HomeData(models.Model):
    """
    Singleton model for home page data.
    Better structured with individual fields instead of one large JSON blob.
    """
    # Hero Section
    hero_name = models.CharField(max_length=255, default="Your Name")
    hero_tagline = models.CharField(max_length=500, default="Your Tagline")
    hero_bio = models.TextField(default="Your bio")
    hero_profile_image = models.CharField(max_length=500, blank=True, help_text="URL to profile image (can use CDN URL or relative path)")
    hero_resume_url = models.CharField(max_length=500, blank=True, help_text="URL to resume PDF (can be relative like /resume.pdf)")

    # Hero CTA Buttons
    hero_cta_primary_text = models.CharField(max_length=100, blank=True, default="View My Work")
    hero_cta_primary_url = models.CharField(max_length=500, blank=True, default="/project")
    hero_cta_secondary_text = models.CharField(max_length=100, blank=True, default="Contact Me")
    hero_cta_secondary_url = models.CharField(max_length=500, blank=True, default="mailto:your@email.com")

    # About Section
    about_title = models.CharField(max_length=255, default="About Me")
    about_paragraphs = models.JSONField(default=list, help_text="List of paragraphs for about section")
    about_highlights = models.JSONField(default=list, help_text="List of key highlights")

    # Stats Section
    stats_years_of_experience = models.CharField(max_length=20, blank=True, help_text="e.g., '2+', '5'")
    stats_projects_completed = models.IntegerField(null=True, blank=True)
    stats_publications = models.IntegerField(null=True, blank=True)
    stats_technologies_used = models.IntegerField(null=True, blank=True)

    # Skills Section
    skills_title = models.CharField(max_length=255, default="Technical Skills")
    skills_categories = models.JSONField(default=list, help_text="List of skill categories with name, icon, and skills list")

    # Social Links
    social_github = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_email = models.EmailField(blank=True)
    social_scholar = models.URLField(blank=True)

    # CTA Section
    cta_title = models.CharField(max_length=255, blank=True, default="Let's Work Together")
    cta_paragraph = models.TextField(blank=True, default="I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.")
    cta_primary_text = models.CharField(max_length=100, blank=True, default="Get In Touch")
    cta_primary_url = models.CharField(max_length=500, blank=True)
    cta_secondary_text = models.CharField(max_length=100, blank=True, default="View Portfolio")
    cta_secondary_url = models.CharField(max_length=500, blank=True, default="/project")

    # Featured Sections (toggles)
    show_experience = models.BooleanField(default=True, help_text="Show experience section on home page")
    show_education = models.BooleanField(default=True, help_text="Show education section on home page")
    show_projects = models.BooleanField(default=True, help_text="Show projects section on home page")
    show_research = models.BooleanField(default=True, help_text="Show research section on home page")
    show_blog = models.BooleanField(default=True, help_text="Show blog section on home page")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Page Data"
        verbose_name_plural = "Home Page Data"

    def __str__(self):
        return "Home Page Data"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_home_data(cls):
        """Get or create the home data instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Blog(models.Model):
    # Basic Information
    slug = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True)
    excerpt = models.TextField(blank=True, help_text="Short description/summary of the blog")

    # Content (Markdown)
    content_markdown = models.TextField(help_text="Blog content in Markdown format")

    # Media
    cover_image = models.URLField(blank=True)
    featured_image = models.URLField(blank=True)

    # Categorization
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)

    # Author & Dates
    author = models.CharField(max_length=255, default="Admin")
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Engagement Metrics
    views = models.IntegerField(default=0, help_text="Number of views")
    likes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)

    # Control Flags
    is_published = models.BooleanField(default=False, help_text="Publish this blog")
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage")
    is_trending = models.BooleanField(default=False, help_text="Mark as trending")
    is_editor_choice = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)

    # Display & SEO
    display_order = models.IntegerField(default=0)
    read_time = models.IntegerField(default=5, help_text="Estimated read time in minutes")
    meta_description = models.TextField(blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-published_date', 'display_order']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    """
    Model for storing blog comments.
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True, help_text="Approve comment for display")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Comment"
        verbose_name_plural = "Blog Comments"

    def __str__(self):
        return f"Comment by {self.author_name} on {self.blog.title}"


class BlogsData(models.Model):
    # Keep metadata and lists as JSON for flexibility
    metadata = models.JSONField()
    blogs = models.JSONField(default=list, blank=True)
    future_topics = models.JSONField(default=list, blank=True)

    def __str__(self):
        return "blogsData"


class BlogSettings(models.Model):
    """
    Global blog settings (singleton model).
    """
    duration_update_interval = models.IntegerField(
        default=300,
        help_text="How often to update duration tracking (in seconds). Default: 300 (5 minutes)"
    )
    inactivity_threshold = models.IntegerField(
        default=120,
        help_text="How long before considering user inactive (in seconds). Default: 120 (2 minutes)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Settings"
        verbose_name_plural = "Blog Settings"

    def __str__(self):
        return "Blog Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create the settings instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class BlogView(models.Model):
    """
    Track blog views by device fingerprint.
    Counts one view per device per day (resets daily for better analytics).
    Also tracks time spent and last seen time for engagement analytics.
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='view_records')
    fingerprint = models.CharField(max_length=255, db_index=True, help_text="Device fingerprint")
    session_id = models.CharField(max_length=255, blank=True, help_text="Browser session ID")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True, db_index=True)
    viewed_date = models.DateField(auto_now_add=True, db_index=True, help_text="Date of view (for daily tracking)")
    last_seen = models.DateTimeField(auto_now=True, help_text="Last time user was on this blog")
    duration_seconds = models.IntegerField(default=0, help_text="Total time spent on this blog (in seconds)")

    class Meta:
        ordering = ['-viewed_at']
        verbose_name = "Blog View"
        verbose_name_plural = "Blog Views"
        # Ensure one view per fingerprint per blog per day
        unique_together = ['blog', 'fingerprint', 'viewed_date']
        indexes = [
            models.Index(fields=['blog', 'fingerprint', 'viewed_date']),
            models.Index(fields=['viewed_at']),
            models.Index(fields=['last_seen']),
        ]

    def __str__(self):
        return f"View on {self.blog.title} - {self.fingerprint[:20]} on {self.viewed_date}"

    def get_duration_display(self):
        """Return human-readable duration."""
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"


class BlogLike(models.Model):
    """
    Track unique blog likes by device fingerprint.
    Prevents the same device from liking multiple times.
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='like_records')
    fingerprint = models.CharField(max_length=255, db_index=True, help_text="Device fingerprint")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    liked_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, help_text="False if user unliked")

    class Meta:
        ordering = ['-liked_at']
        verbose_name = "Blog Like"
        verbose_name_plural = "Blog Likes"
        # Ensure one like record per fingerprint per blog
        unique_together = ['blog', 'fingerprint']
        indexes = [
            models.Index(fields=['blog', 'fingerprint', 'is_active']),
            models.Index(fields=['liked_at']),
        ]

    def __str__(self):
        status = "Liked" if self.is_active else "Unliked"
        return f"{status} {self.blog.title} - {self.fingerprint[:20]}"


def secure_file_upload_path(instance, filename):
    """
    Generate a secure file path using UUID.
    Stores files in: secure_storage/<file_type>/<uuid>.<ext>
    """
    ext = os.path.splitext(filename)[1].lower()  # Get file extension
    unique_filename = f"{instance.uuid}{ext}"
    return os.path.join('secure_storage', instance.file_type, unique_filename)


class MediaFile(models.Model):
    """
    Model for storing media files (images, audio, video, documents, etc.)
    Files are stored securely and served through a custom URL endpoint.
    """
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('archive', 'Archive'),
        ('other', 'Other'),
    ]

    # Unique identifier and slug
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, help_text="Custom URL slug for accessing this file")

    # File information
    file = models.FileField(upload_to=secure_file_upload_path, help_text="Upload file (image, audio, video, document, etc.)")
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='image', db_index=True)
    original_filename = models.CharField(max_length=255, blank=True, help_text="Original filename when uploaded")
    file_size = models.BigIntegerField(default=0, help_text="File size in bytes")
    mime_type = models.CharField(max_length=100, blank=True, help_text="MIME type of the file")

    # Metadata
    title = models.CharField(max_length=255, blank=True, help_text="Optional title/description")
    alt_text = models.CharField(max_length=500, blank=True, help_text="Alt text for images (accessibility)")

    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Access control
    is_public = models.BooleanField(default=True, help_text="If false, file requires authentication")

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['uuid']),
            models.Index(fields=['file_type', '-uploaded_at']),
        ]

    def __str__(self):
        return f"{self.slug} ({self.file_type})"

    def save(self, *args, **kwargs):
        # Auto-generate slug from UUID if not provided
        if not self.slug:
            self.slug = str(self.uuid)

        # Store original filename
        if self.file and not self.original_filename:
            self.original_filename = os.path.basename(self.file.name)

        # Calculate file size
        if self.file:
            try:
                self.file_size = self.file.size
            except (ValueError, OSError):
                self.file_size = 0

        super().save(*args, **kwargs)

    def get_file_url(self):
        """
        Returns the custom URL for accessing this file.
        Format: /cdn/{slug}
        """
        return f"/cdn/{self.slug}"

    def get_api_url(self):
        """
        Returns the API URL for accessing this file.
        Format: /api/cdn/{slug}
        """
        return f"/api/cdn/{self.slug}"

    def get_file_extension(self):
        """Returns the file extension."""
        if self.file:
            return os.path.splitext(self.file.name)[1].lstrip('.')
        return ''

    def get_file_size_display(self):
        """Returns human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
