/**
 * Time Tracking Utility
 *
 * Tracks time spent on a page and sends updates to the backend.
 * Handles page visibility changes and user inactivity.
 */

import { getApiUrl } from './api-config';
import { getUserIdentifier } from './fingerprint';

interface TimeTrackerOptions {
  slug: string;
  updateInterval?: number; // How often to send updates (milliseconds)
  inactivityThreshold?: number; // How long before considering user inactive (milliseconds)
}

export class TimeTracker {
  private slug: string;
  private startTime: number;
  private lastActiveTime: number;
  private totalTime: number = 0;
  private updateInterval: number;
  private inactivityThreshold: number;
  private intervalId: number | null = null;
  private fingerprint: string = '';
  private isActive: boolean = true;

  constructor(options: TimeTrackerOptions) {
    this.slug = options.slug;
    this.updateInterval = options.updateInterval || 30000; // 30 seconds default
    this.inactivityThreshold = options.inactivityThreshold || 60000; // 1 minute default
    this.startTime = Date.now();
    this.lastActiveTime = Date.now();

    // Get fingerprint
    const identifier = getUserIdentifier();
    this.fingerprint = identifier.fingerprint;

    this.init();
  }

  private init() {
    // Track user activity
    this.addActivityListeners();

    // Start periodic updates
    this.startTracking();

    // Send final update before page unload
    window.addEventListener('beforeunload', () => {
      this.sendUpdate();
    });

    // Handle page visibility changes
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.pause();
      } else {
        this.resume();
      }
    });
  }

  private addActivityListeners() {
    const activityEvents = ['mousemove', 'keydown', 'scroll', 'click', 'touchstart'];

    activityEvents.forEach(event => {
      document.addEventListener(event, () => {
        this.lastActiveTime = Date.now();
        this.isActive = true;
      }, { passive: true });
    });
  }

  private startTracking() {
    // Send updates periodically
    this.intervalId = window.setInterval(() => {
      this.checkAndSendUpdate();
    }, this.updateInterval);
  }

  private checkAndSendUpdate() {
    const now = Date.now();
    const timeSinceLastActivity = now - this.lastActiveTime;

    // Only count time if user is active
    if (timeSinceLastActivity < this.inactivityThreshold) {
      this.sendUpdate();
    } else {
      // User is inactive, mark as such
      this.isActive = false;
    }
  }

  private async sendUpdate() {
    if (!this.fingerprint) return;

    const now = Date.now();
    const sessionDuration = Math.floor((now - this.startTime) / 1000); // Convert to seconds

    // Calculate actual active time (excluding inactive periods)
    const timeSinceLastActive = now - this.lastActiveTime;
    const activeTime = timeSinceLastActive < this.inactivityThreshold
      ? sessionDuration
      : Math.floor((this.lastActiveTime - this.startTime) / 1000);

    if (activeTime <= 0) return;

    try {
      const response = await fetch(`${getApiUrl()}/api/blog-posts/${this.slug}/update-duration/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fingerprint: this.fingerprint,
          duration: activeTime,
        }),
        // Use sendBeacon if available for beforeunload
        keepalive: true,
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Duration updated:', data.total_duration_display);

        // Reset start time for next interval
        this.startTime = now;
        this.totalTime += activeTime;
      }
    } catch (error) {
      console.error('Error updating duration:', error);
    }
  }

  private pause() {
    // Send current duration before pausing
    this.sendUpdate();

    // Stop tracking
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  private resume() {
    // Reset times
    this.startTime = Date.now();
    this.lastActiveTime = Date.now();
    this.isActive = true;

    // Restart tracking
    if (!this.intervalId) {
      this.startTracking();
    }
  }

  public stop() {
    // Send final update
    this.sendUpdate();

    // Stop tracking
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }

    // Remove event listeners
    document.removeEventListener('visibilitychange', this.pause);
    window.removeEventListener('beforeunload', this.sendUpdate);
  }

  public getTotalTime(): number {
    return this.totalTime;
  }
}

/**
 * Fetch blog settings from API
 */
async function fetchBlogSettings(): Promise<{ updateInterval: number; inactivityThreshold: number }> {
  try {
    const response = await fetch(`${getApiUrl()}/api/blog-settings/`);
    if (response.ok) {
      const data = await response.json();
      return {
        updateInterval: data.duration_update_interval * 1000, // Convert seconds to milliseconds
        inactivityThreshold: data.inactivity_threshold * 1000, // Convert seconds to milliseconds
      };
    }
  } catch (error) {
    console.error('Error fetching blog settings:', error);
  }

  // Return defaults if fetch fails
  return {
    updateInterval: 300000, // 5 minutes default
    inactivityThreshold: 120000, // 2 minutes default
  };
}

/**
 * Initialize time tracking for a blog post
 * Fetches settings from API and uses configured intervals
 * @param slug Blog post slug
 * @returns Promise<TimeTracker> instance
 */
export async function initializeTimeTracking(slug: string): Promise<TimeTracker> {
  const settings = await fetchBlogSettings();

  return new TimeTracker({
    slug,
    updateInterval: settings.updateInterval,
    inactivityThreshold: settings.inactivityThreshold,
  });
}
