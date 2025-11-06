/**
 * Blog Data Structure
 *
 * This file contains all blog metadata and functionality.
 * Blog data is fetched from the API endpoints.
 *
 * Features:
 * - Pagination support (configure posts_per_page)
 * - Trending and featured blogs sections
 * - Category/topic organization
 * - Full content support with markdown/html
 */

import siteData from './site-data.json';

export interface BlogPost {
  id?: number;
  slug?: string;
  title?: string;
  subtitle?: string;
  excerpt?: string;
  content_markdown?: string;
  content_html?: string;
  cover_image?: string;
  featured_image?: string;
  category?: string;
  tags?: string[];
  author?: string;
  published_date?: string;
  created_at?: string;
  updated_at?: string;
  views?: number;
  likes?: number;
  comments_count?: number;
  shares?: number;
  is_published?: boolean;
  is_featured?: boolean;
  is_trending?: boolean;
  is_editor_choice?: boolean;
  allow_comments?: boolean;
  display_order?: number;
  read_time?: number;
  meta_description?: string;
  meta_keywords?: string;
}

export interface BlogMetadata {
  site_title: string;
  site_description: string;
  posts_per_page: number;
  author_default: string;
  author_image_default: string;
}

export interface FutureBlogTopics {
  topic: string;
  description: string;
  icon?: string;
}

export interface BlogsData {
  metadata: BlogMetadata;
  blogs: BlogPost[];
  future_topics: FutureBlogTopics[];
}

/**
 * Keep metadata and future topics from local `site-data.json`.
 * Blog posts are fetched from the API.
 */
export const blogsData: BlogsData = {
  metadata: (siteData as any).blogsData?.metadata || {
    site_title: 'Blog',
    site_description: 'Insights and articles',
    posts_per_page: 6,
    author_default: 'Author',
    author_image_default: '/images/profile.jpg',
  },
  blogs: [],
  future_topics: (siteData as any).blogsData?.future_topics || [],
};

// API Endpoints
const BLOG_POSTS_API = 'http://localhost:8000/api/blog-posts/';
const BLOGS_API = 'http://localhost:8000/api/blogs/';
const TRENDING_BLOGS_API = 'http://localhost:8000/api/trending-blogs/';
const FEATURED_BLOGS_API = 'http://localhost:8000/api/featured-blogs/';

/**
 * Fetch all blog posts from the API
 */
export const fetchBlogPosts = async (): Promise<BlogPost[]> => {
  try {
    const res = await fetch(BLOG_POSTS_API);
    if (!res.ok) {
      console.error(`Failed to fetch blog posts: ${res.status} ${res.statusText}`);
      return [];
    }
    const data = await res.json();
    if (!Array.isArray(data)) return [];

    return data.map((item: any) => ({
      id: item.id,
      slug: item.slug,
      title: item.title,
      subtitle: item.subtitle,
      excerpt: item.excerpt,
      content_markdown: item.content_markdown,
      content_html: item.content_html,
      cover_image: item.cover_image,
      featured_image: item.featured_image,
      category: item.category,
      tags: Array.isArray(item.tags) ? item.tags : [],
      author: item.author,
      published_date: item.published_date,
      created_at: item.created_at,
      updated_at: item.updated_at,
      views: item.views,
      likes: item.likes,
      comments_count: item.comments_count,
      shares: item.shares,
      is_published: item.is_published,
      is_featured: item.is_featured,
      is_trending: item.is_trending,
      is_editor_choice: item.is_editor_choice,
      allow_comments: item.allow_comments,
      display_order: item.display_order,
      read_time: item.read_time,
      meta_description: item.meta_description,
      meta_keywords: item.meta_keywords,
    } as BlogPost));
  } catch (err) {
    console.error('Error fetching blog posts:', err);
    return [];
  }
};

/**
 * Fetch a single blog post by slug with full content
 */
export const fetchBlogPostBySlug = async (slug: string): Promise<BlogPost | null> => {
  try {
    const res = await fetch(`${BLOG_POSTS_API}${slug}/`);
    if (!res.ok) {
      console.error(`Failed to fetch blog post ${slug}: ${res.status} ${res.statusText}`);
      return null;
    }
    const item = await res.json();

    return {
      id: item.id,
      slug: item.slug,
      title: item.title,
      subtitle: item.subtitle,
      excerpt: item.excerpt,
      content_markdown: item.content_markdown,
      content_html: item.content_html,
      cover_image: item.cover_image,
      featured_image: item.featured_image,
      category: item.category,
      tags: Array.isArray(item.tags) ? item.tags : [],
      author: item.author,
      published_date: item.published_date,
      created_at: item.created_at,
      updated_at: item.updated_at,
      views: item.views,
      likes: item.likes,
      comments_count: item.comments_count,
      shares: item.shares,
      is_published: item.is_published,
      is_featured: item.is_featured,
      is_trending: item.is_trending,
      is_editor_choice: item.is_editor_choice,
      allow_comments: item.allow_comments,
      display_order: item.display_order,
      read_time: item.read_time,
      meta_description: item.meta_description,
      meta_keywords: item.meta_keywords,
    } as BlogPost;
  } catch (err) {
    console.error(`Error fetching blog post ${slug}:`, err);
    return null;
  }
};

/**
 * Fetch blog metadata and future topics
 */
export const fetchBlogMetadata = async (): Promise<Partial<BlogsData>> => {
  try {
    const res = await fetch(BLOGS_API);
    if (!res.ok) {
      console.error(`Failed to fetch blog metadata: ${res.status} ${res.statusText}`);
      return {};
    }
    const data = await res.json();

    return {
      metadata: data.metadata || blogsData.metadata,
      future_topics: Array.isArray(data.future_topics) ? data.future_topics : [],
    };
  } catch (err) {
    console.error('Error fetching blog metadata:', err);
    return {};
  }
};

