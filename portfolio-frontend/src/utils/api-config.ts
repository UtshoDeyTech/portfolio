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
    // Server-side: Use environment variable or fallback to localhost
    return import.meta.env.SERVER_API_URL || 'http://127.0.0.1:8000';
  } else {
    // Client-side: Use public URL accessible from browser (can be relative URL for nginx proxy)
    return import.meta.env.PUBLIC_API_URL || '';
  }
}

/**
 * Fetch data with automatic API URL resolution
 * This is a wrapper around fetch that automatically uses the correct API URL
 */
export async function apiFetch(endpoint: string, options?: RequestInit): Promise<Response> {
  const baseUrl = getApiUrl();

  // Handle relative baseUrl (for nginx proxy)
  if (!baseUrl || baseUrl === '/') {
    const url = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return fetch(url, options);
  }

  // Handle absolute baseUrl
  const url = endpoint.startsWith('/') ? `${baseUrl}${endpoint}` : `${baseUrl}/${endpoint}`;
  return fetch(url, options);
}
