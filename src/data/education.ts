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
  degree?: string;                 // Degree name (e.g., "Bachelor's degree", "Master's degree")
  field_of_study?: string;         // Major/Field (e.g., "Computer Science")
  education_type?: string;         // Type (e.g., "Graduate", "Undergraduate", "Higher Secondary")
  start_date?: string;             // Start date (e.g., "Jan 2020")
  end_date?: string;               // End date (e.g., "Dec 2023")
  grade?: string;                  // Grade/CGPA/GPA value
  grade_scale?: string;            // Maximum grade scale (e.g., "4.00", "5.00")
  location?: string;               // Location (e.g., "Dhaka, Bangladesh")
  is_current?: boolean;            // Set to true if currently studying
  institution_logo_url?: string;   // URL to institution logo image
  description?: string;            // Brief description of the education
  achievements?: string[];         // Array of achievement strings
  certificate_url?: string;        // URL to certificate/diploma
  is_visible?: boolean;            // Set to false to hide this entry (default: true)
  display_order?: number;          // Order of display (lower numbers appear first)
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

export const educationData: EducationData = (siteData as any).educationData;

/**
 * Helper: getVisibleEducation
 * Returns the list of education entries that are visible, sorted by display_order.
 * Use this helper from pages to centralize filtering/sorting logic.
 */
export const getVisibleEducation = (): EducationItem[] => {
  return educationData.education
    .filter((item) => item.is_visible !== false)
    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
};

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
