from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import User,Team
from league.admin import generate_fixtures

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email','first_name','last_name','phoneNo','team']
    list_display = ['email','first_name','last_name','phoneNo','team','is_active']
    
    readonly_fields=["userimage"]
    def userimage(self, obj):
        if obj.userImage:
            return mark_safe(f'<img src="{obj.userImage.url}" width="100" height="100" />')
        return "No Image"


class TeamStatusFilter(admin.SimpleListFilter):
    title = 'Team Status'
    parameter_name = 'team_status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('relegate', 'Relegate'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(TeamStatus='active')
        elif self.value() == 'relegate':
            return queryset.filter(TeamStatus='relegate')
        return queryset


class TeamAdmin(admin.ModelAdmin):
    actions = [generate_fixtures]
    
    search_fields = ['TeamName','TeamStadium','TeamCity']
    list_display = ['TeamName','TeamStadium','TeamCity','TeamStatus']
    list_filter = [TeamStatusFilter]
    
admin.site.register(User,UserAdmin)
admin.site.register(Team,TeamAdmin)




# class ReadOnlyAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     # Optional: You can also make the fields read-only in the detail view
#     def get_readonly_fields(self, request, obj=None):
#         if obj:  # This ensures that all fields are read-only when editing an existing object
#             return [field.name for field in obj._meta.fields]
#         return []

# admin.site.register(Message, ReadOnlyAdmin)
