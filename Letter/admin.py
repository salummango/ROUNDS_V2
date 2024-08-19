from django.contrib import admin
from django.utils.html import format_html
from .models import Letter
from django import forms
from tinymce.widgets import TinyMCE

class LetterAdminForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Letter
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'disabled': 'disabled'}),
            'sender': forms.TextInput(attrs={'disabled': 'disabled'}),
            'receiver': forms.TextInput(attrs={'disabled': 'disabled'}),
            'created': forms.DateTimeInput(attrs={'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super(LetterAdminForm, self).__init__(*args, **kwargs)
        # Only check if the instance is saved and has a receiver
        if self.instance.pk and self.instance.receiver and not self.instance.receiver.is_staff:
            self.fields['receiver'].widget.attrs['readonly'] = True

class LetterAdmin(admin.ModelAdmin):
    form = LetterAdminForm

    list_display = ('title', 'sender', 'receiver', 'created')
    search_fields = ('title', 'sender__username', 'receiver__username', 'created')

   
    
    def get_queryset(self, request):
        """Only show letters sent to the logged-in admin."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(receiver=request.user)

    def has_change_permission(self, request, obj=None):
        """Disable editing letters."""
        if obj:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Disable deleting letters."""
        return False

admin.site.register(Letter, LetterAdmin)
