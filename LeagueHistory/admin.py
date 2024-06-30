from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .models import HistoricalFixtureFile
from django.utils.html import format_html
from django.urls import reverse

def download_csv(modeladmin, request, queryset):
    for fixture_file in queryset:
        file_path = fixture_file.file.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={fixture_file.file.name}'
            return response

download_csv.short_description = "Download selected CSV files"

class HistoricalFixtureFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at', 'view_file', 'download_file')
    search_fields = ['file']
    readonly_fields = ('uploaded_at',)
    actions = [download_csv]

    def view_file(self, obj):
        return format_html('<a href="{}" target="_blank">View</a>', reverse('view_csv', args=[obj.id]))

    def download_file(self, obj):
        return format_html('<a href="{}" download>Download</a>', obj.file.url)

    view_file.short_description = "View File"
    download_file.short_description = "Download File"

admin.site.register(HistoricalFixtureFile, HistoricalFixtureFileAdmin)
