/**
 * Experience Data Structure
 *
 * This file contains all professional experience information displayed on the Experience page.
 * All fields are optional - if a field is missing or empty, it will be gracefully handled
 * using the builder pattern in the ExperienceCard component.
 *
 * To edit:
 * 1. Update the values in the experienceData object below
 * 2. You can remove any field from an experience entry if you don't want to display it
 * 3. Set is_visible to false to hide an entry without deleting it
 * 4. Use display_order to control the order of experience items (lower numbers appear first)
 */

export interface ExperienceItem {
  company_name?: string;           // Company name
  company_logo_url?: string;       // URL to company logo
  role?: string;                   // Job title/role
  employment_type?: string;        // e.g., "Full-time", "Part-time", "Internship"
  location?: string;               // Physical location
  work_mode?: string;              // e.g., "Remote", "On-site", "Hybrid"
  start_date?: string;             // Start date (e.g., "Jan 2024")
  end_date?: string | null;        // End date or null if current
  is_current?: boolean;            // Set to true if currently working
  description?: string;            // Brief description of the role
  achievements?: string[];         // Array of achievement strings
  skills?: string[];               // Array of skills used
  tech_stack?: string[];           // Array of technologies used
  is_visible?: boolean;            // Set to false to hide this entry (default: true)
  display_order?: number;          // Order of display (lower numbers appear first)
  created_at?: string;             // Creation timestamp
  updated_at?: string;             // Last update timestamp
}

export interface ExperienceData {
  metadata: {
    created_at: string;
    updated_at: string;
  };
  page?: {
    title?: string;
    subtitle?: string;
    stats_labels?: {
      years_experience?: string;
      current_positions?: string;
    };
    skills_heading?: string;
  };
  experiences: ExperienceItem[];
}

export const experienceData: ExperienceData = {
  "metadata": {
    "created_at": "2025-10-27T21:15:00Z",
    "updated_at": "2025-10-27T21:15:00Z"
  },
  "experiences": [
    {
      "company_name": "LEADS Corporation Limited",
      "company_logo_url": "",
      "role": "Senior Software Engineer",
      "employment_type": "Full-time",
      "location": "Dhaka, Bangladesh",
      "work_mode": "On-site",
      "start_date": "Oct 2025",
      "end_date": null,
      "is_current": true,
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
      "is_visible": true,
      "display_order": 1,
      "created_at": "2025-10-27T21:15:00Z",
      "updated_at": "2025-10-27T21:15:00Z"
    },
    {
      "company_name": "InalyZe Bangladesh Ltd.",
      "company_logo_url": "",
      "role": "Python Developer (ML Specialist)",
      "employment_type": "Part-time",
      "location": "Remote",
      "work_mode": "Remote",
      "start_date": "Sep 2024",
      "end_date": null,
      "is_current": true,
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
      "is_visible": true,
      "display_order": 2,
      "created_at": "2025-10-27T21:15:00Z",
      "updated_at": "2025-10-27T21:15:00Z"
    },
    {
      "company_name": "Affpilot",
      "company_logo_url": "",
      "role": "Software Engineer",
      "employment_type": "Full-time",
      "location": "Mirpur DOHS, Dhaka",
      "work_mode": "On-site",
      "start_date": "Feb 2025",
      "end_date": "Sep 2025",
      "is_current": false,
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
      "is_visible": true,
      "display_order": 3,
      "created_at": "2025-10-27T21:15:00Z",
      "updated_at": "2025-10-27T21:15:00Z"
    },
    {
      "company_name": "AdsPillar",
      "company_logo_url": "",
      "role": "Machine Learning Engineer",
      "employment_type": "Full-time",
      "location": "Dhaka, Bangladesh",
      "work_mode": "On-site",
      "start_date": "Mar 2024",
      "end_date": "Jan 2025",
      "is_current": false,
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
      "is_visible": true,
      "display_order": 4,
      "created_at": "2025-10-27T21:15:00Z",
      "updated_at": "2025-10-27T21:15:00Z"
    },
    {
      "company_name": "InsureCow",
      "company_logo_url": "",
      "role": "Jr. Machine Learning Engineer",
      "employment_type": "Full-time",
      "location": "Dhaka, Bangladesh",
      "work_mode": "On-site",
      "start_date": "Jan 2024",
      "end_date": "Feb 2024",
      "is_current": false,
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
      "is_visible": true,
      "display_order": 5,
      "created_at": "2025-10-27T21:15:00Z",
      "updated_at": "2025-10-27T21:15:00Z"
    },
    {
      "company_name": "Inflexionpoint Technologies (BD) Ltd.",
      "company_logo_url": "",
      "role": "Machine Learning Intern",
      "employment_type": "Internship",
      "location": "Dhaka, Bangladesh",
      "work_mode": "On-site",
      "start_date": "Aug 2023",
      "end_date": "Jan 2024",
      "is_current": false,
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
      "is_visible": true,
      "display_order": 6,
      "created_at": "2025-10-27T21:15:00Z",
      "updated_at": "2025-10-27T21:15:00Z"
    }
  ]
  ,
  "page": {
    "title": "Professional Experience",
    "subtitle": "My career journey and professional accomplishments",
    "stats_labels": {
      "years_experience": "Years Experience",
      "current_positions": "Current Position(s)"
    },
    "skills_heading": "All Skills Across Experiences"
  }
};

/**
 * Example: Adding a new experience entry with minimal fields
 * (All fields are optional - remove any you don't need)
 *
 * {
 *   "company_name": "Tech Company",
 *   "role": "Software Developer",
 *   "start_date": "Jan 2026",
 *   "is_current": true,
 *   "is_visible": true,
 *   "display_order": 1
 * }
 *
 * The builder pattern in ExperienceCard.astro will handle any missing fields gracefully.
 */
