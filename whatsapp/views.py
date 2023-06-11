from django.shortcuts import render

def send_notification(request):
    return render(request, 'chat.html')

def schedule(request):
    return render(request, 'schedule.html')
