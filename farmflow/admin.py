from django.contrib import admin
from .models import *
from django.contrib import admin, messages
from .models import Crop
from django.core.mail import send_mail
from django.template.loader import render_to_string
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from decouple import config
from django.forms import ModelForm


class FarmAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_approval_status = self.instance.approval_status

class FarmAdmin(admin.ModelAdmin):
    form = FarmAdminForm
    
    def changelist_view(self, request, extra_context=None):
        if pending_verifications := Farm.objects.filter(
            approval_status='Pending'
        ).count():
            messages.warning(request, f'There are {pending_verifications} pending farm verifications.')

        return super().changelist_view(request, extra_context)
    
    actions = ['approve_farms']

    def save_model(self, request, obj, form, change):
        initial_status = form.initial_approval_status
        new_status = form.cleaned_data.get('approval_status')
        # Check if the status of the object has been changed to 'Approved'
        if initial_status != new_status and new_status == 'Approved':
            # Send the email
            msg_plain = render_to_string('email_templates/farm_approved.txt', {'user': obj.owner, 'farm': obj})
            msg_html = render_to_string('email_templates/farm_approved.html', {'user': obj.owner, 'farm': obj})

            send_mail(
                'Your farm has been approved',
                msg_plain,
                'noreply@farmshare.co.ke',
                [obj.owner.email],
                html_message=msg_html,
                fail_silently=False,
            )

            # Twilio SMS sending
            if obj.owner.profile.phone_number:
                try:
                    account_sid = config('TWILIO_ACCOUNT_SID')
                    auth_token = config('TWILIO_AUTH_TOKEN')
                    client = Client(account_sid, auth_token)

                    sms_message = f'Hello {obj.owner.username}, your farm has been approved.'
                    client.messages.create(
                        body=sms_message,
                        from_=config('TWILIO_PHONE_NUMBER'),  # your Twilio number
                        to=str(obj.owner.profile.phone_number),  # user's phone number in profile
                    )
                except TwilioRestException as e:
                    print(f"Twilio Error: {e}")
            else:
                messages.info(request, "To send SMS notifications, please add user phone number to profile.")

        super().save_model(request, obj, form, change)

     
# Register your models here.
admin.site.register(Profile)
admin.site.register(Cluster)
admin.site.register(ProducerGroup)
admin.site.register(ValueChainChoice)
admin.site.register(SoilTestResult)
admin.site.register(InputUsed)
admin.site.register(FarmingType)
admin.site.register(WaterSource)
admin.site.register(Crop)
admin.site.register(CropProductionStage)
admin.site.register(FarmInputUsed)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Produce)
admin.site.register(Tag)