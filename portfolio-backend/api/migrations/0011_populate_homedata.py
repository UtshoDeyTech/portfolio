# Generated data migration to populate HomeData

from django.db import migrations


def populate_home_data(apps, schema_editor):
    """Populate HomeData with your previous data."""
    HomeData = apps.get_model('api', 'HomeData')

    # Delete any existing data
    HomeData.objects.all().delete()

    # Create your home data
    HomeData.objects.create(
        pk=1,  # Singleton ID
        # Hero Section
        hero_name="Utsho Dey",
        hero_tagline="Senior Software Engineer | AI/ML Enthusiast | Full-Stack Developer",
        hero_bio="Passionate about building scalable backend systems, integrating AI solutions, and solving complex engineering challenges. Experienced in Python, Java, Spring Boot, FastAPI, and cloud technologies.",
        hero_profile_image="http://localhost:8000/api/cdn/utsho-dey-profile-photo",
        hero_resume_url="/resume.pdf",

        # Hero CTA Buttons
        hero_cta_primary_text="View My Work",
        hero_cta_primary_url="/project",
        hero_cta_secondary_text="Contact Me",
        hero_cta_secondary_url="mailto:utshodey@example.com",

        # About Section
        about_title="About Me",
        about_paragraphs=[
            "I'm a Senior Software Engineer with 2+ years of experience specializing in backend development, machine learning integration, and building enterprise-grade applications. Currently working at LEADS Corporation Limited, I focus on scalable banking solutions using Java and Spring Boot.",
            "My expertise spans across Python (FastAPI, Django), Java (Spring Boot), cloud technologies (AWS, Docker, Kubernetes), and AI/ML integration (OpenAI, LangChain, Pinecone). I'm passionate about writing clean, maintainable code and implementing best practices in software architecture.",
            "I hold a Master's degree in Computer Science from BRAC University, where I've conducted research on recommendation systems and deep learning. I enjoy contributing to open-source projects and sharing knowledge through technical blogs."
        ],
        about_highlights=[
            "Designed and deployed microservices architecture handling 100K+ requests",
            "Reduced system latency by 40% through optimization techniques",
            "Built AI-powered document intelligence platform serving enterprise clients",
            "Published research in Springer Nature conference proceedings"
        ],

        # Stats Section
        stats_years_of_experience="2+",
        stats_projects_completed=10,
        stats_publications=2,
        stats_technologies_used=25,

        # Skills Section
        skills_title="Technical Skills",
        skills_categories=[
            {
                "name": "Backend Development",
                "icon": "⚙️",
                "skills": ["Python", "Java", "Spring Boot", "FastAPI", "Node.js", "Microservices", "REST APIs", "GraphQL"]
            },
            {
                "name": "AI & Machine Learning",
                "icon": "🤖",
                "skills": ["OpenAI", "LangChain", "TensorFlow", "Scikit-learn", "Pinecone", "Prompt Engineering", "LLM Integration"]
            },
            {
                "name": "Databases",
                "icon": "🗄️",
                "skills": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Oracle", "Vector Databases"]
            },
            {
                "name": "Cloud & DevOps",
                "icon": "☁️",
                "skills": ["Docker", "Kubernetes", "AWS", "Azure", "CI/CD", "Git", "Linux"]
            },
            {
                "name": "Frontend",
                "icon": "🎨",
                "skills": ["React", "TypeScript", "Tailwind CSS", "HTML/CSS", "Responsive Design"]
            },
            {
                "name": "Tools & Others",
                "icon": "🛠️",
                "skills": ["RabbitMQ", "Celery", "OAuth2.0", "Stripe", "Supabase", "PyQt"]
            }
        ],

        # Social Links
        social_email="utshodey@example.com",
        social_github="https://github.com/UtshoDeyTech",
        social_linkedin="https://www.linkedin.com/in/utshodey/",
        social_twitter="",
        social_scholar="https://scholar.google.com",

        # CTA Section
        cta_title="Let's Work Together",
        cta_paragraph="I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.",
        cta_primary_text="Get In Touch",
        cta_primary_url="mailto:utshodey@example.com",
        cta_secondary_text="View Portfolio",
        cta_secondary_url="/project",

        # Featured Sections
        show_experience=True,
        show_education=True,
        show_projects=True,
        show_research=True,
        show_blog=True,
    )


def reverse_populate(apps, schema_editor):
    """Reverse migration - delete the data."""
    HomeData = apps.get_model('api', 'HomeData')
    HomeData.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_homedata_hero_profile_image_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_home_data, reverse_populate),
    ]
