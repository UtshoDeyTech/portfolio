/**
 * API Configuration
 *
 * This utility provides the correct API URL based on the execution context:
 * - Server-side (Astro SSR): Uses SERVER_API_URL for Docker internal networking
 * - Client-side (Browser): Uses PUBLIC_API_URL for external access
 */

/**
 * Get the appropriate API base URL based on execution context
 * @returns The API base URL to use
 */
export function getApiUrl(): string {
  // Check if we're running on the server (Node.js) or client (browser)
  const isServer = typeof window === 'undefined';

  if (isServer) {
    // Server-side: Use Docker internal network URL
    return import.meta.env.SERVER_API_URL || 'http://backend:8000';
  } else {
    // Client-side: Use public URL accessible from browser
    return import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';
  }
}

/**
 * Fetch data with automatic API URL resolution
 * This is a wrapper around fetch that automatically uses the correct API URL
 */
export async function apiFetch(endpoint: string, options?: RequestInit): Promise<Response> {
  const baseUrl = getApiUrl();
  const url = endpoint.startsWith('/') ? `${baseUrl}${endpoint}` : `${baseUrl}/${endpoint}`;

  return fetch(url, options);
}
