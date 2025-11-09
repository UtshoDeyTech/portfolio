import { useEffect, useState } from 'react';
import { getApiUrl } from '@/utils/api-config';

interface Comment {
  id: number;
  blog: number;
  author_name: string;
  comment_text: string;
  created_at: string;
  updated_at: string;
  is_approved: boolean;
}

interface CommentSectionProps {
  slug: string;
  allowComments: boolean;
  initialCommentsCount: number;
}

export default function CommentSection({ slug, allowComments, initialCommentsCount }: CommentSectionProps) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentsCount, setCommentsCount] = useState(initialCommentsCount);
  const [isLoadingComments, setIsLoadingComments] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    author_name: '',
    author_email: '',
    comment_text: '',
  });
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Load comments on component mount
  useEffect(() => {
    loadComments();
  }, [slug]);

  const loadComments = async () => {
    setIsLoadingComments(true);
    try {
      const response = await fetch(`${getApiUrl()}/api/blog-posts/${slug}/comments/list/`);
      if (response.ok) {
        const data = await response.json();
        setComments(data);
        setCommentsCount(data.length);
      }
    } catch (error) {
      console.error('Error loading comments:', error);
    } finally {
      setIsLoadingComments(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSuccessMessage('');
    setErrorMessage('');

    try {
      const response = await fetch(`${getApiUrl()}/api/blog-posts/${slug}/comments/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        setSuccessMessage(data.message || 'Comment added successfully!');
        setFormData({ author_name: '', author_email: '', comment_text: '' });

        // Reload comments to show the new one
        await loadComments();
      } else {
        const error = await response.json();
        setErrorMessage(error.error || 'Failed to submit comment. Please try again.');
      }
    } catch (error) {
      setErrorMessage('An error occurred. Please try again.');
      console.error('Error submitting comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="mt-12 pt-8 border-t">
      {/* Comments Count Header */}
      <div className="flex items-center gap-2 mb-6">
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
            clipRule="evenodd"
          ></path>
        </svg>
        <h2 className="text-2xl font-bold">
          {commentsCount} {commentsCount === 1 ? 'Comment' : 'Comments'}
        </h2>
      </div>

      {/* Comment Form */}
      {allowComments ? (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4">Leave a Comment</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="form-control">
                <label className="label">
                  <span className="label-text">Name *</span>
                </label>
                <input
                  type="text"
                  name="author_name"
                  value={formData.author_name}
                  onChange={handleInputChange}
                  className="input input-bordered w-full"
                  placeholder="Your name"
                  required
                />
              </div>
              <div className="form-control">
                <label className="label">
                  <span className="label-text">Email *</span>
                </label>
                <input
                  type="email"
                  name="author_email"
                  value={formData.author_email}
                  onChange={handleInputChange}
                  className="input input-bordered w-full"
                  placeholder="your.email@example.com"
                  required
                />
              </div>
            </div>
            <div className="form-control">
              <label className="label">
                <span className="label-text">Comment *</span>
              </label>
              <textarea
                name="comment_text"
                value={formData.comment_text}
                onChange={handleInputChange}
                className="textarea textarea-bordered h-32"
                placeholder="Share your thoughts..."
                required
              ></textarea>
            </div>

            {successMessage && (
              <div className="alert alert-success">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="stroke-current shrink-0 h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>{successMessage}</span>
              </div>
            )}

            {errorMessage && (
              <div className="alert alert-error">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="stroke-current shrink-0 h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>{errorMessage}</span>
              </div>
            )}

            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="loading loading-spinner"></span>
                  Submitting...
                </>
              ) : (
                'Post Comment'
              )}
            </button>
          </form>
        </div>
      ) : (
        <div className="alert alert-info mb-8">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            className="stroke-current shrink-0 w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <span>Comments are disabled for this post.</span>
        </div>
      )}

      {/* Comments List */}
      <div className="space-y-6">
        {isLoadingComments ? (
          <div className="flex justify-center py-8">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        ) : comments.length > 0 ? (
          comments.map((comment) => (
            <div key={comment.id} className="card bg-base-200 shadow-sm">
              <div className="card-body">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="avatar placeholder">
                      <div className="bg-neutral text-neutral-content rounded-full w-10">
                        <span className="text-lg">
                          {comment.author_name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold">{comment.author_name}</h4>
                      <time className="text-sm text-base-content/60">
                        {formatDate(comment.created_at)}
                      </time>
                    </div>
                  </div>
                </div>
                <p className="mt-3 text-base-content/80 whitespace-pre-wrap">
                  {comment.comment_text}
                </p>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8 text-base-content/60">
            <p>No comments yet. Be the first to comment!</p>
          </div>
        )}
      </div>
    </div>
  );
}
