import json
import os
from django.core.management.base import BaseCommand
from api.models import (
    Profile, SocialLinks, SiteSettings, Education,
    Experience, Project, Research, Blog, HomeSection
)


class Command(BaseCommand):
    help = 'Import data from JSON files into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data import...')

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Profile.objects.all().delete()
        SocialLinks.objects.all().delete()
        SiteSettings.objects.all().delete()
        Education.objects.all().delete()
        Experience.objects.all().delete()
        Project.objects.all().delete()
        Research.objects.all().delete()
        Blog.objects.all().delete()
        HomeSection.objects.all().delete()

        # Import sample data
        self.import_profile()
        self.import_social_links()
        self.import_site_settings()
        self.import_home_section()

        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))

    def import_profile(self):
        """Import profile data"""
        profile = Profile.objects.create(
            full_name='Utsho Dey',
            title='Senior Software Engineer | AI/ML Enthusiast | Full-Stack Developer',
            institute='BRAC University',
            author_name='Utsho Dey',
            descriptions='Passionate about building scalable backend systems, integrating AI solutions, and solving complex engineering challenges. Experienced in Python, Java, Spring Boot, FastAPI, and cloud technologies.',
            research_areas=['Machine Learning', 'Deep Learning', 'Recommendation Systems', 'Natural Language Processing']
        )
        self.stdout.write(f'Created profile: {profile.full_name}')

    def import_social_links(self):
        """Import social links"""
        social = SocialLinks.objects.create(
            email='utshodey@example.com',
            linkedin='https://www.linkedin.com/in/utshodey/',
            github='https://github.com/UtshoDeyTech',
            scholar='https://scholar.google.com',
            x='https://twitter.com/utshodey'
        )
        self.stdout.write('Created social links')

    def import_site_settings(self):
        """Import site settings"""
        settings = SiteSettings.objects.create(
            website_url='http://localhost:4321',
            menu_left=False,
            transitions=True,
            light_theme='light',
            dark_theme='dark',
            excerpt_length=200,
            post_per_page=5,
            default_title='Utsho Dey - Portfolio',
            default_description='Portfolio of Utsho Dey - Senior Software Engineer specializing in backend development, AI/ML integration, and full-stack development.',
            default_image='/images/profile.jpg'
        )
        self.stdout.write('Created site settings')

    def import_home_section(self):
        """Import home section"""
        home = HomeSection.objects.create(
            greeting='Hi, I\'m',
            name='Utsho Dey',
            tagline='Senior Software Engineer | AI/ML Enthusiast | Full-Stack Developer',
            description='Passionate about building scalable backend systems, integrating AI solutions, and solving complex engineering challenges.',
            cta_text='View My Work',
            cta_link='/project',
            profile_image='/images/profile.jpg',
            background_pattern='dots'
        )
        self.stdout.write('Created home section')
