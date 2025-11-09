# API Endpoints — Response Schemas

This file documents the API endpoints exposed by the `api` app and the JSON shape each endpoint returns. Use these schemas to integrate the frontend UI.

Base URL: /api/ (adjust if you mounted the router differently)

Notes:
- All date fields are returned as strings (e.g., "2025-10-27" or "Oct 2025").
- Fields marked `nullable` may be `null` in JSON.
- JSON arrays and objects use native JSON types (Array/Object).

---

## GET /api/education/
Returns: array of EducationEntry objects (list)

Each EducationEntry:
- id: integer
- institution: string
- degree: string
- field_of_study: string
- education_type: string
- start_date: string
- end_date: string | null
- grade: string
- grade_scale: string
- location: string
- is_current: boolean
- institution_logo_url: string
- description: string
- achievements: array of strings
- certificate_url: string
- is_visible: boolean
- display_order: integer
- created_at: string (ISO datetime)
- updated_at: string (ISO datetime)

Example response (array):
```
[
  {
    "id": 1,
    "institution": "BRAC University",
    "degree": "Master's degree",
    "field_of_study": "Computer Science",
    "education_type": "Graduate",
    "start_date": "Mar 2024",
    "end_date": "Aug 2025",
    "grade": "3.75",
    "grade_scale": "4.00",
    "location": "Dhaka, Bangladesh",
    "is_current": true,
    "institution_logo_url": "https://...png",
    "description": "Specializing...",
    "achievements": ["Maintained CGPA 3.75"],
    "certificate_url": "",
    "is_visible": true,
    "display_order": 1,
    "created_at": "2025-10-30T00:00:00Z",
    "updated_at": "2025-10-30T00:00:00Z"
  }
]
```

---

## GET /api/education/{id}/
Returns: single EducationEntry object (same fields as above)

---

## GET /api/experience/
Returns: array of ExperienceEntry objects

Fields per entry:
- id: integer
- company_name: string
- company_logo_url: string
- role: string
- employment_type: string
- location: string
- work_mode: string
- start_date: string
- end_date: string | null
- is_current: boolean
- description: string
- achievements: array of strings
- skills: array of strings
- tech_stack: array of strings
- is_visible: boolean
- display_order: integer
- created_at, updated_at: string datetimes

Example (single):
```
{
  "id": 1,
  "company_name": "LEADS Corporation Limited",
  "company_logo_url": "",
  "role": "Senior Software Engineer",
  "employment_type": "Full-time",
  "location": "Dhaka, Bangladesh",
  "work_mode": "On-site",
  "start_date": "Oct 2025",
  "end_date": null,
  "is_current": true,
  "description": "Working as...",
  "achievements": ["Implemented secure microservice..."],
  "skills": ["Spring Boot", "Java"],
  "tech_stack": ["Java 17", "Spring Boot"],
  "is_visible": true,
  "display_order": 1,
  "created_at": "2025-10-30T00:00:00Z",
  "updated_at": "2025-10-30T00:00:00Z"
}
```

---

## GET /api/experience/{id}/
Returns: single ExperienceEntry (same fields as list)

---

## GET /api/projects/
Returns: array of Project objects

Project fields:
- id: integer
- slug: string
- title: string
- organization: string
- role: string
- start_date: string
- end_date: string | null
- type: string
- short_description: string
- responsibilities: array of strings
- achievements: array of strings
- skills: array of strings
- tech_stack: object or array (depends on record; treat as JSON object)
- project_url: string
- github_url: string
- contributor_count: integer
- collaboration: string
- tags: array of strings
- is_visible: boolean
- display_order: integer
- created_at, updated_at: string datetimes

Example project (minimal):
```
{
  "id": 1,
  "slug": "askken_ai",
  "title": "AskKen.ai",
  "organization": "InalyZe Bangladesh Ltd.",
  "role": "Lead Backend Developer",
  "start_date": "Sep 2024",
  "end_date": "Present",
  "type": "Professional",
  "short_description": "Advanced multi-tenant...",
  "responsibilities": ["Led backend architecture..."],
  "achievements": ["Reduced latency by 40%"],
  "skills": ["FastAPI", "Python"],
  "tech_stack": {"backend": ["FastAPI"]},
  "project_url": "https://askken.ai",
  "github_url": "https://github.com/...",
  "contributor_count": 4,
  "collaboration": "Led a team...",
  "tags": ["AI", "LLM"],
  "is_visible": true,
  "display_order": 1,
  "created_at": "2025-10-30T00:00:00Z",
  "updated_at": "2025-10-30T00:00:00Z"
}
```

