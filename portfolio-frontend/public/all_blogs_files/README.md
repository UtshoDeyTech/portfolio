# Blog Posts Directory

This folder contains all blog post markdown files for your portfolio website.

## Quick Start

### Adding a New Blog Post

1. **Create the Markdown File**
   - Create a new `.md` file in this directory
   - Example: `intro-to-fastapi.md`

2. **Write Your Content**
   ```markdown
   # Introduction to FastAPI

   FastAPI is a modern, fast web framework for building APIs with Python...

   ## Why FastAPI?

   - Fast performance
   - Easy to learn
   - Automatic documentation

   ## Code Example

   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   def read_root():
       return {"Hello": "World"}
   ```

   ## Conclusion

   FastAPI is an excellent choice for building Python APIs...
   ```

3. **Add Metadata to `src/data/blogs.ts`**
   ```typescript
   {
     "id": "intro-to-fastapi",
     "file_name": "intro-to-fastapi.md",
     "title": "Introduction to FastAPI: Building High-Performance APIs",
     "description": "Learn how to build lightning-fast APIs with FastAPI",
     "author": "Your Name",
     "published_date": "2025-01-15",
     "read_time": 8,
     "cover_image": "/images/blog/fastapi-cover.jpg",
     "tags": ["Python", "FastAPI", "Backend"],
     "categories": ["Backend Development"],
     "is_featured": true,
     "is_visible": true
   }
   ```

## File Structure

```
all_blogs_files/
├── .gitkeep
├── README.md                          # This file
├── intro-to-fastapi.md               # Example blog post
├── machine-learning-basics.md        # Another blog post
└── ... (your blog posts)
```

## Markdown Features Supported

- **Headings**: `# H1`, `## H2`, `### H3`
- **Bold**: `**bold text**`
- **Italic**: `*italic text*`
- **Links**: `[link text](url)`
- **Images**: `![alt text](/images/blog/image.jpg)`
- **Code blocks**: ` ```language ... ``` `
- **Lists**: Bulleted and numbered
- **Blockquotes**: `> quote`
- **Tables**
- **Horizontal rules**: `---`

## Blog Metadata Fields

All fields in `src/data/blogs.ts` are optional except `file_name` and `title`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `file_name` | string | **Required** - Name of .md file |
| `title` | string | **Required** - Blog title |
| `slug` | string | URL slug (auto-generated if not provided) |
| `description` | string | Short excerpt/description |
| `author` | string | Author name |
| `published_date` | string | Date in YYYY-MM-DD format |
| `read_time` | number | Estimated read time in minutes |
| `cover_image` | string | Cover image URL |
| `tags` | array | Array of tag strings |
| `categories` | array | Array of category strings |
| `is_featured` | boolean | Mark as featured |
| `is_top_blog` | boolean | Show in "Top Blogs" section |
| `views` | number | View count |
| `likes` | number | Like count |
| `is_draft` | boolean | Hide from public (draft mode) |
| `is_visible` | boolean | Control visibility |

## Tips

1. **Images**: Store blog images in `/public/images/blog/`
2. **Drafts**: Set `is_draft: true` to hide unfinished posts
3. **Featured**: Set `is_featured: true` for important posts
4. **SEO**: Use descriptive titles and add relevant tags
5. **Read Time**: Estimate 200-250 words per minute

## Example Blog Post Structure

```markdown
# Main Title

Brief introduction paragraph...

## Section 1

Content for section 1...

### Subsection

More detailed content...

## Section 2

More content with code examples:

```python
def example():
    return "Hello World"
```

## Conclusion

Wrap up your post...

---

*Tags: Python, Tutorial, Backend*
```

## Need Help?

- Check existing blog files for examples
- Markdown guide: https://www.markdownguide.org/
- Edit `src/data/blogs.ts` to add metadata
