const store = { data: null}

// --- Function Definitions ---
// Function to fetch the most recent earthquakes for frontend
function getCurrentEarthquakes() {
    // USGS API
    const url= 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson';

    // Fetch data from the API
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Get the earthquakes from the response features
            const earthquakes = data.features.slice(0, 1);
            const earthquakeList = document.getElementById('earthquake-list');

            earthquakeList.innerHTML = '';

            // Iterate over each earthquake and add it to the list
            earthquakes.forEach((earthquake) => {
                store.earthquake = earthquake
                const properties = earthquake.properties;
                const magnitude = properties.mag;
                const location = properties.place;

                // Create a new list item for each earthquake
                const listItem = document.createElement('li');
                listItem.textContent = 'Magnitude: ' + magnitude + ', Location: ' + location;

                // Add the list item to the UL
                earthquakeList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error getting data:', error);
        });
}

function getEarthquakeMap(){
    // API endpoint URL for current earthquakes
    const url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson';

    // Fetch data from the API
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Get the first earthquake from the response
            const firstEarthquake = data.features[0];
            const coordinates = firstEarthquake.geometry.coordinates;
            const latitude = coordinates[1];
            const longitude = coordinates[0];

            // Initialize Leaflet map
            const map = L.map('map').setView([latitude, longitude], 5);

            // Add tile layer to the map
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            // Add marker to the map
            L.marker([latitude, longitude]).addTo(map)
                .bindPopup('Earthquake Location')
                .openPopup();
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Function to send a POST to save data
function saveData() {
    const save_data = store.earthquake
    fetch('http://localhost:8000/set-data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: save_data})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Save failed');
        }
        console.log('Data saved successfully');
        document.getElementById("save-button").dispatchEvent(new Event('dataSaved'));
    })
    .catch(error => {
        console.error('Error saving data:', error);
    });
}

//function to get weather data from JJ's microservice
function getWeather(){
    fetch('http://localhost:8000/get-weather/', {
        method: 'GET',
        headers: {
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch weather data');
        }
        return response.json();
    })
    .then(weatherData => {
        store.weather = weatherData;
        displayWeather(weatherData);
    })
    .catch(error => {
        console.error('Error retrieving weather data from the microservice:', error);
    });
}

function displayWeather(weatherData){
        // Fill in weather data
        const minTempElement = document.getElementById("min-temp");
        minTempElement.textContent = `${weatherData.data.min_temp_avg}°C`;

        const maxTempElement = document.getElementById("max-temp");
        maxTempElement.textContent = `${weatherData['data']['max_temp_avg']}°C`;

        const currentTempElement = document.getElementById("current-temp");
        currentTempElement.textContent = `${weatherData.data.current_temp_avg}°C`;
    }


// --- Function Calls ---
getEarthquakeMap()
window.onload = getCurrentEarthquakes;


// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', () => {
    const saveButton = document.getElementById("save-button")
    saveButton.addEventListener('click', saveData);
    saveButton.addEventListener('dataSaved',()=> {
        saveButton.textContent = 'Data Saved';
        saveButton.disabled = true;
    });
});
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("get-weather").addEventListener('click', getWeather);

});