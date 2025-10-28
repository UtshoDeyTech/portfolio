from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    Profile, SocialLinks, SiteSettings, Education,
    Experience, Project, Research, Blog, HomeSection
)
from .serializers import (
    ProfileSerializer, SocialLinksSerializer, SiteSettingsSerializer,
    EducationSerializer, ExperienceSerializer, ProjectSerializer,
    ResearchSerializer, BlogSerializer, HomeSectionSerializer
)


@api_view(['GET'])
def api_root(request):
    """API root endpoint with available endpoints"""
    return Response({
        'profile': '/api/profile/',
        'social-links': '/api/social-links/',
        'site-settings': '/api/site-settings/',
        'education': '/api/education/',
        'experience': '/api/experience/',
        'projects': '/api/projects/',
        'research': '/api/research/',
        'blogs': '/api/blogs/',
        'home-section': '/api/home-section/',
    })


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for profile information"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SocialLinksViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for social links"""
    queryset = SocialLinks.objects.all()
    serializer_class = SocialLinksSerializer


class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for site settings"""
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for education entries"""
    queryset = Education.objects.filter(is_visible=True)
    serializer_class = EducationSerializer


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for experience entries"""
    queryset = Experience.objects.filter(is_visible=True)
    serializer_class = ExperienceSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for project entries"""
    queryset = Project.objects.filter(is_visible=True)
    serializer_class = ProjectSerializer


class ResearchViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for research publications"""
    queryset = Research.objects.filter(is_visible=True)
    serializer_class = ResearchSerializer


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for blog posts"""
    queryset = Blog.objects.filter(is_visible=True)
    serializer_class = BlogSerializer
    lookup_field = 'slug'


class HomeSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for home section"""
    queryset = HomeSection.objects.all()
    serializer_class = HomeSectionSerializer
