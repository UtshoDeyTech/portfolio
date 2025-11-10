"""
Simple Admin Views for Import/Export Functionality
"""

import os
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse
from django.conf import settings
from pathlib import Path

from .backup_utils import export_portfolio_data, import_portfolio_data


@staff_member_required
def export_portfolio_view(request):
    """
    Export all portfolio data as a ZIP file and download it.
    """
    try:
        # Create export
        zip_path = export_portfolio_data()

        # Send file as download
        if os.path.exists(zip_path):
            response = FileResponse(
                open(zip_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(zip_path)
            )
            messages.success(request, f'✅ Portfolio data exported: {os.path.basename(zip_path)}')
            return response
        else:
            messages.error(request, '❌ Export file was not created.')
            return redirect('admin:api_homedata_change', 1)

    except Exception as e:
        messages.error(request, f'❌ Export failed: {str(e)}')
        return redirect('admin:api_homedata_change', 1)


@staff_member_required
def import_portfolio_view(request):
    """
    Import portfolio data from a ZIP file.
    """
    if request.method != 'POST':
        messages.error(request, '❌ Invalid request method.')
        return redirect('admin:api_homedata_change', 1)

    zip_file = request.FILES.get('backup_file')
    overwrite = request.POST.get('overwrite') == 'yes'

    if not zip_file:
        messages.error(request, '❌ Please select a backup file.')
        return redirect('admin:api_homedata_change', 1)

    if not overwrite:
        messages.error(request, '❌ You must confirm overwrite by checking the checkbox.')
        return redirect('admin:api_homedata_change', 1)

    try:
        # Save uploaded file temporarily
        temp_dir = Path(settings.BASE_DIR) / 'temp_uploads'
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / zip_file.name

        with open(temp_path, 'wb+') as destination:
            for chunk in zip_file.chunks():
                destination.write(chunk)

        # Import data
        results = import_portfolio_data(temp_path, overwrite=overwrite)

        # Clean up
        os.remove(temp_path)
        if temp_dir.exists() and not any(temp_dir.iterdir()):
            temp_dir.rmdir()

        if results['success']:
            message = '✅ Import completed successfully!\n\n'
            message += 'Imported:\n'
            for key, value in results['imported'].items():
                message += f'  • {key}: {value}\n'

            if results.get('errors'):
                message += '\n⚠️ Warnings:\n'
                for error in results['errors']:
                    message += f'  • {error}\n'

            messages.success(request, message)
        else:
            messages.error(request, f"❌ Import failed: {', '.join(results['errors'])}")

    except Exception as e:
        messages.error(request, f'❌ Import failed: {str(e)}')

    return redirect('admin:api_homedata_change', 1)
