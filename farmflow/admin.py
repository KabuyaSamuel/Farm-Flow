from django.contrib import admin
from .models import *

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
admin.site.register(Farm)