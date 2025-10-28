# Blog System Guide

Complete guide for using the blog system in your portfolio.

## Overview

The blog system uses:
- **JSON data structure** in `src/data/blogs.ts` for metadata
- **Markdown files** in `/public/all_blogs_files/` for content
- **Pagination system** (configurable posts per page)
- **New Blogs** and **Top Blogs** sections
- **Empty state** with future topics when no blogs exist

## Complete JSON Structure Example

Here's a full example of `src/data/blogs.ts` with multiple blog posts:

```typescript
export const blogsData: BlogsData = {
  "metadata": {
    "site_title": "Tech Blog",
    "site_description": "Insights on Software Development, AI, and Technology",
    "posts_per_page": 6,
    "author_default": "Utsho Dey",
    "author_image_default": "/images/profile.jpg"
  },

  "blogs": [
    // Blog Post 1: Featured Professional Article
    {
      "id": "intro-to-fastapi",
      "file_name": "intro-to-fastapi.md",
      "title": "Introduction to FastAPI: Building High-Performance Python APIs",
      "slug": "intro-to-fastapi",
      "description": "Learn how to build lightning-fast APIs with FastAPI, exploring its key features, async support, and best practices for production deployment.",
      "author": "Utsho Dey",
      "author_image": "/images/profile.jpg",
      "published_date": "2025-01-15",
      "updated_date": "2025-01-16",
      "read_time": 8,
      "cover_image": "/images/blog/fastapi-cover.jpg",
      "tags": ["Python", "FastAPI", "Backend", "API Development", "Async"],
      "categories": ["Backend Development", "Python", "Web Development"],
      "is_featured": true,
      "is_top_blog": true,
      "views": 1250,
      "likes": 89,
      "is_draft": false,
      "is_visible": true,
      "seo_keywords": ["fastapi tutorial", "python api", "async python"],
      "display_order": 1
    },

    // Blog Post 2: Machine Learning Article
    {
      "id": "ml-deployment-guide",
      "file_name": "ml-deployment-guide.md",
      "title": "Deploying Machine Learning Models: A Complete Guide",
      "slug": "ml-deployment-guide",
      "description": "A comprehensive guide to deploying ML models in production using Docker, FastAPI, and cloud services.",
      "author": "Utsho Dey",
      "published_date": "2025-01-10",
      "read_time": 12,
      "cover_image": "/images/blog/ml-deployment.jpg",
      "tags": ["Machine Learning", "Docker", "FastAPI", "DevOps", "Cloud"],
      "categories": ["Machine Learning", "DevOps"],
      "is_featured": false,
      "is_top_blog": true,
      "views": 980,
      "likes": 67,
      "is_draft": false,
      "is_visible": true,
      "display_order": 2
    },

    // Blog Post 3: System Design Article
    {
      "id": "microservices-architecture",
      "file_name": "microservices-architecture.md",
      "title": "Building Scalable Microservices: Best Practices and Patterns",
      "description": "Explore microservices architecture patterns, communication strategies, and real-world implementation examples.",
      "author": "Utsho Dey",
      "published_date": "2025-01-05",
      "read_time": 15,
      "cover_image": "/images/blog/microservices.jpg",
      "tags": ["Microservices", "Architecture", "System Design", "Backend"],
      "categories": ["System Design", "Backend Development"],
      "is_featured": true,
      "is_top_blog": false,
      "views": 1520,
      "likes": 102,
      "is_draft": false,
      "is_visible": true,
      "display_order": 3
    },

    // Blog Post 4: Tutorial
    {
      "id": "docker-kubernetes-tutorial",
      "file_name": "docker-kubernetes-tutorial.md",
      "title": "Docker and Kubernetes: Complete Beginner's Guide",
      "description": "Learn containerization with Docker and orchestration with Kubernetes from scratch.",
      "published_date": "2024-12-28",
      "read_time": 20,
      "tags": ["Docker", "Kubernetes", "DevOps", "Tutorial"],
      "categories": ["DevOps", "Cloud"],
      "is_visible": true,
      "display_order": 4
    },

    // Blog Post 5: Draft Example (Not Visible)
    {
      "id": "upcoming-ai-trends",
      "file_name": "upcoming-ai-trends.md",
      "title": "AI Trends to Watch in 2025",
      "description": "Exploring the most exciting AI developments and trends for the coming year.",
      "published_date": "2025-01-20",
      "read_time": 10,
      "tags": ["AI", "Machine Learning", "Trends"],
      "categories": ["Artificial Intelligence"],
      "is_draft": true,  // This won't be shown publicly
      "is_visible": true,
      "display_order": 5
    },

    // Blog Post 6: Quick Tip/Short Article
    {
      "id": "python-decorators-explained",
      "file_name": "python-decorators-explained.md",
      "title": "Python Decorators Explained in 5 Minutes",
      "description": "A quick and practical guide to understanding and using Python decorators.",
      "published_date": "2024-12-20",
      "read_time": 5,
      "cover_image": "/images/blog/python-decorators.jpg",
      "tags": ["Python", "Programming", "Quick Tip"],
      "categories": ["Python", "Programming Basics"],
      "is_visible": true,
      "display_order": 6
    }
  ],

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
```

