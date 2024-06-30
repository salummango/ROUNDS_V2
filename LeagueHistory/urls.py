from django.urls import path
from .admin import download_csv
from .views import view_csv
urlpatterns = [
    # Other URLs
    path('admin/leaguhistory/historicalfixturefile/download/', download_csv, name='download_csv'),
    path('view-csv/<int:file_id>/', view_csv, name='view_csv'),
]


