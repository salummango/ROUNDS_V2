from django.urls import path, include
from .views import RegisterUser, LoginUser, LogoutUser, UserView, AllUser

urlpatterns = [
    path('registration', RegisterUser.as_view()),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view()),
    path('putdelete', UserView.as_view()),
    path('alluser/', AllUser.as_view(), name='alluser'),

]
