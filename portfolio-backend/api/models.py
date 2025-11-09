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
