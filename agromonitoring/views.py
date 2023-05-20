from django.shortcuts import render
import requests
from decouple import config
from django.utils import timezone

# Create your views here.

def get_weather(request):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = config('AGRO_API')
    url = 'https://api.agromonitoring.com/agro/1.0/weather'

    # Get latitude and longitude from the request or use default values
    lat = request.GET.get('lat', -1.2200474)  # Default latitude: 35
    lon = request.GET.get('lon', 36.6629928)  # Default longitude: 139

    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return render(request, 'error.html', {'message': 'Failed to fetch weather data'})
    data = response.json()

    data['dt'] = timezone.datetime.fromtimestamp(data['dt'], timezone.get_current_timezone())

    return render(request, 'weather.html', {'weather_data': data})


def weather_forecast(request):
    api_key = config('AGRO_API')
    lat = -1.2200474
    lon = 36.6629928
    
    url = f'https://api.agromonitoring.com/agro/1.0/weather/forecast?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    forecast_data = response.json()

   # Convert the forecast dates to the EAT timezone
    for forecast in forecast_data:
        forecast['dt'] = timezone.datetime.fromtimestamp(forecast['dt'], timezone.get_current_timezone())
    
    context = {
        'forecast_data': forecast_data,
    }
    
    return render(request, 'weather_forecast.html', context)


def get_soil_data(request):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = config('AGRO_API')
    url = 'http://api.agromonitoring.com/agro/1.0/soil'

    # Get the polyid from the request or set a default value
    polyid = request.GET.get('polyid', '646736f06efa7f268a949509')

    params = {
        'polyid': polyid,
        'appid': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return render(request, 'error.html', {'message': 'Failed to fetch soil data'})
    data = response.json()

    data['dt'] = timezone.datetime.fromtimestamp(data['dt'], timezone.get_current_timezone())

    return render(request, 'soil.html', {'soil_data': data})



def get_uvi(request):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = config('AGRO_API')
    url = 'http://api.agromonitoring.com/agro/1.0/uvi'

    # Get the polyid from the request
    polyid = request.GET.get('polyid', '646736f06efa7f268a949509')

    params = {
        'polyid': polyid,
        'appid': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return render(request, 'error.html', {'message': 'Failed to fetch UV Index data'})
    data = response.json()

    data['dt'] = timezone.datetime.fromtimestamp(data['dt'], timezone.get_current_timezone())

    return render(request, 'uvi.html', {'uvi_data': data})



def search_satellite_imagery(request):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = config('AGRO_API')
    url = 'http://api.agromonitoring.com/agro/1.0/image/search'

    # Get the polygon_id, start date, and end date from the request
    polygon_id = request.GET.get('polygon_id', '646736f06efa7f268a949509')
    start_date = request.GET.get('start_date', '1677618000')
    end_date = request.GET.get('end_date', '1680296400')

    params = {
        'polyid': polygon_id,
        'start': start_date,
        'end': end_date,
        'appid': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return render(request, 'error.html', {'message': 'Failed to fetch satellite imagery data'})
    data = response.json()

     # Convert the timestamp to a datetime object in UTC
    for image_data in data:
        timestamp = image_data['dt']
        utc_dt = timezone.datetime.fromtimestamp(timestamp, tz=timezone.utc)
        image_data['dt'] = utc_dt.astimezone(timezone.get_current_timezone())

    return render(request, 'satellite_imagery.html', {'imagery_data': data})




def get_satellite_images(request):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = config('AGRO_API')
    polygon_id = request.GET.get('polygon_id', '646736f06efa7f268a949509')
    start_date = request.GET.get('start_date', '1671475200')
    end_date = request.GET.get('end_date', '1671478800')

    # Fetch satellite imagery metadata
    metadata_url = f'http://api.agromonitoring.com/agro/1.0/image/search?start={start_date}&end={end_date}&polyid={polygon_id}&appid={api_key}'
    metadata_response = requests.get(metadata_url)

    if metadata_response.status_code != 200:
        return render(request, 'error.html', {'message': 'Failed to fetch satellite imagery data'})
    metadata_data = metadata_response.json()

    # Fetch specific satellite images or zonal statistics
    image_urls = metadata_data[0]['image']  # Replace index [0] with the desired image type
    stats_urls = metadata_data[0]['stats']  # Replace index [0] with the desired index type

    # Render the template with the image and stats URLs
    return render(request, 'satellite_images.html', {'image_urls': image_urls, 'stats_urls': stats_urls})
