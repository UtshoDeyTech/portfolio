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
  education: EducationItem[];
}

export const educationData: EducationData = {
  "metadata": {
    "created_at": "2025-10-27T21:00:00Z",
    "updated_at": "2025-10-27T21:00:00Z"
  },
  "education": [
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
      "is_current": true,
      "institution_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/4/40/BRAC_University_monogram.svg/1024px-BRAC_University_monogram.svg.png",
      "description": "Specializing in advanced topics such as Machine Learning, Cloud Computing, and Distributed Systems.",
      "achievements": [
        "Maintained CGPA 3.75",
        "Conducted research on decentralized recommendation systems"
      ],
      "certificate_url": "",
      "is_visible": true,
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
      "is_current": false,
      "institution_logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/4/40/BRAC_University_monogram.svg/1024px-BRAC_University_monogram.svg.png",
      "description": "Focused on software engineering, artificial intelligence, and backend development.",
      "achievements": [
        "Graduated with First Class Honors",
        "Developed a Decentralized Movie Recommendation System as final year project"
      ],
      "certificate_url": "",
      "is_visible": true,
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
      "is_current": false,
      "institution_logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Logo_of_Khulna_Public_College.jpg/330px-Logo_of_Khulna_Public_College.jpg",
      "description": "Completed HSC with distinction in Science group.",
      "achievements": ["Awarded Board Scholarship for academic excellence"],
      "certificate_url": "",
      "is_visible": true,
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
      "is_current": false,
      "institution_logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5fWBAixXX-n2KyD3cOjbhKxM_yVP1pctxsA&s",
      "description": "Completed SSC with top grades in Science group.",
      "achievements": ["Secured GPA 5.00 with distinction in all subjects"],
      "certificate_url": "",
      "is_visible": true,
      "display_order": 4
    }
  ]
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
