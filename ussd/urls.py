from django.urls import path
from ussd.views import ussd

urlpatterns = [
    path('ussd-code/', ussd, name='ussd'),
   
]
