from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import HistoricalFixtureFile

def view_csv(request, file_id):
    fixture_file = get_object_or_404(HistoricalFixtureFile, id=file_id)
    file_path = fixture_file.file.path

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/csv')
        response['Content-Disposition'] = f'inline; filename={fixture_file.file.name}'
        return response
