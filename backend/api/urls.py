from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    api_root, ProfileViewSet, SocialLinksViewSet, SiteSettingsViewSet,
    EducationViewSet, ExperienceViewSet, ProjectViewSet,
    ResearchViewSet, BlogViewSet, HomeSectionViewSet
)

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'social-links', SocialLinksViewSet, basename='social-links')
router.register(r'site-settings', SiteSettingsViewSet, basename='site-settings')
router.register(r'education', EducationViewSet, basename='education')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'research', ResearchViewSet, basename='research')
router.register(r'blogs', BlogViewSet, basename='blogs')
router.register(r'home-section', HomeSectionViewSet, basename='home-section')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
]
