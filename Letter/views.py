from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Letter
from .forms import LetterForm




def letter_detail(request, letter_id):
    details = get_object_or_404(Letter, pk=letter_id)
    return render(request, 'letter_detail.html', {'details': details})
