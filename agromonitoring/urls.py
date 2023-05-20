from django.urls import path
from .views import get_weather, get_soil_data, get_uvi, search_satellite_imagery, get_satellite_images, weather_forecast

urlpatterns = [
    path('weather/', get_weather, name='get-weather'),
    path('weather/forecast/', weather_forecast, name='weather-forecast'),
    path('soil/', get_soil_data, name='soil-data'),
    path('uvi/', get_uvi, name='uvi-data'),
    path('satellite/', search_satellite_imagery, name='satellite-imagery'),
    path('satellite/images/', get_satellite_images, name='satellite-images'),


   

    # Add other URL patterns as needed
]
