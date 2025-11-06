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

export const projectsData: ProjectsData = {
  projects: (siteData as any).projectsData?.projects || [],
  page: (siteData as any).projectsData?.page || {},
};

const PROJECTS_API = 'http://localhost:8000/api/projects/';

export const fetchProjects = async (): Promise<ProjectItem[]> => {
  try {
    const res = await fetch(PROJECTS_API);
    if (!res.ok) {
      console.error(`Failed to fetch projects: ${res.status} ${res.statusText}`);
      return [];
    }
    const data = await res.json();
    if (!Array.isArray(data)) return [];

    return data.map((item: any) => ({
      id: item.id?.toString?.(),
      title: item.title || item.slug || item.id?.toString?.(),
      organization: item.organization,
      role: item.role,
      start_date: item.start_date,
      end_date: item.end_date,
      type: item.type,
      short_description: item.short_description,
      description: item.description,
      responsibilities: Array.isArray(item.responsibilities) ? item.responsibilities : [],
      achievements: Array.isArray(item.achievements) ? item.achievements : [],
      features: Array.isArray(item.features) ? item.features : [],
      skills: Array.isArray(item.skills) ? item.skills : [],
      tech_stack: item.tech_stack || undefined,
      datasets: Array.isArray(item.datasets) ? item.datasets : [],
      accuracy: item.accuracy,
      project_url: item.project_url,
      github_url: item.github_url,
      demo_url: item.demo_url,
      contributor_count: item.contributor_count,
      collaboration: item.collaboration,
      tags: Array.isArray(item.tags) ? item.tags : [],
      cover_image: item.cover_image,
      is_visible: item.is_visible,
      display_order: item.display_order,
    } as ProjectItem));
  } catch (err) {
    console.error('Error fetching projects data:', err);
    return [];
  }
};

export const getVisibleProjects = async (): Promise<ProjectItem[]> => {
  const list = await fetchProjects();
  return list
    .filter((p) => p.is_visible !== false)
    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
};

