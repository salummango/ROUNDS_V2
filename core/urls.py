"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', LogoutView.as_view(), name='admin_logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # Ensure auth URLs are included
    path('tinymce/',include('tinymce.urls')),
    
    path('api/',include('users.urls')),
    path('api/',include('league.urls')),
    path('api/',include('Letter.urls')),
    path('leaguehistory/', include('LeagueHistory.urls')),
    
    path('', views.FixtureList, name='all_match'),
    path('log',views.home,name='log'),
    path('register/',views.regist,name='register'),
    # path('chat/', views.chat_view, name='chat'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)