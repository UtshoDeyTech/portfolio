import { useEffect, useState } from 'react';
import { fetchWithCsrf } from '@/utils/csrf';
import { getApiUrl } from '@/utils/api-config';
import { getUserIdentifier } from '@/utils/fingerprint';
import { initializeTimeTracking, TimeTracker } from '@/utils/time-tracker';

interface BlogInteractionsProps {
  slug: string;
  initialViews: number;
  initialLikes: number;
}

interface ViewStats {
  has_viewed: boolean;
  first_viewed_at?: string;
  last_seen?: string;
  total_duration?: number;
  total_duration_display?: string;
}

export default function BlogInteractions({ slug, initialViews, initialLikes }: BlogInteractionsProps) {
  const [views, setViews] = useState(initialViews);
  const [likes, setLikes] = useState(initialLikes);
  const [isLiked, setIsLiked] = useState(false);
  const [isLiking, setIsLiking] = useState(false);
  const [fingerprint, setFingerprint] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [timeTracker, setTimeTracker] = useState<TimeTracker | null>(null);
  const [viewStats, setViewStats] = useState<ViewStats>({ has_viewed: false });

  // Get fingerprint on mount
  useEffect(() => {
    const identifier = getUserIdentifier();
    setFingerprint(identifier.fingerprint);
    setSessionId(identifier.sessionId);
  }, []);

  // Initialize time tracking
  useEffect(() => {
    let tracker: TimeTracker | null = null;

    const setupTimeTracking = async () => {
      tracker = await initializeTimeTracking(slug);
      setTimeTracker(tracker);
    };

    setupTimeTracking();

    // Cleanup on unmount
    return () => {
      if (tracker) {
        tracker.stop();
      }
    };
  }, [slug]);

  // Increment view count on component mount
  useEffect(() => {
    if (!fingerprint) return; // Wait for fingerprint to be ready

    const incrementView = async () => {
      try {
        const response = await fetch(`${getApiUrl()}/api/blog-posts/${slug}/increment-view/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            fingerprint,
            session_id: sessionId,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          setViews(data.views);
        }
      } catch (error) {
        console.error('Error incrementing view count:', error);
      }
    };

    incrementView();

    // Check if user has already liked this post (from localStorage)
    const likedPosts = JSON.parse(localStorage.getItem('likedPosts') || '[]');
    setIsLiked(likedPosts.includes(slug));
  }, [slug, fingerprint, sessionId]);

  // Fetch view stats periodically
  useEffect(() => {
    if (!fingerprint) return;

    const fetchViewStats = async () => {
      try {
        const response = await fetch(`${getApiUrl()}/api/blog-posts/${slug}/view-stats/?fingerprint=${fingerprint}`);
        if (response.ok) {
          const data = await response.json();
          if (data.success && data.has_viewed) {
            setViewStats(data);
          }
        }
      } catch (error) {
        console.error('Error fetching view stats:', error);
      }
    };

    // Fetch immediately
    fetchViewStats();

    // Refresh every 30 seconds
    const intervalId = setInterval(fetchViewStats, 30000);

    return () => clearInterval(intervalId);
  }, [slug, fingerprint]);

  // Format relative time (e.g., "2 hours ago")
  const getRelativeTime = (isoString: string): string => {
    const now = new Date();
    const then = new Date(isoString);
    const diffMs = now.getTime() - then.getTime();
    const diffSeconds = Math.floor(diffMs / 1000);
    const diffMinutes = Math.floor(diffSeconds / 60);
    const diffHours = Math.floor(diffMinutes / 60);

    if (diffSeconds < 60) {
      return 'just now';
    } else if (diffMinutes < 60) {
      return `${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else {
      const diffDays = Math.floor(diffHours / 24);
      return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    }
  };

  // Handle like/unlike
  const handleToggleLike = async () => {
    if (isLiking || !fingerprint) return; // Prevent multiple clicks and wait for fingerprint

    setIsLiking(true);
    const action = isLiked ? 'unlike' : 'like';

    try {
      const response = await fetch(`${getApiUrl()}/api/blog-posts/${slug}/toggle-like/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action,
          fingerprint,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setLikes(data.likes);
        setIsLiked(data.is_liked);

        // Update localStorage for consistency
        const likedPosts = JSON.parse(localStorage.getItem('likedPosts') || '[]');
        if (data.is_liked) {
          // Add to liked posts
          if (!likedPosts.includes(slug)) {
            localStorage.setItem('likedPosts', JSON.stringify([...likedPosts, slug]));
          }
        } else {
          // Remove from liked posts
          const updated = likedPosts.filter((s: string) => s !== slug);
          localStorage.setItem('likedPosts', JSON.stringify(updated));
        }
      }
    } catch (error) {
      console.error('Error toggling like:', error);
    } finally {
      setIsLiking(false);
    }
  };

  return (
    <div className="mt-4">
      <div className="flex gap-6 text-sm">
        {/* Views */}
        <div className="flex items-center gap-1">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
            <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd"></path>
          </svg>
          <span>{views} views</span>
        </div>

        {/* Likes - Interactive */}
        <button
          onClick={handleToggleLike}
          disabled={isLiking}
          className={`flex items-center gap-1 transition-colors ${
            isLiked ? 'text-red-500' : 'hover:text-red-500'
          } ${isLiking ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          aria-label={isLiked ? 'Unlike this post' : 'Like this post'}
        >
          <svg
            className="w-4 h-4"
            fill={isLiked ? 'currentColor' : 'none'}
            stroke={isLiked ? 'none' : 'currentColor'}
            strokeWidth={isLiked ? 0 : 2}
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
              clipRule="evenodd"
            ></path>
          </svg>
          <span>{likes} likes</span>
        </button>
      </div>

      {/* User's Personal View Stats */}
      {viewStats.has_viewed && (
        <div className="mt-3 pt-3 border-t border-base-300">
          <div className="flex flex-wrap gap-4 text-xs text-base-content/60">
            {viewStats.last_seen && (
              <div className="flex items-center gap-1">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>Last active: {getRelativeTime(viewStats.last_seen)}</span>
              </div>
            )}
            {viewStats.total_duration_display && viewStats.total_duration && viewStats.total_duration > 0 && (
              <div className="flex items-center gap-1">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
                <span>Time spent: {viewStats.total_duration_display}</span>
              </div>
            )}
            {viewStats.first_viewed_at && (
              <div className="flex items-center gap-1">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                <span>First opened: {getRelativeTime(viewStats.first_viewed_at)}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
