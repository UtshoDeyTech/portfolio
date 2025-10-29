/**
 * Blog Data Structure
 *
 * This file contains all blog metadata and configuration.
 * Blog content is stored as .md files in the /public/all_blogs_files/ folder.
 *
 * To add a new blog:
 * 1. Create a .md file in /public/all_blogs_files/ (e.g., my-blog-post.md)
 * 2. Add blog metadata to the blogs array below
 * 3. Set the file_name to match your .md file name
 * 4. Configure other metadata (title, description, tags, etc.)
 *
 * Features:
 * - Pagination support (configure posts_per_page)
 * - New blogs and top blogs sections
 * - Category/topic organization
 * - Draft mode for unpublished posts
 */

import siteData from './site-data.json';

export interface BlogPost {
  id?: string;
  file_name: string;
  title: string;
  slug?: string;
  description?: string;
  author?: string;
  author_image?: string;
  published_date?: string;
  updated_date?: string;
  read_time?: number;
  cover_image?: string;
  tags?: string[];
  categories?: string[];
  is_featured?: boolean;
  is_top_blog?: boolean;
  views?: number;
  likes?: number;
  is_draft?: boolean;
  is_visible?: boolean;
  seo_keywords?: string[];
  display_order?: number;
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

export const blogsData: BlogsData = (siteData as any).blogsData;

export const getPublishedBlogs = () => {
  return blogsData.blogs.filter(
    (blog) => blog.is_visible !== false && blog.is_draft !== true
  );
};

export const getNewBlogs = (limit: number = 5) => {
  return getPublishedBlogs()
    .sort((a, b) => {
      const dateA = a.published_date || '0';
      const dateB = b.published_date || '0';
      return dateB.localeCompare(dateA);
    })
    .slice(0, limit);
};

export const getTopBlogs = (limit: number = 5) => {
  return getPublishedBlogs()
    .filter((blog) => blog.is_top_blog === true || blog.is_featured === true)
    .sort((a, b) => {
      const viewsA = a.views || 0;
      const viewsB = b.views || 0;
      if (viewsA !== viewsB) return viewsB - viewsA;
      return (b.likes || 0) - (a.likes || 0);
    })
    .slice(0, limit);
};

export const getBlogsByCategory = (category: string) => {
  return getPublishedBlogs().filter((blog) => blog.categories?.includes(category));
};

export const getBlogsByTag = (tag: string) => {
  return getPublishedBlogs().filter((blog) => blog.tags?.includes(tag));
};

export const getPaginatedBlogs = (page: number = 1, perPage?: number) => {
  const postsPerPage = perPage || blogsData.metadata.posts_per_page;
  const allBlogs = getPublishedBlogs().sort((a, b) => {
    if (a.display_order !== b.display_order) {
      return (a.display_order || 999) - (b.display_order || 999);
    }
    const dateA = a.published_date || '0';
    const dateB = b.published_date || '0';
    return dateB.localeCompare(dateA);
  });

  const totalPages = Math.ceil(allBlogs.length / postsPerPage);
  const startIndex = (page - 1) * postsPerPage;
  const endIndex = startIndex + postsPerPage;
  const blogs = allBlogs.slice(startIndex, endIndex);

  return {
    blogs,
    currentPage: page,
    totalPages,
    totalPosts: allBlogs.length,
    hasNextPage: page < totalPages,
    hasPrevPage: page > 1,
  };
};

export const getAllCategories = () => {
  return Array.from(
    new Set(
      getPublishedBlogs()
        .flatMap((blog) => blog.categories || [])
        .filter((cat) => cat && cat.trim() !== '')
    )
  ).sort();
};

export const getAllTags = () => {
  return Array.from(
    new Set(
      getPublishedBlogs()
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
