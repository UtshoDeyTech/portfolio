/**
 * API Client for Portfolio Backend
 *
 * This file contains all API calls to the Django backend.
 * Environment variable API_URL should point to the backend URL.
 */

const API_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000/api';

interface ApiResponse<T> {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: T[];
  data?: T;
}

/**
 * Generic fetch wrapper with error handling
 */
async function apiFetch<T>(endpoint: string): Promise<T> {
  try {
    const response = await fetch(`${API_URL}${endpoint}`);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Failed to fetch ${endpoint}:`, error);
    throw error;
  }
}

/**
 * Profile API
 */
export async function getProfile() {
  const response = await apiFetch<ApiResponse<any>>('/profile/');
  return response.results?.[0] || null;
}

/**
 * Social Links API
 */
export async function getSocialLinks() {
  const response = await apiFetch<ApiResponse<any>>('/social-links/');
  return response.results?.[0] || null;
}

/**
 * Site Settings API
 */
export async function getSiteSettings() {
  const response = await apiFetch<ApiResponse<any>>('/site-settings/');
  return response.results?.[0] || null;
}

/**
 * Education API
 */
export async function getEducation() {
  const response = await apiFetch<ApiResponse<any>>('/education/');
  return response.results || [];
}

export async function getEducationById(id: number) {
  return await apiFetch<any>(`/education/${id}/`);
}

/**
 * Experience API
 */
export async function getExperience() {
  const response = await apiFetch<ApiResponse<any>>('/experience/');
  return response.results || [];
}

export async function getExperienceById(id: number) {
  return await apiFetch<any>(`/experience/${id}/`);
}

/**
 * Projects API
 */
export async function getProjects() {
  const response = await apiFetch<ApiResponse<any>>('/projects/');
  return response.results || [];
}

export async function getProjectById(id: number) {
  return await apiFetch<any>(`/projects/${id}/`);
}

/**
 * Research API
 */
export async function getResearch() {
  const response = await apiFetch<ApiResponse<any>>('/research/');
  return response.results || [];
}

export async function getResearchById(id: number) {
  return await apiFetch<any>(`/research/${id}/`);
}

/**
 * Blog API
 */
export async function getBlogs() {
  const response = await apiFetch<ApiResponse<any>>('/blogs/');
  return response.results || [];
}

export async function getBlogBySlug(slug: string) {
  return await apiFetch<any>(`/blogs/${slug}/`);
}

/**
 * Home Section API
 */
export async function getHomeSection() {
  const response = await apiFetch<ApiResponse<any>>('/home-section/');
  return response.results?.[0] || null;
}