## Features

### 1. Pagination System
- Configure posts per page in `metadata.posts_per_page`
- Automatic pagination generation
- Page navigation controls

### 2. New Blogs Section
- Shows most recent posts
- Displayed on the first page only
- Sorted by publication date

### 3. Top Blogs Section
- Shows featured or popular posts
- Based on `is_top_blog` flag or `views` count
- Displayed on the first page only

### 4. Empty State
- Shows future topics when no blogs exist
- Gives visitors insight into upcoming content
- Professional "Coming Soon" message

### 5. Builder Pattern
- All fields are optional (except `file_name` and `title`)
- Gracefully handles missing data
- No breaking if fields are removed

## Usage Examples

### Adding a Simple Blog Post

Minimum required fields:

```typescript
{
  "file_name": "my-blog-post.md",
  "title": "My Blog Post Title",
  "is_visible": true
}
```

### Adding a Featured Blog Post

With all bells and whistles:

```typescript
{
  "id": "comprehensive-guide",
  "file_name": "comprehensive-guide.md",
  "title": "The Complete Guide to X",
  "slug": "complete-guide-to-x",
  "description": "Everything you need to know about X",
  "author": "Your Name",
  "author_image": "/images/author.jpg",
  "published_date": "2025-01-20",
  "read_time": 15,
  "cover_image": "/images/blog/guide-cover.jpg",
  "tags": ["Tutorial", "Guide", "X"],
  "categories": ["Tutorials"],
  "is_featured": true,
  "is_top_blog": true,
  "views": 0,
  "likes": 0,
  "is_visible": true,
  "display_order": 1
}
```

## File Organization

```
portfolio/
├── src/
│   ├── data/
│   │   └── blogs.ts                    # Blog metadata
│   ├── components/
│   │   └── ui/
│   │       └── BlogCard.astro         # Blog card component
│   └── pages/
│       └── blog/
│           ├── [page].astro           # Blog listing with pagination
│           └── [slug].astro           # Individual blog post
├── public/
│   ├── all_blogs_files/               # Markdown blog files
│   │   ├── .gitkeep
│   │   ├── README.md
│   │   ├── intro-to-fastapi.md
│   │   └── ... (your .md files)
│   └── images/
│       └── blog/                      # Blog cover images
│           └── ... (your images)
└── BLOG_SYSTEM_GUIDE.md              # This file
```

## Pagination Configuration

Edit `src/data/blogs.ts`:

```typescript
"metadata": {
  "posts_per_page": 6  // Change this number
}
```

## Customizing Future Topics

Edit the `future_topics` array in `src/data/blogs.ts`:

```typescript
"future_topics": [
  {
    "topic": "Your Topic",
    "description": "Description of what you'll write about",
    "icon": "🎯"  // Any emoji
  }
]
```

## Helper Functions Available

All these functions are exported from `src/data/blogs.ts`:

- `getPublishedBlogs()` - Get all published blogs
- `getNewBlogs(limit)` - Get most recent blogs
- `getTopBlogs(limit)` - Get top/featured blogs
- `getBlogsByCategory(category)` - Filter by category
- `getBlogsByTag(tag)` - Filter by tag
- `getPaginatedBlogs(page, perPage)` - Get paginated results
- `getAllCategories()` - Get all unique categories
- `getAllTags()` - Get all unique tags

## URLs

- Blog listing page 1: `/blog/1`
- Blog listing page 2: `/blog/2`
- Individual blog post: `/blog/{slug}`

## Next Steps

1. ✅ JSON structure created
2. ✅ Blog system implemented
3. ✅ Pagination working
4. ✅ Empty state with future topics
5. ✅ New blogs and top blogs sections
6. 📝 Create your first blog post in `/public/all_blogs_files/`
7. 📝 Add blog metadata to `src/data/blogs.ts`
8. 🎨 Customize empty state message
9. 📸 Add cover images to `/public/images/blog/`

## Tips

- Start with `is_draft: true` while writing
- Use descriptive slugs for SEO
- Add relevant tags and categories
- Include cover images for better engagement
- Set realistic read times (250 words/min)
- Mark your best posts as `is_featured: true`

Happy blogging! 🚀
