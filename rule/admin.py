from django.contrib import admin
from .models import Rule

class RuleAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Return False to disable the add permission
        return False

admin.site.register(Rule, RuleAdmin)
