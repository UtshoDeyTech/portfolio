/**
 * Research Data Structure
 *
 * This file contains all research publications and papers displayed on the Research page.
 * All fields are optional - if a field is missing or empty, it will be gracefully handled
 * using the builder pattern in the ResearchCard component.
 *
 * To edit:
 * 1. Update the values in the researchData object below
 * 2. You can remove any field from a research entry if you don't want to display it
 * 3. Set is_visible to false to hide an entry without deleting it
 * 4. Use display_order to control the order of research items (lower numbers appear first)
 */

export interface ResearchPublication {
  id?: number;                     // Unique identifier
  slug?: string;                   // URL-friendly identifier
  title?: string;                  // Research paper title
  authors?: string[];              // List of authors
  publication_date?: string;       // Publication date
  institution?: string;            // Institution/University name
  book?: string;                   // Book name (for book chapters)
  publisher?: string;              // Publisher name
  pages?: string;                  // Page numbers
  publication_type?: string;       // e.g., "Conference Paper", "Journal Article", "Thesis"
  description?: string;            // Detailed description of the research
  abstract?: string;               // Research abstract
  objectives?: string[];           // Research objectives
  methods_used?: string[];         // Research methods
  models_tested?: string[];        // Models tested
  dataset?: string;                // Dataset(s) used
  dataset_source?: string;         // Source of dataset
  metrics?: string[];              // Evaluation metrics used
  evaluation_metrics?: string[];   // Additional evaluation metrics
  comparison_models?: string[];    // Models compared against
  results_summary?: string;        // Summary of results
  highlights?: string[];           // Key highlights of the research
  tags?: string[];                 // Tags for categorization
  url?: string;                    // Publication URL
  pdf_url?: string;                // PDF URL
  github_url?: string;             // GitHub repository URL
  doi?: string;                    // DOI identifier
  citations?: number;              // Citation count
  cover_image?: string;            // Cover image URL
  is_visible?: boolean;            // Set to false to hide this entry (default: true)
  display_order?: number;          // Order of display (lower numbers appear first)
  created_at?: string;             // Creation timestamp
  updated_at?: string;             // Last update timestamp
}

export interface ResearchData {
  metadata: {
    created_at: string;
    updated_at: string;
  };
  page?: {
    title?: string;
    subtitle?: string;
    stats_labels?: {
      publications?: string;
      citations?: string;
      research_areas?: string;
    };
    publications_by_type_title?: string;
    no_publications_text?: string;
    research_areas_title?: string;
    cta?: {
      title?: string;
      paragraph?: string;
      contact_email?: string;
      scholar_url?: string;
      scholar_text?: string;
    };
  };
  research_publications: ResearchPublication[];
}

import siteData from './site-data.json';
import { getApiUrl } from '@/utils/api-config';

/**
 * Keep metadata and page content from local `site-data.json` (used for titles/metadata).
 * The actual list of research entries is fetched from the external API via
 * `fetchResearch` / `getVisiblePublications` below.
 */
export const researchData: ResearchData = {
  metadata: (siteData as any).researchData?.metadata || { created_at: '', updated_at: '' },
  page: (siteData as any).researchData?.page || {},
  research_publications: [],
};

const RESEARCH_API = () => `${getApiUrl()}/api/research/`;

/**
 * Fetch raw research entries from the API. Returns an array matching ResearchPublication shape.
 * If the request fails, returns an empty array and logs the error.
 */
export const fetchResearch = async (): Promise<ResearchPublication[]> => {
  try {
    const res = await fetch(RESEARCH_API());
    if (!res.ok) {
      console.error(`Failed to fetch research: ${res.status} ${res.statusText}`);
      return [];
    }
    const data = await res.json();
    if (!Array.isArray(data)) return [];

    // Map remote fields to local ResearchPublication interface
    return data.map((item: any) => ({
      id: item.id,
      slug: item.slug,
      title: item.title,
      authors: Array.isArray(item.authors) ? item.authors : [],
      publication_date: item.publication_date,
      institution: item.institution,
      book: item.book,
      publisher: item.publisher,
      pages: item.pages,
      publication_type: item.publication_type,
      description: item.description,
      abstract: item.abstract,
      objectives: Array.isArray(item.objectives) ? item.objectives : [],
      methods_used: Array.isArray(item.methods_used) ? item.methods_used : [],
      models_tested: Array.isArray(item.models_tested) ? item.models_tested : [],
      dataset: item.dataset,
      dataset_source: item.dataset_source,
      metrics: Array.isArray(item.metrics) ? item.metrics : [],
      evaluation_metrics: Array.isArray(item.evaluation_metrics) ? item.evaluation_metrics : [],
      comparison_models: Array.isArray(item.comparison_models) ? item.comparison_models : [],
      results_summary: item.results_summary,
      highlights: Array.isArray(item.highlights) ? item.highlights : [],
      tags: Array.isArray(item.tags) ? item.tags : [],
      url: item.url,
      pdf_url: item.pdf_url,
      github_url: item.github_url,
      doi: item.doi,
      citations: item.citations,
      cover_image: item.cover_image,
      is_visible: item.is_visible,
      display_order: item.display_order,
      created_at: item.created_at,
      updated_at: item.updated_at,
    } as ResearchPublication));
  } catch (err) {
    console.error('Error fetching research data:', err);
    return [];
  }
};

/**
 * Returns visible research entries sorted by display_order.
 * Use this helper (async) from pages and components that run on the server.
 */
export const getVisiblePublications = async (): Promise<ResearchPublication[]> => {
  const list = await fetchResearch();
  return list
    .filter((item) => item.is_visible !== false)
    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
};

/**
 * Example: Adding a new research entry with minimal fields
 * (All fields are optional - remove any you don't need)
 *
 * {
 *   "title": "Research Paper Title",
 *   "authors": ["Author 1", "Author 2"],
 *   "publication_date": "2024",
 *   "institution": "University Name",
 *   "publication_type": "Conference Paper",
 *   "is_visible": true,
 *   "display_order": 1
 * }
 *
 * The builder pattern in ResearchCard component will handle any missing fields gracefully.
 */
