import siteData from './site-data.json';

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
  cover_image?: string;             // Optional cover/thumbnail image URL (e.g. "/images/projects/project1.jpg")
  is_visible?: boolean;             // Set to false to hide this entry (default: true)
  display_order?: number;           // Order of display (lower numbers appear first)
}

export interface ProjectsData {
  projects: ProjectItem[];
  page?: {
    title?: string;
    subtitle?: string;
    stats_labels?: {
      total_projects?: string;
      categories?: string;
    };
  };
}

export const projectsData: ProjectsData = (siteData as any).projectsData;

export const getVisibleProjects = (): ProjectItem[] => {
  return projectsData.projects
    .filter((p) => p.is_visible !== false)
    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
};

