from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json


class JSONField(models.TextField):
    """Custom JSON field for SQLite compatibility"""

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, (list, dict)):
            return value
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value, cls=DjangoJSONEncoder)


class Profile(models.Model):
    """Main profile information"""
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    institute = models.CharField(max_length=255, blank=True)
    author_name = models.CharField(max_length=255)
    descriptions = models.TextField()
    research_areas = JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.full_name


class SocialLinks(models.Model):
    """Social media links"""
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    x = models.URLField(blank=True)
    github = models.URLField(blank=True)
    gitlab = models.URLField(blank=True)
    scholar = models.URLField(blank=True)
    inspire = models.URLField(blank=True)
    arxiv = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Social Links'
        verbose_name_plural = 'Social Links'

    def __str__(self):
        return "Social Links"


class SiteSettings(models.Model):
    """Site template and SEO settings"""
    # Template settings
    website_url = models.URLField()
    menu_left = models.BooleanField(default=False)
    transitions = models.BooleanField(default=True)
    light_theme = models.CharField(max_length=50, default='light')
    dark_theme = models.CharField(max_length=50, default='dark')
    excerpt_length = models.IntegerField(default=200)
    post_per_page = models.IntegerField(default=5)
    base = models.CharField(max_length=100, blank=True)

    # SEO settings
    default_title = models.CharField(max_length=255)
    default_description = models.TextField()
    default_image = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return "Site Settings"


class Education(models.Model):
    """Education entries"""
    institution = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    field_of_study = models.CharField(max_length=255, blank=True)
    education_type = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    grade_scale = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_current = models.BooleanField(default=False)
    institution_logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    achievements = JSONField(default=list, blank=True)
    certificate_url = models.URLField(blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-start_date']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    """Work experience entries"""
    company_name = models.CharField(max_length=255, blank=True)
    company_logo_url = models.URLField(blank=True)
    role = models.CharField(max_length=255, blank=True)
    employment_type = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    work_mode = models.CharField(max_length=50, blank=True)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    achievements = JSONField(default=list, blank=True)
    skills = JSONField(default=list, blank=True)
    tech_stack = JSONField(default=list, blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-start_date']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'

    def __str__(self):
        return f"{self.role} at {self.company_name}"


class Project(models.Model):
    """Project entries"""
    title = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=100, blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    responsibilities = JSONField(default=list, blank=True)
    achievements = JSONField(default=list, blank=True)
    features = JSONField(default=list, blank=True)
    skills = JSONField(default=list, blank=True)
    tech_stack = JSONField(default=dict, blank=True)
    datasets = JSONField(default=list, blank=True)
    accuracy = models.CharField(max_length=50, blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    collaboration = models.CharField(max_length=255, blank=True)
    tags = JSONField(default=list, blank=True)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True)
    contributor_count = models.IntegerField(null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-start_date']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


class Research(models.Model):
    """Research publication entries"""
    title = models.CharField(max_length=500, blank=True)
    authors = JSONField(default=list, blank=True)
    publication_date = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    book = models.CharField(max_length=500, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    publication_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    objectives = JSONField(default=list, blank=True)
    methods_used = JSONField(default=list, blank=True)
    models_tested = JSONField(default=list, blank=True)
    dataset = models.CharField(max_length=255, blank=True)
    dataset_source = models.URLField(blank=True)
    comparison_models = JSONField(default=list, blank=True)
    results_summary = models.TextField(blank=True)
    highlights = JSONField(default=list, blank=True)
    metrics = JSONField(default=list, blank=True)
    evaluation_metrics = JSONField(default=list, blank=True)
    tags = JSONField(default=list, blank=True)
    url = models.URLField(blank=True)
    pdf_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    doi = models.CharField(max_length=255, blank=True)
    citations = models.IntegerField(null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-publication_date']
        verbose_name = 'Research Publication'
        verbose_name_plural = 'Research Publications'

    def __str__(self):
        return self.title


class Blog(models.Model):
    """Blog post entries"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    file_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)
    author = models.CharField(max_length=255, blank=True)
    author_image = models.URLField(blank=True)
    published_date = models.CharField(max_length=50, blank=True)
    read_time = models.IntegerField(null=True, blank=True)
    tags = JSONField(default=list, blank=True)
    categories = JSONField(default=list, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-published_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.file_name:
            self.slug = self.file_name.replace('.md', '')
        super().save(*args, **kwargs)


class HomeSection(models.Model):
    """Home page hero section"""
    greeting = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=500)
    description = models.TextField()
    cta_text = models.CharField(max_length=100)
    cta_link = models.CharField(max_length=255)
    profile_image = models.URLField(blank=True)
    background_pattern = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Home Section'
        verbose_name_plural = 'Home Section'

    def __str__(self):
        return "Home Hero Section"
