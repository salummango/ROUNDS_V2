# In your app's urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('all_match', views.FixtureList, name='all_match'),
    path('team_matches/', views.TeamMatches, name='team_matches'),
    path('TeamManager',views.team_manager_dashboard, name='team_manager_dashboard'),
    path('calendar/',views.calendar_view, name='calendar')
]
