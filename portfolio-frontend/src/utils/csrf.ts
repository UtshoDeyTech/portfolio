/**
 * Get CSRF token from cookie
 */
export function getCsrfToken(): string | null {
  const name = 'csrftoken';
  let cookieValue: string | null = null;

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}

/**
 * Fetch with CSRF token included
 */
export async function fetchWithCsrf(url: string, options: RequestInit = {}) {
  const csrfToken = getCsrfToken();

  const headers = new Headers(options.headers);
  if (csrfToken) {
    headers.set('X-CSRFToken', csrfToken);
  }
  headers.set('Content-Type', 'application/json');

  return fetch(url, {
    ...options,
    headers,
    credentials: 'include', // Important: include cookies
  });
}
