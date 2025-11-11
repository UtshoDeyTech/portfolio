"""
Backup and Restore Utilities for Portfolio Data
Handles export/import of all portfolio data including JSON, markdown files, and media.
"""

import os
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from django.core import serializers
from django.conf import settings
from django.core.files.storage import default_storage


def export_portfolio_data(export_dir=None):
    """
    Export all portfolio data to a directory structure.
    Returns the path to the created zip file.
    Raises exceptions with detailed messages if export fails.
    """
    from .models import (
        EducationEntry, ExperienceEntry, Project, ResearchPublication,
        ResearchIcon, HomeData, Blog, BlogComment, BlogsData,
        BlogSettings, MediaFile
    )

    try:
        # Create export directory
        if export_dir is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_dir = Path(settings.BASE_DIR) / 'exports' / f'portfolio_backup_{timestamp}'
        else:
            export_dir = Path(export_dir)

        export_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise Exception(f"Failed to create export directory: {type(e).__name__}: {str(e)}")

    # 1. Export all models as JSON
    try:
        json_dir = export_dir / 'json_data'
        json_dir.mkdir(exist_ok=True)

        models_to_export = [
            ('education', EducationEntry),
            ('experience', ExperienceEntry),
            ('projects', Project),
            ('research', ResearchPublication),
            ('research_icons', ResearchIcon),
            ('home_data', HomeData),
            ('blogs', Blog),
            ('blog_comments', BlogComment),
            ('blogs_data', BlogsData),
            ('blog_settings', BlogSettings),
            ('media_files', MediaFile),
        ]

        for name, model in models_to_export:
            try:
                data = serializers.serialize('json', model.objects.all(), indent=2)
                with open(json_dir / f'{name}.json', 'w', encoding='utf-8') as f:
                    f.write(data)
            except Exception as e:
                raise Exception(f"Failed to export {name}: {type(e).__name__}: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to export JSON data: {str(e)}")

    # 2. Export blogs as markdown files
    blogs_dir = export_dir / 'blogs_markdown'
    blogs_dir.mkdir(exist_ok=True)

    for blog in Blog.objects.all():
        # Create safe filename from slug
        filename = f"{blog.slug}.md"
        filepath = blogs_dir / filename

        # Create markdown content with frontmatter
        content = f"""---
title: {blog.title}
subtitle: {blog.subtitle}
slug: {blog.slug}
author: {blog.author}
published_date: {blog.published_date}
category: {blog.category}
tags: {json.dumps(blog.tags)}
is_published: {blog.is_published}
is_featured: {blog.is_featured}
is_trending: {blog.is_trending}
views: {blog.views}
likes: {blog.likes}
read_time: {blog.read_time}
cover_image: {blog.cover_image}
---

{blog.content_markdown}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    # 3. Export media files
    media_dir = export_dir / 'media_files'
    media_dir.mkdir(exist_ok=True)

    # Copy all uploaded media files
    media_root = Path(settings.MEDIA_ROOT)
    if media_root.exists():
        for item in media_root.rglob('*'):
            if item.is_file():
                # Preserve directory structure
                relative_path = item.relative_to(media_root)
                dest_path = media_dir / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)

    # 4. Create a manifest file with metadata
    manifest = {
        'export_date': datetime.now().isoformat(),
        'django_version': '5.2.8',  # Update as needed
        'models_exported': [name for name, _ in models_to_export],
        'total_blogs': Blog.objects.count(),
        'total_media_files': MediaFile.objects.count(),
        'total_education_entries': EducationEntry.objects.count(),
        'total_experience_entries': ExperienceEntry.objects.count(),
        'total_projects': Project.objects.count(),
        'total_research_publications': ResearchPublication.objects.count(),
    }

    with open(export_dir / 'manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    # 5. Create README
    readme_content = f"""# Portfolio Data Backup
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Contents:
- json_data/: All database models exported as JSON
- blogs_markdown/: Blog posts in Markdown format
- media_files/: All uploaded media files (images, documents, etc.)
- manifest.json: Backup metadata