/**
 * Fetch trending blog posts
 */
export const fetchTrendingBlogs = async (): Promise<BlogPost[]> => {
  try {
    const res = await fetch(TRENDING_BLOGS_API);
    if (!res.ok) return [];
    const data = await res.json();
    if (!Array.isArray(data)) return [];

    return data.map((item: any) => ({
      id: item.id,
      slug: item.slug,
      title: item.title,
      subtitle: item.subtitle,
      excerpt: item.excerpt,
      cover_image: item.cover_image,
      category: item.category,
      tags: Array.isArray(item.tags) ? item.tags : [],
      author: item.author,
      published_date: item.published_date,
      views: item.views,
      likes: item.likes,
      comments_count: item.comments_count,
      is_trending: item.is_trending,
      is_featured: item.is_featured,
      read_time: item.read_time,
    } as BlogPost));
  } catch (err) {
    console.error('Error fetching trending blogs:', err);
    return [];
  }
};

/**
 * Fetch featured blog posts
 */
export const fetchFeaturedBlogs = async (): Promise<BlogPost[]> => {
  try {
    const res = await fetch(FEATURED_BLOGS_API);
    if (!res.ok) return [];
    const data = await res.json();
    if (!Array.isArray(data)) return [];

    return data.map((item: any) => ({
      id: item.id,
      slug: item.slug,
      title: item.title,
      subtitle: item.subtitle,
      excerpt: item.excerpt,
      cover_image: item.cover_image,
      category: item.category,
      tags: Array.isArray(item.tags) ? item.tags : [],
      author: item.author,
      published_date: item.published_date,
      views: item.views,
      likes: item.likes,
      comments_count: item.comments_count,
      is_trending: item.is_trending,
      is_featured: item.is_featured,
      read_time: item.read_time,
    } as BlogPost));
  } catch (err) {
    console.error('Error fetching featured blogs:', err);
    return [];
  }
};

/**
 * Fetch blogs by category
 */
export const fetchBlogsByCategory = async (category: string): Promise<BlogPost[]> => {
  try {
    const res = await fetch(`${BLOGS_API}category/${encodeURIComponent(category)}/`);
    if (!res.ok) return [];
    const data = await res.json();
    if (!Array.isArray(data)) return [];

    return data.map((item: any) => ({
      id: item.id,
      slug: item.slug,
      title: item.title,
      subtitle: item.subtitle,
      excerpt: item.excerpt,
      cover_image: item.cover_image,
      category: item.category,
      tags: Array.isArray(item.tags) ? item.tags : [],
      author: item.author,
      published_date: item.published_date,
      views: item.views,
      likes: item.likes,
      comments_count: item.comments_count,
      is_trending: item.is_trending,
      is_featured: item.is_featured,
      read_time: item.read_time,
    } as BlogPost));
  } catch (err) {
    console.error(`Error fetching blogs by category ${category}:`, err);
    return [];
  }
};

/**
 * Get all published blogs (async)
 */
export const getPublishedBlogs = async (): Promise<BlogPost[]> => {
  const posts = await fetchBlogPosts();
  return posts.filter((blog) => blog.is_published !== false);
};

/**
 * Get newest blogs (async)
 */
export const getNewBlogs = async (limit: number = 5): Promise<BlogPost[]> => {
  const posts = await getPublishedBlogs();
  return posts
    .sort((a, b) => {
      const dateA = a.published_date || '0';
      const dateB = b.published_date || '0';
      return dateB.localeCompare(dateA);
    })
    .slice(0, limit);
};

/**
 * Get paginated blogs (async)
 */
export const getPaginatedBlogs = async (page: number = 1, perPage?: number) => {
  const postsPerPage = perPage || blogsData.metadata.posts_per_page;
  const allBlogs = await getPublishedBlogs();

  const sortedBlogs = allBlogs.sort((a, b) => {
    if (a.display_order !== b.display_order) {
      return (a.display_order || 999) - (b.display_order || 999);
    }
    const dateA = a.published_date || '0';
    const dateB = b.published_date || '0';
    return dateB.localeCompare(dateA);
  });

  const totalPages = Math.ceil(sortedBlogs.length / postsPerPage);
  const startIndex = (page - 1) * postsPerPage;
  const endIndex = startIndex + postsPerPage;
  const blogs = sortedBlogs.slice(startIndex, endIndex);

  return {
    blogs,
    currentPage: page,
    totalPages,
    totalPosts: sortedBlogs.length,
    hasNextPage: page < totalPages,
    hasPrevPage: page > 1,
  };
};

/**
 * Get all categories (async)
 */
export const getAllCategories = async (): Promise<string[]> => {
  const posts = await getPublishedBlogs();
  return Array.from(
    new Set(
      posts
        .map((blog) => blog.category)
        .filter((cat) => cat && cat.trim() !== '')
    )
  ).sort();
};

/**
 * Get all tags (async)
 */
export const getAllTags = async (): Promise<string[]> => {
  const posts = await getPublishedBlogs();
  return Array.from(
    new Set(
      posts
        .flatMap((blog) => blog.tags || [])
        .filter((tag) => tag && tag.trim() !== '')
    )
  ).sort();
};

/**
 * Example: Adding a new blog post
 *
 * 1. Create your markdown file: /public/all_blogs_files/my-new-post.md
 *
 * 2. Add to blogs array:
 * {
 *   "id": "my-new-post",
 *   "file_name": "my-new-post.md",
 *   "title": "My New Blog Post",
 *   "description": "A brief description of the post",
 *   "published_date": "2025-01-20",
 *   "tags": ["Python", "Tutorial"],
 *   "categories": ["Backend Development"],
 *   "is_visible": true
 * }
 */
