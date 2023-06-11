from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def ussd(request):
    if request.method != 'POST':
        return HttpResponse()  # Default response for non-POST requests
    session_id = request.POST.get('sessionId')
    service_code = request.POST.get('serviceCode')
    phone_number = request.POST.get('phoneNumber')
    text = request.POST.get('text')

    response = ""
    if text == "":
        response = "CON Welcome to Farm Share USSD service \n" + "1. Register \n"
        response += "2. About \n"
        response += "3. Local  \n"
        response += "4. International"
    elif text == "1":
        response = "CON Select Your Preferred Sport Plans \n" + "1. Daily @ N100 \n"
        response += "2. Weekly @ N50 \n"
        response += "3. Monthly @ N25 "
    elif text == "1*1":
        response = (
            "CON You will be charged N100 for your Daily Sports news subscription \n"
            + "1. Auto-Renew \n"
        )
        response += "2. One-off Purchase \n"
    elif text == "1*1*1":
        response = "END thank you for subscribing to our daily sport news plan \n"
    elif text == "1*1*2":
        response = "END thank you for your one-off daily sport news plan \n"
    elif text == "1*2":
        response = (
            "CON You will be charged N50 for our weekly Sports news plan \n"
            + "1. Auto-Renew \n"
        )
        response += "2. One-off Purchase \n"
    elif text == "1*2*1":
        response = "END thank you for subscribing to our weekly sport news plan \n"
    elif text == "1*2*2":
        response = "END thank you for your one-off weekly sport news plan \n"
    elif text == "1*3":
        response = (
            "CON You will be charged N25 for our monthly Sports news plan \n"
            + "1. Auto-Renew \n"
        )
        response += "2. One-off Purchase \n"
    elif text == "1*3*1":
        response = "END thank you for subscribing to our monthly sport news plan \n"
    elif text == "1*3*2":
        response = "END thank you for your one-off monthly sport news plan \n"

    return HttpResponse(response)
