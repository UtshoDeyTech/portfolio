/**
 * Home Page Data Structure
 *
 * This file contains all home page specific content.
 * Data from other sections (education, experience, projects, etc.)
 * will be dynamically pulled and displayed on the home page.
 *
 * To edit home page content, update the values below.
 */

export interface HomeData {
  hero: {
    name: string;
    tagline: string;
    bio: string;
    profile_image: string;
    resume_url?: string;
    cta_buttons: {
      primary?: { text: string; url: string; };
      secondary?: { text: string; url: string; };
    };
  };
  about: {
    title: string;
    paragraphs: string[];
    highlights: string[];
  };
  stats: {
    years_of_experience?: string;
    projects_completed?: number;
    publications?: number;
    technologies_used?: number;
  };
  skills: {
    title: string;
    categories: {
      name: string;
      icon?: string;
      skills: string[];
    }[];
  };
  social_links: {
    github?: string;
    linkedin?: string;
    twitter?: string;
    email?: string;
    scholar?: string;
  };
  featured_sections: {
    show_experience: boolean;
    show_education: boolean;
    show_projects: boolean;
    show_research: boolean;
    show_blog: boolean;
  };
}

export const homeData: HomeData = {
  "hero": {
    "name": "Utsho Dey",
    "tagline": "Senior Software Engineer | AI/ML Enthusiast | Full-Stack Developer",
    "bio": "Passionate about building scalable backend systems, integrating AI solutions, and solving complex engineering challenges. Experienced in Python, Java, Spring Boot, FastAPI, and cloud technologies.",
    "profile_image": "/images/profile.jpg",
    "resume_url": "/resume.pdf",
    "cta_buttons": {
      "primary": {
        "text": "View My Work",
        "url": "/project"
      },
      "secondary": {
        "text": "Contact Me",
        "url": "mailto:utshodey@example.com"
      }
    }
  },

  "about": {
    "title": "About Me",
    "paragraphs": [
      "I'm a Senior Software Engineer with 2+ years of experience specializing in backend development, machine learning integration, and building enterprise-grade applications. Currently working at LEADS Corporation Limited, I focus on scalable banking solutions using Java and Spring Boot.",
      "My expertise spans across Python (FastAPI, Django), Java (Spring Boot), cloud technologies (AWS, Docker, Kubernetes), and AI/ML integration (OpenAI, LangChain, Pinecone). I'm passionate about writing clean, maintainable code and implementing best practices in software architecture.",
      "I hold a Master's degree in Computer Science from BRAC University, where I've conducted research on recommendation systems and deep learning. I enjoy contributing to open-source projects and sharing knowledge through technical blogs."
    ],
    "highlights": [
      "Designed and deployed microservices architecture handling 100K+ requests",
      "Reduced system latency by 40% through optimization techniques",
      "Built AI-powered document intelligence platform serving enterprise clients",
      "Published research in Springer Nature conference proceedings"
    ]
  },

  "stats": {
    "years_of_experience": "2+",
    "projects_completed": 10,
    "publications": 2,
    "technologies_used": 25
  },

  "skills": {
    "title": "Technical Skills",
    "categories": [
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
    ]
  },

  "social_links": {
    "github": "https://github.com/UtshoDeyTech",
    "linkedin": "https://www.linkedin.com/in/utshodey/",
    "email": "utshodey@example.com",
    "scholar": "https://scholar.google.com"
  },

  "featured_sections": {
    "show_experience": true,
    "show_education": true,
    "show_projects": true,
    "show_research": true,
    "show_blog": true
  }
};

/**
 * Helper Functions
 */

export const getHeroData = () => homeData.hero;
export const getAboutData = () => homeData.about;
export const getStatsData = () => homeData.stats;
export const getSkillsData = () => homeData.skills;
export const getSocialLinks = () => homeData.social_links;
export const getFeaturedSections = () => homeData.featured_sections;
