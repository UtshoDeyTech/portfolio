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
import siteData from './site-data.json';

/**
 * Keep metadata and page content from local `site-data.json` (used for titles/metadata).
 * The actual list of experiences is fetched from the external API via
 * `fetchExperience` / `getVisibleExperience` below.
 */
export const experienceData: ExperienceData = {
  metadata: (siteData as any).experienceData?.metadata || { created_at: '', updated_at: '' },
  page: (siteData as any).experienceData?.page || {},
  experiences: [],
};

// Use the API endpoint for experience. If your server uses a different path
// (e.g. a typo like /api/exprience), update this constant accordingly.
const EXPERIENCE_API = 'http://localhost:8000/api/experience/';

export const fetchExperience = async (): Promise<ExperienceItem[]> => {
  try {
    const res = await fetch(EXPERIENCE_API);
    if (!res.ok) {
      console.error(`Failed to fetch experience: ${res.status} ${res.statusText}`);
      return [];
    }
    const data = await res.json();
    if (!Array.isArray(data)) return [];

    return data.map((item: any) => ({
      company_name: item.company_name,
      company_logo_url: item.company_logo_url,
      role: item.role,
      employment_type: item.employment_type,
      location: item.location,
      work_mode: item.work_mode,
      start_date: item.start_date,
      end_date: item.end_date,
      is_current: item.is_current,
      description: item.description,
      achievements: Array.isArray(item.achievements) ? item.achievements : [],
      skills: Array.isArray(item.skills) ? item.skills : [],
      tech_stack: Array.isArray(item.tech_stack) ? item.tech_stack : [],
      is_visible: item.is_visible,
      display_order: item.display_order,
      created_at: item.created_at,
      updated_at: item.updated_at,
    } as ExperienceItem));
  } catch (err) {
    console.error('Error fetching experience data:', err);
    return [];
  }
};

export const getVisibleExperience = async (): Promise<ExperienceItem[]> => {
  const list = await fetchExperience();
  return list
    .filter((item) => item.is_visible !== false)
    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
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
