from django.contrib import admin
from farmerdata.forms import CropForm
from .models import *
from django.contrib import admin, messages
from .models import Crop
from django.core.mail import send_mail
from django.template.loader import render_to_string

class FarmAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        if pending_verifications := Farm.objects.filter(
            approval_status='Pending'
        ).count():
            messages.warning(request, f'There are {pending_verifications} pending farm verifications.')

        return super(FarmAdmin, self).changelist_view(request, extra_context)
    
    actions = ['approve_farms']

    def save_model(self, request, obj, form, change):
        # Check if the status of the object has been changed to 'Approved'
        if 'approval_status' in form.changed_data and obj.approval_status == 'Approved':
            # Send the email
            msg_plain = render_to_string('email_templates/farm_approved.txt', {'user': obj.owner, 'farm': obj})
            msg_html = render_to_string('email_templates/farm_approved.html', {'user': obj.owner, 'farm': obj})

            send_mail(
                'Your farm has been approved',
                msg_plain,
                'farmflowtech@example.com',
                [obj.owner.email],
                html_message=msg_html,
            )

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