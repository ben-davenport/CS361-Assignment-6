import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Earthquake
from datetime import datetime
from django.db.models import Func, F
from django.db.models.functions import ACos, Cos, Radians, Sin

earthquake_data = {}
@csrf_exempt
def set_data(request):
    print(json.loads(request.body))
    if request.method == 'POST':
        new_data = json.loads(request.body)
        time_value = new_data['data']['properties']['time']
        timestamp = datetime.fromtimestamp(time_value / 1000)  # Convert milliseconds to seconds
        formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string

        # print('-----')
        # print(new_data)
        earthquake = Earthquake.objects.create(
            latitude=new_data['data']['geometry']['coordinates'][1],
            longitude=new_data['data']['geometry']['coordinates'][0],
            magnitude=new_data['data']['properties']['mag'],
            place=new_data['data']['properties']['place'],
            time=formatted_time,
            detail=new_data['data']['properties']['detail'],
            status=new_data['data']['properties']['status'],
            tsunami=bool(new_data['data']['properties']['tsunami']),
            title=new_data['data']['properties']['title']
        )
        return JsonResponse({'message': 'Data updated'})
    else:
        return JsonResponse({'error': 'POST ERROR'})

@csrf_exempt
def get_data(request):
    latest_earthquake = Earthquake.objects.latest('time')
    # Change the earthquake object into JSON format
    serialized_earthquake = {
        'latitude': latest_earthquake.latitude,
        'longitude': latest_earthquake.longitude,
        'magnitude': latest_earthquake.magnitude,
        'place': latest_earthquake.place,
        'time': latest_earthquake.time,
        'detail': latest_earthquake.detail,
        'status': latest_earthquake.status,
        'tsunami': latest_earthquake.tsunami,
        'title': latest_earthquake.title
    }

    return JsonResponse({'data': serialized_earthquake})
def get_closest_earthquake(latitude, longitude):
    # Distance calculation source assistance:
    # https://medium.com/analytics-vidhya/finding-nearest-pair-of-latitude-and-longitude-match-using-python-ce50d62af546

    # Convert latitude and longitude to radians
    latitude_rad = Radians(latitude)
    longitude_rad = Radians(longitude)

    # Calculate distances and get the closest earthquake
    closest_earthquake = Earthquake.objects.annotate(
        lat_rad=Radians(F('latitude')),
        lon_rad=Radians(F('longitude')),
        delta_lon=Func(F('longitude') - longitude, function='ABS'),
        central_angle=ACos(
            Sin(latitude_rad) * Sin(F('lat_rad')) +
            Cos(latitude_rad) * Cos(F('lat_rad')) *
            Cos(Func(F('delta_lon') / 2, function='RADIANS'))
        ),
        distance=Func(Func('central_angle', function='DEGREES'), function='ABS') * 60 * 1.1515  # Convert central angle to distance in miles
    ).order_by('distance').first()

    if closest_earthquake.distance < 0.001:  # Adjust threshold as needed
        closest_earthquake.distance = 0

    return closest_earthquake
def get_closest_earthquake_view(request):
    if request.method == 'GET':
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        if latitude is not None and longitude is not None:
            try:
                closest_earthquake = get_closest_earthquake(float(latitude), float(longitude))
                if closest_earthquake is not None:
                    data = {
                        'latitude': closest_earthquake.latitude,
                        'longitude': closest_earthquake.longitude,
                        'magnitude': closest_earthquake.magnitude,
                        'place': closest_earthquake.place,
                        'time': closest_earthquake.time,
                        'detail': closest_earthquake.detail,
                        'status': closest_earthquake.status,
                        'tsunami': closest_earthquake.tsunami,
                        'title': closest_earthquake.title
                    }
                    return JsonResponse({'closest_earthquake': data})
                else:
                    return JsonResponse({'error': 'No earthquakes found'})
            except ValueError:
                return JsonResponse({'error': 'Invalid latitude or longitude'})
        else:
            return JsonResponse({'error': 'Latitude and longitude are required as query parameters'})
    else:
        return JsonResponse({'error': 'GET method is required'})
