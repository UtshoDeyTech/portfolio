import json
from django.core.management.base import BaseCommand
from api.models import (
    Profile, SocialLinks, SiteSettings, Education,
    Experience, Project, Research, Blog, HomeSection
)

class Command(BaseCommand):
    help = 'Import data from frontend TypeScript files into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data import...')

        self.clear_data()
        self.import_profile()
        self.import_social_links()
        self.import_site_settings()
        self.import_home_section()
        self.import_education()
        self.import_experience()
        self.import_projects()
        self.import_research()
        self.import_blogs()

        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))

    def clear_data(self):
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

    def import_profile(self):
        profile_data = {
            "fullName": "Utsho Dey",
            "title": "Software Engineer",
            "institute": "Affpilot.com",
            "author_name": "Utsho Dey",
            "research_areas": [],
            "descriptions": "Utsho Dey is a software engineer specializing in building exceptional digital experiences. With a passion for crafting innovative solutions, Utsho combines technical expertise with a keen eye for design to deliver high-quality software products. Whether working on web applications or mobile platforms, Utsho is dedicated to creating user-friendly interfaces and seamless functionality that enhance the overall user experience."
        }
        Profile.objects.create(
            full_name=profile_data['fullName'],
            title=profile_data['title'],
            institute=profile_data['institute'],
            author_name=profile_data['author_name'],
            descriptions=profile_data['descriptions'],
            research_areas=json.dumps(profile_data['research_areas'])
        )
        self.stdout.write('Profile data imported.')

    def import_social_links(self):
        social_data = {
            "email": "utshodey.tech@gmail.com",
            "linkedin": "https://www.linkedin.com/in/utsho-dey/",
            "x": "https://x.com/UtshoDeyTech",
            "github": "https://github.com/UtshoDeyTech",
            "gitlab": "",
            "scholar": "https://scholar.google.co.in/citations?user=HMKx4rAAAAAJ&hl",
            "inspire": "",
            "arxiv": ""
        }
        SocialLinks.objects.create(**social_data)
        self.stdout.write('Social links imported.')

    def import_site_settings(self):
        template_data = {
            "website_url": "http://localhost:4321",
            "menu_left": False,
            "transitions": True,
            "lightTheme": "light",
            "darkTheme": "dark",
            "excerptLength": 200,
            "postPerPage": 5,
            "base": ""
        }
        seo_data = {
            "default_title": "Utsho Dey - Software Engineer",
            "default_description": "Utsho Dey is a software engineer specializing in building exceptional digital experiences.",
            "default_image": "/images/astro-academia.png"
        }
        SiteSettings.objects.create(
            website_url=template_data['website_url'],
            menu_left=template_data['menu_left'],
            transitions=template_data['transitions'],
            light_theme=template_data['lightTheme'],
            dark_theme=template_data['darkTheme'],
            excerpt_length=template_data['excerptLength'],
            post_per_page=template_data['postPerPage'],
            base=template_data['base'],
            default_title=seo_data['default_title'],
            default_description=seo_data['default_description'],
            default_image=seo_data['default_image']
        )
        self.stdout.write('Site settings imported.')

    def import_home_section(self):
        hero_data = {
            "name": "Utsho Dey",
            "tagline": "Senior Software Engineer | AI/ML Enthusiast | Full-Stack Developer",
            "bio": "Passionate about building scalable backend systems, integrating AI solutions, and solving complex engineering challenges. Experienced in Python, Java, Spring Boot, FastAPI, and cloud technologies.",
            "profile_image": "/images/profile.jpg",
        }
        HomeSection.objects.create(
            greeting="Hi, I'm",
            name=hero_data['name'],
            tagline=hero_data['tagline'],
            description=hero_data['bio'],
            profile_image=hero_data['profile_image'],
            cta_text="View My Work",
            cta_link="/project"
        )
        self.stdout.write('Home section data imported.')

    def import_education(self):
        education_items = [
            {
                "institution": "BRAC University",
                "degree": "Master's degree",
                "field_of_study": "Computer Science",
                "education_type": "Graduate",
                "start_date": "Mar 2024",
                "end_date": "Aug 2025",
                "grade": "3.75",
                "grade_scale": "4.00",
                "location": "Dhaka, Bangladesh",
                "is_current": True,
                "institution_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/4/40/BRAC_University_monogram.svg/1024px-BRAC_University_monogram.svg.png",
                "description": "Specializing in advanced topics such as Machine Learning, Cloud Computing, and Distributed Systems.",
                "achievements": [
                    "Maintained CGPA 3.75",
                    "Conducted research on decentralized recommendation systems"
                ],
                "is_visible": True,
                "display_order": 1
            },
            {
                "institution": "BRAC University",
                "degree": "Bachelor's degree",
                "field_of_study": "Computer Science",
                "education_type": "Undergraduate",
                "start_date": "Apr 2019",
                "end_date": "Dec 2022",
                "grade": "3.70",
                "grade_scale": "4.00",
                "location": "Dhaka, Bangladesh",
                "is_current": False,
                "institution_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/4/40/BRAC_University_monogram.svg/1024px-BRAC_University_monogram.svg.png",
                "description": "Focused on software engineering, artificial intelligence, and backend development.",
                "achievements": [
                    "Graduated with First Class Honors",
                    "Developed a Decentralized Movie Recommendation System as final year project"
                ],
                "is_visible": True,
                "display_order": 2
            },
            {
                "institution": "Khulna Public College",
                "degree": "Higher Secondary Certificate",
                "field_of_study": "Science",
                "education_type": "Higher Secondary",
                "start_date": "May 2015",
                "end_date": "Apr 2017",
                "grade": "5.00",
                "grade_scale": "5.00",
                "location": "Khulna, Bangladesh",
                "is_current": False,
                "institution_logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Logo_of_Khulna_Public_College.jpg/330px-Logo_of_Khulna_Public_College.jpg",
                "description": "Completed HSC with distinction in Science group.",
                "achievements": ["Awarded Board Scholarship for academic excellence"],
                "is_visible": True,
                "display_order": 3
            },
            {
                "institution": "Noapara Model Secondary School",
                "degree": "Secondary School Certificate",
                "field_of_study": "Science",
                "education_type": "Secondary",
                "start_date": "Jan 2003",
                "end_date": "Feb 2015",
                "grade": "5.00",
                "grade_scale": "5.00",
                "location": "Noapara, Bangladesh",
                "is_current": False,
                "institution_logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5fWBAixXX-n2KyD3cOjbhKxM_yVP1pctxsA&s",
                "description": "Completed SSC with top grades in Science group.",
                "achievements": ["Secured GPA 5.00 with distinction in all subjects"],
                "is_visible": True,
                "display_order": 4
            }
        ]
        for item in education_items:
            item['achievements'] = json.dumps(item['achievements'])
            Education.objects.create(**item)
        self.stdout.write('Education data imported.')

    def import_experience(self):
        experience_items = [
            {
                "company_name": "LEADS Corporation Limited",
                "role": "Senior Software Engineer",
                "start_date": "Oct 2025",
                "is_current": True,
                "description": "Working as a Senior Software Engineer focusing on scalable enterprise-grade banking applications using Java, Spring Boot, and Microservices architecture.",
                "achievements": [
                    "Implemented secure microservice communication architecture using RabbitMQ and Redis.",
                    "Optimized Oracle-based data pipelines for large-scale banking transactions.",
                    "Applied SOLID design principles to modernize legacy systems."
                ],
                "skills": [
                    "Spring Boot",
                    "Java",
                    "Banking",
                    "Microservices",
                    "Redis",
                    "RabbitMQ",
                    "SOLID Design Principles",
                    "Git",
                    "Oracle Database"
                ],
                "tech_stack": [
                    "Java 17",
                    "Spring Boot",
                    "Redis",
                    "RabbitMQ",
                    "Oracle",
                    "Git"
                ],
                "is_visible": True,
                "display_order": 1
            },
            {
                "company_name": "InalyZe Bangladesh Ltd.",
                "role": "Python Developer (ML Specialist)",
                "start_date": "Sep 2024",
                "is_current": True,
                "description": "Leading backend and AI infrastructure development for a multi-tenant document intelligence platform, integrating OpenAI, Pinecone, and AWS services.",
                "achievements": [
                    "Built complete FastAPI backend with PostgreSQL and AWS S3 integration.",
                    "Developed an AI-powered document chat system using React and OpenAI APIs.",
                    "Containerized the entire solution using Docker and deployed on Kubernetes.",
                    "Designed scalable multi-tenant architecture ensuring strict data isolation."
                ],
                "skills": [
                    "FastAPI",
                    "PostgreSQL",
                    "Amazon S3",
                    "Pinecone",
                    "OpenAI",
                    "React",
                    "Docker",
                    "Kubernetes",
                    "Prompt Engineering",
                    "Database Design"
                ],
                "tech_stack": [
                    "Python",
                    "FastAPI",
                    "React",
                    "PostgreSQL",
                    "AWS",
                    "Pinecone",
                    "Docker",
                    "Kubernetes"
                ],
                "is_visible": True,
                "display_order": 2
            },
            {
                "company_name": "Affpilot",
                "role": "Software Engineer",
                "start_date": "Feb 2025",
                "end_date": "Sep 2025",
                "is_current": False,
                "description": "Worked on scalable backend systems integrating microservices with OAuth 2.0, Stripe, and RabbitMQ for high-traffic marketing automation products.",
                "achievements": [
                    "Developed microservice-based backend with Python and Go.",
                    "Integrated Stripe Connect for payment automation and subscription management.",
                    "Built asynchronous processing pipelines using RabbitMQ and Celery.",
                    "Deployed services with Docker and optimized database interactions with PostgreSQL."
                ],
                "skills": [
                    "Python",
                    "Go",
                    "RabbitMQ",
                    "Microservices",
                    "gRPC",
                    "REST APIs",
                    "Docker",
                    "OAuth2.0",
                    "PostgreSQL",
                    "Stripe Connect",
                    "OpenAI API",
                    "Gemini",
                    "SERP API"
                ],
                "tech_stack": [
                    "Python",
                    "Go",
                    "Docker",
                    "RabbitMQ",
                    "PostgreSQL",
                    "Celery",
                    "Stripe",
                    "OpenAI"
                ],
                "is_visible": True,
                "display_order": 3
            },
            {
                "company_name": "AdsPillar",
                "role": "Machine Learning Engineer",
                "start_date": "Mar 2024",
                 "end_date": "Jan 2025",
                "is_current": False,
                "description": "Developed AI-integrated social media automation platforms leveraging FastAPI, Supabase, and OpenAI APIs to power intelligent content scheduling and analytics.",
                "achievements": [
                    "Integrated OpenAI, Gemini, and Hugging Face APIs for content generation.",
                    "Built social media scheduling system with multi-platform integration.",
                    "Developed backend using FastAPI and frontend using React.",
                    "Designed database architecture using MySQL, PostgreSQL, and Supabase."
                ],
                "skills": [
                    "FastAPI",
                    "Supabase",
                    "AWS",
                    "PostgreSQL",
                    "OpenAI API",
                    "DALL·E",
                    "Prompt Engineering",
                    "Chatbot Development",
                    "Vector Databases",
                    "Pinecone",
                    "Python",
                    "Database Design"
                ],
                "tech_stack": [
                    "FastAPI",
                    "React",
                    "Supabase",
                    "AWS",
                    "OpenAI",
                    "Hugging Face",
                    "Pinecone"
                ],
                "is_visible": True,
                "display_order": 4
            },
            {
                "company_name": "InsureCow",
                "role": "Jr. Machine Learning Engineer",
                "start_date": "Jan 2024",
                "end_date": "Feb 2024",
                "is_current": False,
                "description": "Worked on data preprocessing and basic model prototyping for insurance-related AI systems.",
                "achievements": [
                    "Collaborated with senior engineers to design ML pipelines.",
                    "Developed scripts for dataset cleaning and transformation."
                ],
                "skills": [
                    "Python",
                    "Scikit-learn",
                    "Data Preprocessing",
                    "Machine Learning"
                ],
                "tech_stack": [
                    "Python",
                    "Pandas",
                    "Scikit-learn"
                ],
                "is_visible": True,
                "display_order": 5
            },
            {
                "company_name": "Inflexionpoint Technologies (BD) Ltd.",
                "role": "Machine Learning Intern",
                "start_date": "Aug 2023",
                "end_date": "Jan 2024",
                "is_current": False,
                "description": "Participated in AI internship program focusing on practical ML model building and deployment.",
                "achievements": [
                    "Developed ML models for classification tasks using Python.",
                    "Learned practical data engineering and model validation techniques."
                ],
                "skills": [
                    "Python",
                    "Machine Learning",
                    "Data Analysis",
                    "Model Evaluation"
                ],
                "tech_stack": [
                    "Python",
                    "Pandas",
                    "Scikit-learn",
                    "TensorFlow"
                ],
                "is_visible": True,
                "display_order": 6
            }
        ]
        for item in experience_items:
            item['achievements'] = json.dumps(item['achievements'])
            item['skills'] = json.dumps(item['skills'])
            item['tech_stack'] = json.dumps(item['tech_stack'])
            Experience.objects.create(**item)
        self.stdout.write('Experience data imported.')

    def import_projects(self):
        project_items = [
            {
                "title": "AskKen.ai",
                "organization": "InalyZe Bangladesh Ltd.",
                "role": "Lead Backend Developer",
                "start_date": "Sep 2024",
                "end_date": "Present",
                "type": "Professional",
                "short_description": "Advanced multi-tenant document intelligence platform for enterprise document management and AI chatbot automation.",
                "responsibilities": [
                    "Led backend architecture design using FastAPI and PostgreSQL.",
                    "Integrated document processing pipeline with Amazon S3 and Pinecone vector database.",
                    "Developed AI chatbot with React and OpenAI integration for intelligent querying.",
                    "Implemented secure multi-company authentication and role-based access control.",
                    "Optimized for high user concurrency and large-scale document repositories.",
                    "Containerized services with Docker and deployed on Kubernetes."
                ],
                "achievements": [
                    "Reduced document query latency by 40% using vector optimization.",
                    "Enabled support for 1M+ document embeddings.",
                    "Enhanced multi-tenant scalability with database sharding."
                ],
                "skills": [
                    "FastAPI",
                    "Python",
                    "PostgreSQL",
                    "Amazon S3",
                    "Pinecone",
                    "Docker",
                    "Kubernetes",
                    "LLM Integration",
                    "Prompt Engineering",
                    "React"
                ],
                "tech_stack": {
                    "backend": ["FastAPI", "Python", "PostgreSQL"],
                    "frontend": ["React"],
                    "ai_integration": ["OpenAI API", "Pinecone", "LangChain"],
                    "devops": ["Docker", "Kubernetes", "Azure", "AWS"]
                },
                "project_url": "https://askken.ai",
                "contributor_count": 4,
                "collaboration": "Led a team of 3 engineers and 1 designer.",
                "tags": ["AI", "LLM", "Enterprise SaaS", "Multi-Tenant Architecture"],
                "is_visible": True,
                "display_order": 1
            },
            {
                "title": "YouTube Video Summarizer",
                "organization": "Affpilot",
                "role": "Python Developer",
                "start_date": "Mar 2025",
                "end_date": "Mar 2025",
                "type": "Personal Project",
                "short_description": "Desktop app to transcribe and summarize YouTube videos in multiple languages using Gemini API.",
                "responsibilities": [
                    "Developed full-featured desktop app using PyQt.",
                    "Integrated Gemini API for cross-language summarization.",
                    "Implemented multi-threaded transcription for performance optimization.",
                    "Designed markdown preview and summary history features."
                ],
                "features": [
                    "Multi-language transcription (10+ languages)",
                    "Cross-language summarization",
                    "Intelligent summarization with Gemini API",
                    "GUI with summary management"
                ],
                "skills": ["Gemini API", "PyQt", "Python", "Ffmpeg", "Prompt Engineering"],
                "tech_stack": {
                    "language": "Python",
                    "libraries": ["PyQt5", "Ffmpeg", "Gemini API", "LangChain"],
                    "architecture": "Desktop Application"
                },
                "github_url": "https://github.com/UtshoDeyTech/youtube-video-summarizer",
                "contributor_count": 1,
                "tags": ["AI", "Multilingual", "Desktop App", "Gemini"],
                "is_visible": True,
                "display_order": 2
            },
            {
                "title": "PlanPostAi.com",
                "organization": "AdsPillar",
                "role": "Backend Engineer",
                "start_date": "Mar 2024",
                "end_date": "Jan 2025",
                "type": "Professional",
                "short_description": "AI-powered social media management platform that automates content creation and scheduling.",
                "responsibilities": [
                    "Developed scalable backend with FastAPI and PostgreSQL.",
                    "Integrated OpenAI, Llama, DALL-E, and Stability AI models for content generation.",
                    "Created API endpoints for bulk content generation and intelligent scheduling.",
                    "Implemented database optimization for high-throughput media uploads."
                ],
                "achievements": [
                    "Reduced manual content creation time by 90%.",
                    "Achieved efficient randomization algorithm for post scheduling.",
                    "Handled 100K+ media generation requests with optimized concurrency."
                ],
                "skills": [
                    "FastAPI",
                    "PostgreSQL",
                    "Docker",
                    "Machine Learning",
                    "Prompt Design",
                    "Git",
                    "Backend Architecture"
                ],
                "tech_stack": {
                    "backend": ["FastAPI", "Python", "PostgreSQL"],
                    "ai_integration": ["OpenAI", "Llama", "DALL-E", "Stability AI"],
                    "devops": ["Docker", "AWS"],
                    "version_control": ["Git", "GitHub"]
                },
                "project_url": "https://planpostai.com",
                "contributor_count": 5,
                "tags": ["AI", "Social Media", "Automation", "SaaS"],
                "is_visible": True,
                "display_order": 3
            },
            {
                "title": "Skin Cancer Detection Using Custom CNN",
                "organization": "BRAC University",
                "role": "Research Student",
                "start_date": "Jan 2023",
                "end_date": "Jan 2025",
                "type": "Academic Project",
                "short_description": "CNN-based image classification model to detect multiple skin diseases using HAM10000 dataset.",
                "responsibilities": [
                    "Designed and trained a custom CNN model for skin disease classification.",
                    "Processed and augmented 28x28 RGB medical images.",
                    "Evaluated model accuracy and optimized with hyperparameter tuning."
                ],
                "skills": ["TensorFlow", "Keras", "Python", "Deep Learning"],
                "datasets": ["HAM10000"],
                "accuracy": "92%",
                "github_url": "https://github.com/UtshoDeyTech/skin-cancer-cnn",
                "tags": ["Deep Learning", "Healthcare", "CNN", "Computer Vision"],
                "is_visible": True,
                "display_order": 4
            },
            {
                "title": "Fashion Recommendation System",
                "organization": "BRAC University",
                "role": "Student Developer",
                "type": "Academic Project",
                "short_description": "A content-based image recommendation system built using Streamlit and feature extraction.",
                "responsibilities": [
                    "Collected and preprocessed fashion image dataset from Kaggle.",
                    "Extracted 2048-dimensional image features using deep models.",
                    "Built similarity-based recommendation model.",
                    "Deployed using Streamlit for user interaction."
                ],
                "skills": ["Streamlit", "Python", "Feature Extraction", "Content-Based Filtering"],
                "datasets": ["Kaggle Fashion Dataset"],
                "tags": ["Recommendation System", "Computer Vision", "Web App"],
                "is_visible": True,
                "display_order": 5
            },
            {
                "title": "Movie Recommendation System",
                "organization": "BRAC University",
                "role": "Student Developer",
                "type": "Academic Project",
                "short_description": "A content-based recommendation engine using IMDb data to suggest similar movies.",
                "responsibilities": [
                    "Scraped and cleaned 25,000 movie entries from IMDb.",
                    "Developed content-based similarity model using TF-IDF and cosine similarity.",
                    "Built and deployed Streamlit web app for movie recommendations."
                ],
                "skills": ["Python", "Streamlit", "Scikit-learn", "Data Scraping"],
                "datasets": ["IMDb Dataset"],
                "tags": ["Recommendation System", "NLP", "Web App"],
                "is_visible": True,
                "display_order": 6
            }
        ]
        for item in project_items:
            item['responsibilities'] = json.dumps(item.get('responsibilities', []))
            item['achievements'] = json.dumps(item.get('achievements', []))
            item['features'] = json.dumps(item.get('features', []))
            item['skills'] = json.dumps(item.get('skills', []))
            item['tech_stack'] = json.dumps(item.get('tech_stack', {}))
            item['datasets'] = json.dumps(item.get('datasets', []))
            item['tags'] = json.dumps(item.get('tags', []))
            Project.objects.create(**item)
        self.stdout.write('Project data imported.')

    def import_research(self):
        research_items = [
            {
                "title": "Application of Deep Convolutional Neural Network in Multiclass Skin Cancer Classification Using Custom CNN Architecture",
                "authors": [
                    "Nadia Shafique",
                    "Kaynat Bint Shaheen",
                    "Zarjis Husain Sikder",
                    "Utsho Dey",
                    "Sharforaz Rahman Swacha"
                ],
                "publication_date": "2023",
                "institution": "Brac University",
                "publication_type": "Undergraduate Thesis / Research Paper",
                "description": "This research proposes a custom CNN architecture for the classification of multiple skin diseases using 28x28 RGB images from the HAM10000 dataset. The model demonstrates superior performance in accuracy and efficiency compared to established pre-trained networks like ResNet50 and EfficientNetB0/B2.",
                "objectives": [
                    "Develop a custom CNN model for multiclass skin disease classification.",
                    "Compare performance with pre-trained models (ResNet50, EfficientNetB0/B2).",
                    "Reduce training time and parameter complexity for efficient deployment."
                ],
                "dataset": "HAM10000",
                "metrics": ["Accuracy", "Precision", "Recall", "F1-Score"],
                "comparison_models": ["ResNet50", "EfficientNetB0", "EfficientNetB2"],
                "results_summary": "The proposed model achieved higher test accuracy with fewer trainable parameters and faster training per epoch than existing pre-trained models, making it suitable for resource-constrained environments.",
                "highlights": [
                    "Improved test accuracy and reduced test loss.",
                    "Lightweight model with lower computational requirements.",
                    "Demonstrates potential for clinical diagnostic deployment."
                ],
                "tags": [
                    "Deep Learning",
                    "CNN",
                    "Medical Imaging",
                    "Healthcare AI",
                    "Computer Vision"
                ],
                "url": "https://scholar.google.com/scholar?cluster=1234567890",
                "is_visible": True,
                "display_order": 1
            },
            {
                "title": "Tailored House Price Prediction Insights for Dhaka and Chittagong City",
                "authors": [
                    "Utsho Dey",
                    "Md Sakhawat Hossain Rabbi",
                    "Md Abrar Hamim",
                    "Md Tarek Habib"
                ],
                "publication_date": "2024-09-11",
                "book": "International Conference on Electrical and Electronics Engineering (ICEEE)",
                "publisher": "Springer Nature Singapore",
                "pages": "229-250",
                "publication_type": "Conference Paper",
                "dataset_source": "https://bdproperty.com/",
                "description": "This paper explores the use of advanced machine learning models to predict housing prices in Dhaka and Chittagong. Using a 3-year dataset, the study applies models such as XGBoost, Random Forest, and Linear Regression to evaluate performance based on R-squared and MSE metrics.",
                "objectives": [
                    "Build accurate predictive models for house pricing in Bangladesh.",
                    "Analyze the impact of data preprocessing and feature scaling on model accuracy.",
                    "Compare traditional and ensemble ML methods for prediction."
                ],
                "methods_used": [
                    "Data Preprocessing",
                    "Feature Engineering",
                    "Model Comparison",
                    "Evaluation Metrics Analysis"
                ],
                "models_tested": ["Linear Regression", "Random Forest", "XGBoost"],
                "evaluation_metrics": ["R²", "Mean Squared Error (MSE)"],
                "results_summary": "Random Forest achieved the highest prediction accuracy, emphasizing the significance of preprocessing and feature selection for regression tasks.",
                "highlights": [
                    "Comprehensive study on Dhaka and Chittagong housing markets.",
                    "Feature scaling significantly improved performance metrics.",
                    "Published in Springer Nature's conference proceedings."
                ],
                "tags": [
                    "Machine Learning",
                    "Regression",
                    "Real Estate Analytics",
                    "Data Science",
                    "XGBoost"
                ],
                "url": "https://link.springer.com/chapter/10.xxxxxxx",
                "is_visible": True,
                "display_order": 2
            }
        ]
        for item in research_items:
            item.pop('id', None)
            item['authors'] = json.dumps(item.get('authors', []))
            item['objectives'] = json.dumps(item.get('objectives', []))
            item['methods_used'] = json.dumps(item.get('methods_used', []))
            item['models_tested'] = json.dumps(item.get('models_tested', []))
            item['comparison_models'] = json.dumps(item.get('comparison_models', []))
            item['highlights'] = json.dumps(item.get('highlights', []))
            item['metrics'] = json.dumps(item.get('metrics', []))
            item['evaluation_metrics'] = json.dumps(item.get('evaluation_metrics', []))
            item['tags'] = json.dumps(item.get('tags', []))
            Research.objects.create(**item)
        self.stdout.write('Research data imported.')

    def import_blogs(self):
        blog_items = []
        for item in blog_items:
            item.pop('id', None)
            item['tags'] = json.dumps(item.get('tags', []))
            item['categories'] = json.dumps(item.get('categories', []))
            Blog.objects.create(**item)
        self.stdout.write('Blog data imported.')