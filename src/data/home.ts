/**
 * Home Page Data Structure
 *
 * This file contains all home page specific content.
 * Data from other sections (education, experience, projects, etc.)
 * will be dynamically pulled and displayed on the home page.
 *
 * To edit home page content, update the values below.
 */

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
import siteData from './site-data.json';

export const homeData: HomeData = (siteData as any).homeData;

/**
 * Helper Functions
 */

export const getHeroData = () => homeData.hero;
export const getAboutData = () => homeData.about;
export const getStatsData = () => homeData.stats;
export const getSkillsData = () => homeData.skills;
export const getSocialLinks = () => homeData.social_links;
export const getFeaturedSections = () => homeData.featured_sections;
