import { useEffect, useState } from 'react';
import { fetchWithCsrf } from '@/utils/csrf';
import { getApiUrl } from '@/utils/api-config';

interface BlogInteractionsProps {
  slug: string;
  initialViews: number;
  initialLikes: number;
}

export default function BlogInteractions({ slug, initialViews, initialLikes }: BlogInteractionsProps) {
  const [views, setViews] = useState(initialViews);
  const [likes, setLikes] = useState(initialLikes);
  const [isLiked, setIsLiked] = useState(false);
  const [isLiking, setIsLiking] = useState(false);

  // Increment view count on component mount
  useEffect(() => {
    const incrementView = async () => {
      try {
        const response = await fetch(`${getApiUrl()}/api/blog-posts/${slug}/increment-view/`, {
          method: 'POST',
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
  }, [slug]);

  // Handle like/unlike
  const handleToggleLike = async () => {
    if (isLiking) return; // Prevent multiple clicks

    setIsLiking(true);
    const action = isLiked ? 'unlike' : 'like';

    try {
      const response = await fetch(`${getApiUrl()}/api/blog-posts/${slug}/toggle-like/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action }),
      });

      if (response.ok) {
        const data = await response.json();
        setLikes(data.likes);
        setIsLiked(!isLiked);

        // Update localStorage
        const likedPosts = JSON.parse(localStorage.getItem('likedPosts') || '[]');
        if (isLiked) {
          // Remove from liked posts
          const updated = likedPosts.filter((s: string) => s !== slug);
          localStorage.setItem('likedPosts', JSON.stringify(updated));
        } else {
          // Add to liked posts
          localStorage.setItem('likedPosts', JSON.stringify([...likedPosts, slug]));
        }
      }
    } catch (error) {
      console.error('Error toggling like:', error);
    } finally {
      setIsLiking(false);
    }
  };

  return (
    <div className="flex gap-6 mt-4 text-sm">
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
  );
}
