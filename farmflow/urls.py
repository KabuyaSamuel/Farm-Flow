from django.urls import path
from .views import index, RegisterView, profile, edit_profile

urlpatterns = [
    path('', index, name='home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('edit/profile/', edit_profile, name='edit-profile'),
]