## To Restore:
1. Upload this zip file to your Django admin panel
2. Go to: /admin/portfolio-import/
3. Select the zip file and click "Import"
4. All data will be restored to the database

## Models Included:
- Education Entries: {EducationEntry.objects.count()}
- Experience Entries: {ExperienceEntry.objects.count()}
- Projects: {Project.objects.count()}
- Research Publications: {ResearchPublication.objects.count()}
- Blog Posts: {Blog.objects.count()}
- Media Files: {MediaFile.objects.count()}
- Home Page Data: {HomeData.objects.count()}

WARNING: Importing will overwrite existing data!
"""

    with open(export_dir / 'README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)

    # 6. Create ZIP file
    zip_path = export_dir.parent / f'{export_dir.name}.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, export_dir)
                zipf.write(file_path, arcname)

    # 7. Clean up temporary directory
    shutil.rmtree(export_dir)

    return zip_path


def import_portfolio_data(zip_path, overwrite=False):
    """
    Import portfolio data from a backup zip file.

    Args:
        zip_path: Path to the backup zip file
        overwrite: If True, will overwrite existing data

    Returns:
        dict: Import results with counts and status
    """
    from .models import (
        EducationEntry, ExperienceEntry, Project, ResearchPublication,
        ResearchIcon, HomeData, Blog, BlogComment, BlogsData,
        BlogSettings, MediaFile
    )
    from django.core import serializers as django_serializers

    # Extract zip to temporary directory
    import_dir = Path(settings.BASE_DIR) / 'temp_import'
    if import_dir.exists():
        shutil.rmtree(import_dir)
    import_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(import_dir)

    results = {
        'success': True,
        'imported': {},
        'errors': [],
    }

    try:
        # Read manifest
        manifest_path = import_dir / 'manifest.json'
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
                results['manifest'] = manifest

        # Clear existing data if overwrite is True
        if overwrite:
            models_to_clear = [
                BlogComment,  # Delete first (has FK to Blog)
                Blog,
                BlogsData,
                BlogSettings,
                MediaFile,
                Project,
                ResearchPublication,
                ResearchIcon,
                ExperienceEntry,
                EducationEntry,
                HomeData,  # Singleton, delete last
            ]
            for model in models_to_clear:
                count = model.objects.count()
                model.objects.all().delete()
                results['imported'][f'{model.__name__}_deleted'] = count

        # Import JSON data
        json_dir = import_dir / 'json_data'
        if json_dir.exists():
            json_files = [
                ('education.json', EducationEntry),
                ('experience.json', ExperienceEntry),
                ('projects.json', Project),
                ('research.json', ResearchPublication),
                ('research_icons.json', ResearchIcon),
                ('home_data.json', HomeData),
                ('blog_settings.json', BlogSettings),
                ('blogs_data.json', BlogsData),
                ('blogs.json', Blog),
                ('blog_comments.json', BlogComment),
                ('media_files.json', MediaFile),
            ]

            for filename, model in json_files:
                filepath = json_dir / filename
                if filepath.exists():
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = f.read()
                            objects = django_serializers.deserialize('json', data)
                            count = 0
                            for obj in objects:
                                obj.save()
                                count += 1
                            results['imported'][filename] = count
                    except Exception as e:
                        error_msg = f"Error importing {filename}: {type(e).__name__}: {str(e)}"
                        results['errors'].append(error_msg)
                        results['imported'][filename] = 0

        # Restore media files
        media_dir = import_dir / 'media_files'
        if media_dir.exists():
            media_root = Path(settings.MEDIA_ROOT)
            media_root.mkdir(parents=True, exist_ok=True)

            copied_files = 0
            for item in media_dir.rglob('*'):
                if item.is_file():
                    relative_path = item.relative_to(media_dir)
                    dest_path = media_root / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)
                    copied_files += 1

            results['imported']['media_files_copied'] = copied_files

    except Exception as e:
        results['success'] = False
        results['errors'].append(f"Import failed: {str(e)}")

    finally:
        # Clean up temporary directory
        if import_dir.exists():
            shutil.rmtree(import_dir)

    return results
