from django import forms
from .models import Letter
from tinymce.widgets import TinyMCE

# class LetterForm(forms.ModelForm):
#     class Meta:
#         model = Letter
#         fields = ['title', 'body', 'receiver']  # Only allow the admin user to select the receiver
#         widgets = {
#             'body': TinyMCE(attrs={'cols': 80, 'rows': 20}),
#         }


from django import forms
from .models import Letter
from django.contrib.auth import get_user_model

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['title', 'body', 'receiver']
        widgets = {
            'body': TinyMCE(attrs={'cols': 80, 'rows': 20}),
        }

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if user.is_staff:
                # Admins can send letters to any user
                self.fields['receiver'].queryset = get_user_model().objects.all()
            else:
                # Normal users can only send letters to admins
                self.fields['receiver'].queryset = get_user_model().objects.filter(is_staff=True)


