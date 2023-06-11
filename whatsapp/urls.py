from django.urls import path
from whatsapp.views import send_notification, schedule # ← add this import

urlpatterns = [
    path('whatsapp/', send_notification, name='whatsapp'),   # ← add this path definition
    path('schedule/', schedule, name='schedule'),
   
]
