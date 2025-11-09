from django.db import models


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
    # Store whole homeData as JSON to avoid over-modeling
    data = models.JSONField()

    def __str__(self):
        return "homeData"


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
