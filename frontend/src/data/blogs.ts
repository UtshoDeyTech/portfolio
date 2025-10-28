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

export interface BlogPost {
  id?: string;                          // Unique identifier
  file_name: string;                    // Name of the .md file (without path)
  title: string;                        // Blog post title
  slug?: string;                        // URL-friendly slug (auto-generated from file_name if not provided)
  description?: string;                 // Short description/excerpt
  author?: string;                      // Author name
  author_image?: string;                // Author profile image URL
  published_date?: string;              // Publication date (e.g., "2025-01-15")
  updated_date?: string;                // Last updated date
  read_time?: number;                   // Estimated read time in minutes
  cover_image?: string;                 // Cover image URL
  tags?: string[];                      // Array of tags
  categories?: string[];                // Array of categories/topics
  is_featured?: boolean;                // Featured post flag
  is_top_blog?: boolean;                // Mark as top blog
  views?: number;                       // View count
  likes?: number;                       // Like count
  is_draft?: boolean;                   // Draft mode (won't be displayed if true)
  is_visible?: boolean;                 // Visibility flag (default: true)
  seo_keywords?: string[];              // SEO keywords
  display_order?: number;               // Custom display order
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

export const blogsData: BlogsData = {
  "metadata": {
    "site_title": "Tech Blog",
    "site_description": "Insights on Software Development, AI, and Technology",
    "posts_per_page": 6,
    "author_default": "Utsho Dey",
    "author_image_default": "/images/profile.jpg"
  },

  "blogs": [
    // Example blog post structure (currently empty - add your blogs here)
    // {
    //   "id": "intro-to-fastapi",
    //   "file_name": "intro-to-fastapi.md",
    //   "title": "Introduction to FastAPI: Building High-Performance Python APIs",
    //   "slug": "intro-to-fastapi",
    //   "description": "Learn how to build lightning-fast APIs with FastAPI, exploring its key features and best practices.",
    //   "author": "Utsho Dey",
    //   "published_date": "2025-01-15",
    //   "read_time": 8,
    //   "cover_image": "/images/blog/fastapi-cover.jpg",
    //   "tags": ["Python", "FastAPI", "Backend", "API Development"],
    //   "categories": ["Backend Development", "Python"],
    //   "is_featured": true,
    //   "is_top_blog": true,
    //   "views": 1250,
    //   "likes": 89,
    //   "is_draft": false,
    //   "is_visible": true
    // }
  ],

  /**
   * Future Blog Topics
   *
   * These topics will be displayed when the blog section is empty,
   * giving visitors an idea of what content to expect in the future.
   */
  "future_topics": [
    {
      "topic": "Machine Learning & AI",
      "description": "Deep dives into ML algorithms, LLM integration, prompt engineering, and practical AI applications in real-world projects.",
      "icon": "🤖"
    },
    {
      "topic": "Backend Development",
      "description": "Best practices for building scalable backend systems with Python, FastAPI, Spring Boot, microservices architecture, and database optimization.",
      "icon": "⚙️"
    },
    {
      "topic": "Cloud & DevOps",
      "description": "Tutorials on Docker, Kubernetes, CI/CD pipelines, AWS services, and modern deployment strategies.",
      "icon": "☁️"
    },
    {
      "topic": "System Design",
      "description": "Exploring distributed systems, scalability patterns, database design, and architectural decisions for enterprise applications.",
      "icon": "🏗️"
    },
    {
      "topic": "Full Stack Development",
      "description": "End-to-end development guides covering frontend frameworks (React), backend APIs, database management, and deployment.",
      "icon": "💻"
    },
    {
      "topic": "Data Science & Analytics",
      "description": "Data preprocessing, visualization, statistical analysis, and building recommendation systems.",
      "icon": "📊"
    },
    {
      "topic": "Software Engineering Best Practices",
      "description": "Code quality, testing strategies, design patterns, SOLID principles, and maintaining clean codebases.",
      "icon": "✨"
    },
    {
      "topic": "Career & Learning",
      "description": "Tips for career growth in tech, learning resources, interview preparation, and navigating the software engineering landscape.",
      "icon": "🚀"
    }
  ]
};

/**
 * Helper Functions
 */

// Get all published blogs
export const getPublishedBlogs = () => {
  return blogsData.blogs.filter(
    blog => blog.is_visible !== false && blog.is_draft !== true
  );
};

// Get new blogs (most recent)
export const getNewBlogs = (limit: number = 5) => {
  return getPublishedBlogs()
    .sort((a, b) => {
      const dateA = a.published_date || '0';
      const dateB = b.published_date || '0';
      return dateB.localeCompare(dateA);
    })
    .slice(0, limit);
};

// Get top blogs (by views or featured)
export const getTopBlogs = (limit: number = 5) => {
  return getPublishedBlogs()
    .filter(blog => blog.is_top_blog === true || blog.is_featured === true)
    .sort((a, b) => {
      // Sort by views first, then by likes
      const viewsA = a.views || 0;
      const viewsB = b.views || 0;
      if (viewsA !== viewsB) return viewsB - viewsA;
      return (b.likes || 0) - (a.likes || 0);
    })
    .slice(0, limit);
};

// Get blogs by category
export const getBlogsByCategory = (category: string) => {
  return getPublishedBlogs().filter(
    blog => blog.categories?.includes(category)
  );
};

// Get blogs by tag
export const getBlogsByTag = (tag: string) => {
  return getPublishedBlogs().filter(
    blog => blog.tags?.includes(tag)
  );
};

// Get paginated blogs
export const getPaginatedBlogs = (page: number = 1, perPage?: number) => {
  const postsPerPage = perPage || blogsData.metadata.posts_per_page;
  const allBlogs = getPublishedBlogs().sort((a, b) => {
    // Sort by display_order first, then by date
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
    hasPrevPage: page > 1
  };
};

// Get all unique categories
export const getAllCategories = () => {
  return Array.from(
    new Set(
      getPublishedBlogs()
        .flatMap(blog => blog.categories || [])
        .filter(cat => cat && cat.trim() !== '')
    )
  ).sort();
};

// Get all unique tags
export const getAllTags = () => {
  return Array.from(
    new Set(
      getPublishedBlogs()
        .flatMap(blog => blog.tags || [])
        .filter(tag => tag && tag.trim() !== '')
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
