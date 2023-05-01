from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Cluster)
admin.site.register(ProducerGroup)
admin.site.register(ValueChainChoice)
admin.site.register(SoilTestResult)
admin.site.register(InputUsed)
admin.site.register(FarmingType)
admin.site.register(WaterSource)