---

## GET /api/projects/{slug}/
Returns: single Project object (same fields as list)

---

## GET /api/research/
Returns: array of ResearchPublication objects

Fields per publication:
- id: integer
- slug: string
- title: string
- authors: array of strings
- publication_date: string
- institution: string
- publication_type: string
- description: string
- objectives: array of strings
- dataset: string
- metrics: array of strings
- comparison_models: array of strings
- results_summary: string
- highlights: array of strings
- tags: array of strings
- url: string
- is_visible: boolean
- display_order: integer
- cover_image: string
- created_at, updated_at: string

Example:
```
{
  "id": 1,
  "slug": "skin_cancer_cnn_research",
  "title": "Application of Deep CNN...",
  "authors": ["Nadia Shafique", "Utsho Dey"],
  "publication_date": "2023",
  "institution": "Brac University",
  "publication_type": "Undergraduate Thesis / Research Paper",
  "description": "This research proposes...",
  "objectives": ["Develop a custom CNN model..."],
  "dataset": "HAM10000",
  "metrics": ["Accuracy"],
  "comparison_models": ["ResNet50"],
  "results_summary": "The proposed model...",
  "highlights": ["Improved test accuracy"],
  "tags": ["Deep Learning"],
  "url": "https://scholar.google.com/...",
  "is_visible": true,
  "display_order": 1
}
```

---

## GET /api/research/{slug}/
Returns: single ResearchPublication object (same fields)

---

## GET /api/research-icons/
Returns: array of ResearchIcon objects

ResearchIcon fields:
- id: integer
- key: string (unique)
- path: string (SVG path or long string)
- title: string

Example:
```
{
  "id": 1,
  "key": "computer-science",
  "path": "M9 17.25v1.007...",
  "title": "Computer Science"
}
```

---

## GET /api/home/
Returns: singleton HomeData record `{ data: <object> }`

Shape: `data` is an object containing multiple sections used by the UI. Typical keys:
- hero: object (name, tagline, bio, profile_image, resume_url, cta_buttons)
- about: object (title, paragraphs[], highlights[])
- stats: object (years_of_experience, projects_completed, publications, technologies_used)
- skills: object (title, categories[] where each category has name, icon, skills[])
- social_links: object (github, linkedin, email, scholar)
- cta: object
- featured_sections: object of booleans

Example response:
```
{
  "id": 1,
  "data": {
    "hero": {"name":"Utsho Dey","tagline":"...","profile_image":"/images/profile.jpg"},
    "about": {"title":"About Me","paragraphs": ["..."], "highlights": ["..."]},
    "skills": {"title":"Technical Skills","categories": [...]}
  }
}
```

Note: The UI should treat `data` as an opaque object and map fields it needs.

---

## GET /api/blogs/
Returns: singleton BlogsData record `{ metadata: {...}, blogs: [...], future_topics: [...] }`

- metadata: object (site_title, site_description, posts_per_page, author_default, author_image_default, etc.)
- blogs: array of blog objects (each blog may have title, summary, date, tags, url, content, etc.)
- future_topics: array of objects { topic, description, icon }

Example:
```
{
  "id": 1,
  "metadata": {"site_title": "Tech Blog", "posts_per_page": 6},
  "blogs": [],
  "future_topics": [{"topic": "Machine Learning & AI", "description": "...", "icon": "🤖"}]
}
```

---

## Integration tips
- Sorting: use `display_order` to order items where provided. Many models also have `is_visible` to hide items in the UI.
- Detail pages: Projects and Research use `slug` for the detail endpoint.
- Nullables: `end_date` is often null for current items.
- Timestamps: `created_at` and `updated_at` are ISO datetimes.

## Quick test commands
Start dev server and fetch endpoints locally:

```pwsh
python manage.py runserver
# then (example):
curl http://127.0.0.1:8000/api/education/
curl http://127.0.0.1:8000/api/projects/askken_ai/
```

---

If you want, I can also generate JSON Schema (OpenAPI components) for each response so you can auto-generate TypeScript types for the frontend — would you like that?
