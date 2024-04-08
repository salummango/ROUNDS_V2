from django.contrib import admin
from .models import User,Team
from league.admin import generate_fixtures

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email','first_name','last_name','phoneNo','team']
    list_display = ['email','first_name','last_name','phoneNo','team','is_active']

class TeamAdmin(admin.ModelAdmin):
    actions = [generate_fixtures]
    
    search_fields = ['TeamName','TeamStadium','TeamCity']
    list_display = ['TeamName','TeamStadium','TeamCity']
    
admin.site.register(User,UserAdmin)
admin.site.register(Team,TeamAdmin)