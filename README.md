# CS361 Microservice
# Earthquakes API

## Overview

The Earthquakes API provides access to earthquake data collected from the USGS (United States Geological Survey). It allows users to retrieve information about earthquakes, including their magnitude, location, time, and other relevant details.

## Installation

To use the Earthquakes API, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the Django server using `python3 manage.py runserver`.
4. Test by running `python3 tests.py`


## Usage

### Endpoints

#### 1. `/get-data/`

- **Method**: GET
- **Description**: Retrieve earthquake data from the API.
- **Parameters**: None
- **Response**: Returns a JSON object containing earthquake data.

Example Request:
```json
GET /get-data/
```
Example Response:
```json
{'data': 
    {'latitude': 63.4966, 
    'longitude': -148.9255, 
    'magnitude': 2.1, 
    'place': '11 km N of Cantwell, Alaska', 
    'time': '2024-02-27T21:11:51Z', 
    'detail': 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/ak0242o9qp77.geojson',
    'status': 'automatic', 
    'tsunami': False, 
    'title': 'M 2.1 - 11 km N of Cantwell, Alaska'
    }
}
```

2. `/set-data/`

- **Method**: POST
- **Description**: Submit earthquake data to the API.
- **Parameters**: JSON object containing earthquake data.
- **Response**:  Returns a confirmation message upon successful submission.

Example Request:

```json
POST /set-data/

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
      }
    }
}
```

Example Response:
```json
{
  "message": "Data updated successfully."
}

```


3. `/get-closest-earthquake/`

- **Method**: POST
- **Description**: : Retrieve the closest earthquake to a specified location.
- **Parameters**:  Latitude and longitude of the location.
- **Response**: Returns a JSON object containing details of the closest earthquake.

Example Request:
```json
GET /get-closest-earthquake/?latitude=37.7749&longitude=-122.4194
```

Example Response:
```json
 {'closest_earthquake': 
    {'latitude': -122.4194, 
      'longitude': 37.7749, 
      'magnitude': 5.0, 
      'place': 'San Francisco, CA', 
      'time': '2024-02-27T03:44:06Z', 
      'detail': 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson', 
      'status': 'automatic', 
      'tsunami': False, 
      'title': 'Test Earthquake'
    }
}
```

