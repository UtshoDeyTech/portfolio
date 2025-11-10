/**
 * Home Page Data Structure
 *
 * This file fetches home page content from the backend API.
 * Data from other sections (education, experience, projects, etc.)
 * will be dynamically pulled and displayed on the home page.
 *
 * To edit home page content, update it from the Django admin panel.
 */

import { getApiUrl } from '@/utils/api-config';
import siteData from './site-data.json';

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
  cta?: {
    title?: string;
    paragraph?: string;
    primary?: { text: string; url: string };
    secondary?: { text: string; url: string };
  };
  featured_sections: {
    show_experience: boolean;
    show_education: boolean;
    show_projects: boolean;
    show_research: boolean;
    show_blog: boolean;
  };
}

/**
 * Fetch homeData from backend API
 */
export async function fetchHomeData(): Promise<HomeData> {
  try {
    const response = await fetch(`${getApiUrl()}/api/home/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch home data: ${response.statusText}`);
    }
    const data = await response.json();
    return data.data as HomeData;
  } catch (error) {
    console.error('Error fetching home data from API, falling back to JSON:', error);
    // Fallback to static JSON if API fails
    return (siteData as any).homeData;
  }
}

/**
 * Helper Functions
 */

export const getHeroData = (homeData: HomeData) => homeData.hero;
export const getAboutData = (homeData: HomeData) => homeData.about;
export const getStatsData = (homeData: HomeData) => homeData.stats;
export const getSkillsData = (homeData: HomeData) => homeData.skills;
export const getSocialLinks = (homeData: HomeData) => homeData.social_links;
export const getFeaturedSections = (homeData: HomeData) => homeData.featured_sections;
