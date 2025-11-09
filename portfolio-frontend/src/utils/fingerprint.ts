/**
 * Browser Fingerprinting Utility
 *
 * Creates a unique identifier for each device/browser combination
 * to track user interactions without requiring authentication.
 *
 * Note: This is not 100% unique but provides good enough uniqueness
 * for tracking likes/views from different devices.
 */

/**
 * Generate a hash from a string
 */
function simpleHash(str: string): string {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash).toString(36);
}

/**
 * Get browser fingerprint components
 */
function getFingerprintComponents(): Record<string, string> {
  const navigator = window.navigator;
  const screen = window.screen;

  return {
    // Browser information
    userAgent: navigator.userAgent || '',
    language: navigator.language || '',
    languages: navigator.languages?.join(',') || '',
    platform: navigator.platform || '',

    // Screen information
    screenResolution: `${screen.width}x${screen.height}`,
    screenColorDepth: `${screen.colorDepth}`,
    screenPixelDepth: `${screen.pixelDepth || ''}`,

    // Timezone
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || '',
    timezoneOffset: `${new Date().getTimezoneOffset()}`,

    // Hardware concurrency (CPU cores)
    hardwareConcurrency: `${(navigator as any).hardwareConcurrency || ''}`,

    // Device memory (if available)
    deviceMemory: `${(navigator as any).deviceMemory || ''}`,

    // Touch support
    touchSupport: `${navigator.maxTouchPoints || 0}`,

    // Canvas fingerprint (basic)
    canvas: getCanvasFingerprint(),

    // WebGL fingerprint (basic)
    webgl: getWebGLFingerprint(),
  };
}

/**
 * Generate a canvas-based fingerprint
 */
function getCanvasFingerprint(): string {
  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) return '';

    // Draw text
    ctx.textBaseline = 'top';
    ctx.font = '14px Arial';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#f60';
    ctx.fillRect(125, 1, 62, 20);
    ctx.fillStyle = '#069';
    ctx.fillText('Browser Fingerprint', 2, 15);
    ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
    ctx.fillText('Browser Fingerprint', 4, 17);

    return simpleHash(canvas.toDataURL());
  } catch (e) {
    return '';
  }
}

/**
 * Generate a WebGL-based fingerprint
 */
function getWebGLFingerprint(): string {
  try {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl') as WebGLRenderingContext | null;
    if (!gl) return '';

    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    if (!debugInfo) return '';

    const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
    const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);

    return simpleHash(`${vendor}~${renderer}`);
  } catch (e) {
    return '';
  }
}

/**
 * Generate a unique device fingerprint
 */
export function generateFingerprint(): string {
  const components = getFingerprintComponents();

  // Combine all components into a single string
  const fingerprintString = Object.entries(components)
    .map(([key, value]) => `${key}:${value}`)
    .join('|');

  // Generate hash
  const hash = simpleHash(fingerprintString);

  // Add timestamp salt for additional uniqueness
  const timestamp = Date.now().toString(36);

  return `fp_${hash}_${timestamp}`;
}

/**
 * Get or create a persistent device fingerprint
 * Stores in localStorage and cookie for persistence
 */
export function getDeviceFingerprint(): string {
  const STORAGE_KEY = 'device_fingerprint';
  const COOKIE_NAME = 'device_fp';

  // Try to get from localStorage first
  let fingerprint = localStorage.getItem(STORAGE_KEY);

  // If not in localStorage, try cookie
  if (!fingerprint) {
    fingerprint = getCookie(COOKIE_NAME);
  }

  // If still no fingerprint, generate a new one
  if (!fingerprint) {
    fingerprint = generateFingerprint();

    // Store in localStorage
    try {
      localStorage.setItem(STORAGE_KEY, fingerprint);
    } catch (e) {
      console.warn('Failed to store fingerprint in localStorage:', e);
    }

    // Store in cookie (expires in 1 year)
    setCookie(COOKIE_NAME, fingerprint, 365);
  }

  return fingerprint;
}

/**
 * Get cookie value
 */
function getCookie(name: string): string | null {
  const nameEQ = name + "=";
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

/**
 * Set cookie
 */
function setCookie(name: string, value: string, days: number) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=Lax";
}

/**
 * Get a simple session ID (for current browser session only)
 */
export function getSessionId(): string {
  const SESSION_KEY = 'session_id';
  let sessionId = sessionStorage.getItem(SESSION_KEY);

  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substring(2)}`;
    sessionStorage.setItem(SESSION_KEY, sessionId);
  }

  return sessionId;
}

/**
 * Get user identifier for API requests
 * Combines device fingerprint and session ID
 */
export function getUserIdentifier(): {
  fingerprint: string;
  sessionId: string;
} {
  return {
    fingerprint: getDeviceFingerprint(),
    sessionId: getSessionId(),
  };
}
