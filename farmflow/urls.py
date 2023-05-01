from django.urls import path
from .views import index, RegisterView

urlpatterns = [
    path('', index, name='home'),
    path('register/', RegisterView.as_view(), name='users-register'),
]
