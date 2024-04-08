from django.urls import path
from .views import *
from . import views
from .views import LogoutUser

urlpatterns = [
    path('registration',RegisterUser.as_view()),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout',LogoutUser.as_view()),
    path('putdelete',UserView.as_view()),
    path('userdashboard',views.userdashboard,name='userdashboard'),
    
    # path('verify/', verify_email, name='verify_email'),
    # path('registration-success/', registration_success, name='registration_success'),
    # path('verification-success/', verification_success, name='verification_success'),
]
