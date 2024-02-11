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

            // Get the UL element to display the list
            const earthquakeList = document.getElementById('earthquake-list');

            // Clear the list
            earthquakeList.innerHTML = '';

            // Iterate over each earthquake and add it to the list
            earthquakes.forEach((earthquake) => {
                const properties = earthquake.properties;
                const magnitude = properties.mag;
                const location = properties.place;

                // Create a new list item for each earthquake
                const listItem = document.createElement('li');
                listItem.textContent = 'Magnitude: ' + magnitude + ', Location: ' + location;

                // Add the list item to the UL element
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
            // latitude, longitude = coordinates
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

// Call the function to display the location of the earthquake on the map
getEarthquakeMap()

// Call the function when the page loads (should this be replaced with React and events?)
window.onload = getCurrentEarthquakes;
