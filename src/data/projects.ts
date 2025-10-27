/**
 * Projects Data Structure
 *
 * This file contains all project information displayed on the Project page.
 * All fields are optional - if a field is missing or empty, it will be gracefully handled
 * using the builder pattern in the ProjectCard component.
 *
 * To edit:
 * 1. Update the values in the projectsData object below
 * 2. You can remove any field from a project entry if you don't want to display it
 * 3. Set is_visible to false to hide an entry without deleting it
 * 4. Use display_order to control the order of project items (lower numbers appear first)
 */

export interface TechStack {
  backend?: string[];
  frontend?: string[];
  ai_integration?: string[];
  devops?: string[];
  language?: string;
  libraries?: string[];
  architecture?: string;
  version_control?: string[];
}

export interface ProjectItem {
  id?: string;                      // Unique identifier
  title?: string;                   // Project title
  organization?: string;            // Organization/Company name
  role?: string;                    // Your role in the project
  start_date?: string;              // Start date (e.g., "Jan 2024")
  end_date?: string;                // End date or "Present"
  type?: string;                    // e.g., "Professional", "Academic Project", "Personal Project"
  short_description?: string;       // Brief description
  description?: string;             // Detailed description (alternative to short_description)
  responsibilities?: string[];      // Array of responsibilities
  achievements?: string[];          // Array of achievements
  features?: string[];              // Array of features
  skills?: string[];                // Array of skills used
  tech_stack?: TechStack;          // Technology stack object
  datasets?: string[];              // Datasets used (for research/ML projects)
  accuracy?: string;                // Model accuracy (for ML projects)
  project_url?: string;             // Live project URL
  github_url?: string;              // GitHub repository URL
  demo_url?: string;                // Demo URL
  contributor_count?: number;       // Number of contributors
  collaboration?: string;           // Collaboration details
  tags?: string[];                  // Tags for categorization
  is_visible?: boolean;             // Set to false to hide this entry (default: true)
  display_order?: number;           // Order of display (lower numbers appear first)
}

export interface ProjectsData {
  projects: ProjectItem[];
}

export const projectsData: ProjectsData = {
  "projects": [
    {
      "id": "askken_ai",
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
      "is_visible": true,
      "display_order": 1
    },
    {
      "id": "youtube_summarizer",
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
      "is_visible": true,
      "display_order": 2
    },
    {
      "id": "planpost_ai",
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
      "is_visible": true,
      "display_order": 3
    },
    {
      "id": "skin_cancer_detection",
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
      "is_visible": true,
      "display_order": 4
    },
    {
      "id": "fashion_recommendation",
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
      "is_visible": true,
      "display_order": 5
    },
    {
      "id": "movie_recommendation",
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
      "is_visible": true,
      "display_order": 6
    }
  ]
};

/**
 * Example: Adding a new project entry with minimal fields
 * (All fields are optional - remove any you don't need)
 *
 * {
 *   "id": "my_project",
 *   "title": "My Awesome Project",
 *   "short_description": "A brief description of what it does",
 *   "skills": ["Python", "React"],
 *   "tags": ["Web App"],
 *   "is_visible": true,
 *   "display_order": 1
 * }
 *
 * The builder pattern in ProjectCard.astro will handle any missing fields gracefully.
 */
