# from django.urls import path 
# from . import views

# urlpatterns = [
#     path('', views.login_view, name='login'),
#     path('register', views.register_view, name='register'),
#     path('logout', views.logout_view, name='logout'),
#     path('profile', views.profile_view, name='profile'),
# ]

from django.urls import path
from .views import LoginView, RegisterView, LogoutView, ProfileView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),
]

