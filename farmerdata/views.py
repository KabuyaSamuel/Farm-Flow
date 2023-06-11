from django.shortcuts import render, redirect
from .forms import ValueChainForm, CropForm, FarmForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from decouple import config

@login_required
def add_value_chain(request):
    if request.method == 'POST':
        form = ValueChainForm(request.POST)
        if form.is_valid():
            value_chain = form.save(commit=False)
            value_chain.approved = False  # Initially not approved
            value_chain.save()
            messages.info(request, "Value chain added successfully")
            return redirect('home')  # Or wherever you want to redirect
    else:
        form = ValueChainForm()
    return render(request, 'add_value_chain.html', {'form': form})


@login_required
def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.save()
            messages.info(request, "Crop added Successfully link a farm with the crop to display on dashboard.")
            return redirect('home')  # Or wherever you want to redirect
    else:
        form = CropForm()
    return render(request, 'add_crop.html', {'form': form})


@login_required
def create_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            new_farm = form.save(commit=False)
            new_farm.owner = request.user  # assign the current user
            new_farm.save()
            # handle many-to-many fields if any
            form.save_m2m()
            messages.success(request, 'Your farm data has been submitted and is awaiting approval.')

            # Send email to user
            msg_plain = render_to_string('email_templates/farm_submitted.txt', {'user': request.user, 'farm': new_farm})
            msg_html = render_to_string('email_templates/farm_submitted.html', {'user': request.user, 'farm': new_farm})

            send_mail(
                'Your farm data has been submitted',
                msg_plain,
                'noreply@farmshare.co.ke',
                [request.user.email],
                html_message=msg_html,
                fail_silently=False,
            )

            # Twilio SMS sending
            if request.user.profile.phone_number:
                try:
                    account_sid = config('TWILIO_ACCOUNT_SID')
                    auth_token = config('TWILIO_AUTH_TOKEN')
                    client = Client(account_sid, auth_token)

                    sms_message = f'Hello {request.user.username}, your farm data has been submitted and is awaiting approval.'
                    client.messages.create(
                        body=sms_message,
                        from_=config('TWILIO_PHONE_NUMBER'),  # your Twilio number
                        to=str(request.user.profile.phone_number)  # user's phone number in profile
                    )
                except TwilioRestException as e:
                    print(f"Twilio Error: {e}")
            else:
                messages.info(request, "To receive SMS notifications, please add your phone number to your profile.")

            # Send email to admin
            admin_msg = f"A new farm has been submitted for approval by {request.user.username}"

            send_mail(
                'New farm submitted',
                admin_msg,
                'noreply@farmshare.co.ke',
                ['farmflowtech@gmail.com'],  # replace with admin email
                fail_silently=False,
            )

            return redirect('home')

    else:
        form = FarmForm()
    return render(request, 'add_farm.html', {'form': form})

