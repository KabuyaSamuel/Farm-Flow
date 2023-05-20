from django.urls import path
from .views import add_crop, add_value_chain, create_farm

urlpatterns = [
    path('value_chain/add/', add_value_chain, name='add_value_chain'),
    path('crop/add/', add_crop, name='add_crop'),
    path('farm/add/', create_farm, name='add_farm'),
]
