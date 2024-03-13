import requests
import time

def test_get_data():
    response = requests.get('http://localhost:8000/get-data/')
    if response.status_code == 200:
        data = response.json()
        print("Data retrieved successfully:", data)
    else:
        print("Failed to retrieve data")

def test_set_data():
    data = {'data':{
        'geometry':{
            'coordinates':[37.7749,-122.4194,]
        },
        "properties": {
            "time": 1709005446860,
            "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
            "status": "automatic",
            "tsunami": False,
            "title": "Test Earthquake",
            "mag": 5.0,
            "place": "San Francisco, CA",
    }
    }}
    response = requests.post('http://localhost:8000/set-data/', json=data)
    if response.status_code == 200:
        print("Data saved successfully")
    else:
        print("Failed to save data")

def test_get_closest_earthquake():
    params = {
        "latitude":   37.7749,
        "longitude": -122.4194
    }
    response = requests.get('http://localhost:8000/get-closest-earthquake/', params=params)
    if response.status_code == 200:
        data = response.json()
        print("Closest earthquake:", data)
    else:
        print("Failed to get closest earthquake")

def test_get_weather_data():
    # Make the request to the Django server
    response = requests.get('http://localhost:8000/get-weather/')

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to get weather data")

    # Wait to allow the asynchronous operation to complete - may need to be adjusted
    time.sleep(3)

    # Check if the request was successful after the sleep
    if response.status_code != 200:
        print("Failed to get weather data")

    # Parse the JSON response
    data = response.json()

    # Print the weather data
    print("Weather data:", data)

# Run the tests
# test_get_data()
# test_set_data()
# test_get_closest_earthquake()
test_get_weather_data()