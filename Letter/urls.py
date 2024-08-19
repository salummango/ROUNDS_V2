# In your app's urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('<int:letter_id>/', views.letter_detail, name='letter_detail'),

]
