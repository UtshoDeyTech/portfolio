from django.contrib import admin
from .models import (
    Profile, SocialLinks, SiteSettings, Education,
    Experience, Project, Research, Blog, HomeSection
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'institute', 'created_at')
    search_fields = ('full_name', 'title', 'institute')


@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ('email', 'linkedin', 'github', 'created_at')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('website_url', 'default_title', 'created_at')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'start_date', 'end_date', 'is_visible', 'display_order')
    list_filter = ('is_visible', 'is_current', 'education_type')
    search_fields = ('institution', 'degree', 'field_of_study')
    list_editable = ('is_visible', 'display_order')
    ordering = ('display_order', '-start_date')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'role', 'start_date', 'end_date', 'is_current', 'is_visible', 'display_order')
    list_filter = ('is_visible', 'is_current', 'employment_type', 'work_mode')
    search_fields = ('company_name', 'role', 'description')
    list_editable = ('is_visible', 'display_order')
    ordering = ('display_order', '-start_date')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'type', 'start_date', 'end_date', 'is_visible', 'display_order')
    list_filter = ('is_visible', 'type')
    search_fields = ('title', 'organization', 'description')
    list_editable = ('is_visible', 'display_order')
    ordering = ('display_order', '-start_date')


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'publication_type', 'citations', 'is_visible', 'display_order')
    list_filter = ('is_visible', 'publication_type')
    search_fields = ('title', 'abstract', 'institution')
    list_editable = ('is_visible', 'display_order')
    ordering = ('display_order', '-publication_date')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_date', 'views', 'likes', 'is_featured', 'is_visible', 'display_order')
    list_filter = ('is_visible', 'is_featured')
    search_fields = ('title', 'description', 'author')
    list_editable = ('is_featured', 'is_visible', 'display_order')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('display_order', '-published_date')


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'greeting', 'cta_text', 'created_at')
