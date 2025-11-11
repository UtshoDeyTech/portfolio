"""
Backup and Restore Utilities for Portfolio Data
Handles export/import of all portfolio data including JSON, markdown files, and media.
Auto-detects all models in the 'api' app for export/import.
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
from django.apps import apps


def get_exportable_models():
    """
    Auto-detect all models in the 'api' app that should be exported.
    Returns a list of tuples: (json_filename, Model, priority)

    Priority determines import/export order:
    - Lower priority = exported/imported first
    - Higher priority = exported/imported last

    Models with foreign keys should have higher priority to be deleted first
    and imported last.
    """
    api_config = apps.get_app_config('api')
    models = []

    # Define manual priorities for models with known dependencies
    # Higher priority = more dependencies (should be deleted first, imported last)
    priority_map = {
        'BlogComment': 100,  # Has FK to Blog
        'BlogView': 100,     # Has FK to Blog
        'BlogLike': 100,     # Has FK to Blog
        'Blog': 50,          # Referenced by BlogComment, BlogView, BlogLike
        'MediaFile': 30,
        'Project': 30,
        'ResearchPublication': 30,
        'ExperienceEntry': 30,
        'EducationEntry': 30,
        'ResearchIcon': 20,
        'BlogSettings': 20,
        'BlogsData': 20,
        'HomeData': 10,      # Singleton, usually independent
        'NewsletterSubscriber': 10,  # Independent
    }

    for model in api_config.get_models():
        # Skip proxy models and models that shouldn't be exported
        if model._meta.proxy or not model._meta.managed:
            continue

        model_name = model.__name__

        # Skip system/internal models if any
        if model_name.startswith('_'):
            continue

        # Get priority (default to 25 if not specified)
        priority = priority_map.get(model_name, 25)

        # Create filename from model name
        # Convert CamelCase to snake_case
        filename = ''.join(['_' + c.lower() if c.isupper() else c for c in model_name]).lstrip('_')

        models.append((filename, model, priority))

    # Sort by priority (ascending) for export order
    # Lower priority models are exported first
    models.sort(key=lambda x: x[2])

    return models


def export_portfolio_data(export_dir=None):
    """
    Export all portfolio data to a directory structure.
    Returns the path to the created zip file.
    Raises exceptions with detailed messages if export fails.
    Auto-detects all models in the 'api' app for export.
    """
    from .models import Blog

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

    # Get all exportable models (auto-detected)
    models_to_export = get_exportable_models()

    # 1. Export all models as JSON
    try:
        json_dir = export_dir / 'json_data'
        json_dir.mkdir(exist_ok=True)

        for filename, model, priority in models_to_export:
            try:
                data = serializers.serialize('json', model.objects.all(), indent=2)
                with open(json_dir / f'{filename}.json', 'w', encoding='utf-8') as f:
                    f.write(data)
            except Exception as e:
                raise Exception(f"Failed to export {filename}: {type(e).__name__}: {str(e)}")
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
    model_counts = {}
    for filename, model, priority in models_to_export:
        model_counts[model.__name__] = model.objects.count()

    manifest = {
        'export_date': datetime.now().isoformat(),
        'django_version': '5.2.8',  # Update as needed
        'models_exported': [filename for filename, _, _ in models_to_export],
        'model_counts': model_counts,
    }

    with open(export_dir / 'manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    # 5. Create README
    models_list = '\n'.join([f"- {model.__name__}: {model.objects.count()}"
                             for _, model, _ in models_to_export])

    readme_content = f"""# Portfolio Data Backup
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Contents:
- json_data/: All database models exported as JSON
- blogs_markdown/: Blog posts in Markdown format (if any)
- media_files/: All uploaded media files (images, documents, etc.)
- manifest.json: Backup metadata

## To Restore:
1. Upload this zip file to your Django admin panel
2. Go to: /admin/api/backuprestore/
3. Select the zip file and click "Import Data"
4. All data will be restored to the database

## Models Included:
{models_list}

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
    Auto-detects all models from the exported data.

    Args:
        zip_path: Path to the backup zip file
        overwrite: If True, will overwrite existing data

    Returns:
        dict: Import results with counts and status
    """
    from django.core import serializers as django_serializers

    # Get all exportable models (auto-detected)
    models_info = get_exportable_models()

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
            # Delete in reverse priority order (highest priority first)
            # This ensures models with FKs are deleted before their references
            models_to_clear = sorted(models_info, key=lambda x: x[2], reverse=True)

            for filename, model, priority in models_to_clear:
                try:
                    count = model.objects.count()
                    model.objects.all().delete()
                    results['imported'][f'{model.__name__}_deleted'] = count
                except Exception as e:
                    results['errors'].append(f"Error deleting {model.__name__}: {str(e)}")

        # Import JSON data
        json_dir = import_dir / 'json_data'
        if json_dir.exists():
            # Import in normal priority order (lowest priority first)
            # This ensures independent models are imported before dependent ones
            for filename, model, priority in models_info:
                json_filename = f'{filename}.json'
                filepath = json_dir / json_filename

                if filepath.exists():
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = f.read()
                            objects = django_serializers.deserialize('json', data)
                            count = 0
                            for obj in objects:
                                obj.save()
                                count += 1
                            results['imported'][json_filename] = count
                    except Exception as e:
                        error_msg = f"Error importing {json_filename}: {type(e).__name__}: {str(e)}"
                        results['errors'].append(error_msg)
                        results['imported'][json_filename] = 0

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
