/**
 * research.ts - Loads research data from the shared JSON bundle and re-exports typed values/helpers.
 */

import siteData from './site-data.json';

export interface ResearchPublication {
  id?: string;
  title?: string;
  authors?: string[];
  publication_date?: string;
  institution?: string;
  book?: string;
  publisher?: string;
  pages?: string;
  publication_type?: string;
  description?: string;
  abstract?: string;
  objectives?: string[];
  methods_used?: string[];
  models_tested?: string[];
  dataset?: string;
  dataset_source?: string;
  metrics?: string[];
  evaluation_metrics?: string[];
  comparison_models?: string[];
  results_summary?: string;
  highlights?: string[];
  tags?: string[];
  url?: string;
  pdf_url?: string;
  github_url?: string;
  doi?: string;
  citations?: number;
  cover_image?: string;
  is_visible?: boolean;
  display_order?: number;
}

export interface ResearchData {
  research_publications: ResearchPublication[];
  page?: Record<string, any>;
}

// Use the JSON bundle as the source of truth for data
export const researchData: ResearchData = (siteData as any).researchData;

export const getVisiblePublications = (): ResearchPublication[] => {
  return researchData.research_publications
    .filter((p) => p.is_visible !== false)
    .sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
};
