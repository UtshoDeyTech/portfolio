/**
 * Education Data Structure
 *
 * This file contains all education information displayed on the Education page.
 * All fields are optional - if a field is missing or empty, it will be gracefully handled
 * using the builder pattern in the EducationCard component.
 *
 * To edit:
 * 1. Update the values in the educationData object below
 * 2. You can remove any field from an education entry if you don't want to display it
 * 3. Set is_visible to false to hide an entry without deleting it
 * 4. Use display_order to control the order of education items (lower numbers appear first)
 */

export interface EducationItem {
  institution?: string;           // Name of the institution
  degree?: string;                // Degree name (e.g., "Bachelor's degree", "Master's degree")
  field_of_study?: string;        // Major/Field (e.g., "Computer Science")
  education_type?: string;        // Type (e.g., "Graduate", "Undergraduate", "Higher Secondary")
  start_date?: string;            // Start date (e.g., "Jan 2020")
  end_date?: string;              // End date (e.g., "Dec 2023")
  grade?: string;                 // Grade/CGPA/GPA value
  grade_scale?: string;           // Maximum grade scale (e.g., "4.00", "5.00")
  location?: string;              // Location (e.g., "Dhaka, Bangladesh")
  is_current?: boolean;           // Set to true if currently studying
  institution_logo_url?: string;  // URL to institution logo image
  description?: string;           // Brief description of the education
  achievements?: string[];        // Array of achievement strings
  certificate_url?: string;       // URL to certificate/diploma
  is_visible?: boolean;           // Set to false to hide this entry (default: true)
  display_order?: number;         // Order of display (lower numbers appear first)
}

export interface EducationData {
  metadata: {
    created_at: string;
    updated_at: string;
  };
  page?: {
    title?: string;
    subtitle?: string;
    empty_text?: string;
  };
  education: EducationItem[];
}

import siteData from './site-data.json';
import { getApiUrl } from '@/utils/api-config';

/**
 * Keep metadata and page content from local `site-data.json` (used for titles/metadata).
 * The actual list of education entries is fetched from the external API via
 * `fetchEducation` / `getVisibleEducation` below.
 */
export const educationData: EducationData = {
  metadata: (siteData as any).educationData?.metadata || { created_at: '', updated_at: '' },
  page: (siteData as any).educationData?.page || {},
  education: [],
};

const EDUCATION_API = () => `${getApiUrl()}/api/education/`;

/**
 * Fetch raw education entries from the API. Returns an array matching EducationItem shape.
 * If the request fails, returns an empty array and logs the error.
 */
export const fetchEducation = async (): Promise<EducationItem[]> => {
  try {
    const res = await fetch(EDUCATION_API());
    if (!res.ok) {
      console.error(`Failed to fetch education: ${res.status} ${res.statusText}`);
      return [];
    }
    const data = await res.json();
    if (!Array.isArray(data)) return [];

    // Map remote fields to local EducationItem interface (fields largely match)
    return data.map((item: any) => ({
      institution: item.institution,
      degree: item.degree,
      field_of_study: item.field_of_study,
      education_type: item.education_type,
      start_date: item.start_date,
      end_date: item.end_date,
      grade: item.grade,
      grade_scale: item.grade_scale,
      location: item.location,
      is_current: item.is_current,
      institution_logo_url: item.institution_logo_url,
      description: item.description,
      achievements: Array.isArray(item.achievements) ? item.achievements : [],
      certificate_url: item.certificate_url,
      is_visible: item.is_visible,
      display_order: item.display_order,
    } as EducationItem));
  } catch (err) {
    console.error('Error fetching education data:', err);
    return [];
  }
};

/**
 * Returns visible education entries sorted by display_order.
 * Use this helper (async) from pages and components that run on the server.
 */
export const getVisibleEducation = async (): Promise<EducationItem[]> => {
  const list = await fetchEducation();
  return list
    .filter((item) => item.is_visible !== false)
    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
};
// Note: synchronous helper removed. Use the async `getVisibleEducation()` above.

/**
 * Example: Adding a new education entry with minimal fields
 * (All fields are optional - remove any you don't need)
 *
 * {
 *   "institution": "University Name",
 *   "degree": "PhD",
 *   "field_of_study": "Artificial Intelligence",
 *   "start_date": "Sep 2025",
 *   "is_current": true,
 *   "is_visible": true,
 *   "display_order": 1
 * }
 *
 * The builder pattern in EducationCard.astro will handle any missing fields gracefully.
 */
