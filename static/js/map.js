var incident_spots = JSON.parse(document.getElementById('incident-spots').textContent)

var map = L.map('geo-map', {
    minZoom: 13,
    maxZoom: 16,
    timeout: 10000,
})

var userIcon = L.divIcon({
    className: 'custom-icon',
    html: '<i class="fas fa-person fa-2x" style="color: #d60808;"></i>',
})

function onLocationFound(loc) {
    var maxBounds = L.latLngBounds(
        [loc.latlng.lat, loc.latlng.lng],
        [loc.latlng.lat, loc.latlng.lng]
    )

    // Set maxBounds for the map
    map.setMaxBounds(maxBounds)    // limit max map view to user's current location
    map.setView(loc.latlng, 14)     // zoom the map to user's current location. Zoom start - 14
    L.marker(loc.latlng, {
        icon: L.AwesomeMarkers.icon({
            prefix: 'fas fa',
            icon: 'person fa-2x',
            markerColor: 'darkpurple'
        })
    }).addTo(map).bindPopup("You are here!").openPopup()    // marker that shows user's current position
}

function onLocationError(e) {
    var toast = document.createElement('div')
    toast.className = 'toast bg-danger text-light';
    toast.setAttribute('role', 'alert')
    toast.setAttribute('aria-live', 'assertive')
    toast.setAttribute('aria-atomic', 'true')

    var toastHeader = document.createElement('div')
    toastHeader.className = 'toast-header';
    var strong = document.createElement('strong')
    strong.className = 'me-auto';
    strong.innerText = 'Location Error';
    var button = document.createElement('button')
    button.className = 'btn-close';
    button.setAttribute('type', 'button')
    button.setAttribute('data-bs-dismiss', 'toast')
    button.setAttribute('aria-label', 'Close')
    toastHeader.appendChild(strong)
    toastHeader.appendChild(button)

    var toastBody = document.createElement('div')
    toastBody.className = 'toast-body';
    toastBody.innerText = e.message;

    toast.appendChild(toastHeader)
    toast.appendChild(toastBody)

    var toastContainer = document.getElementById('toast-container')
    toastContainer.appendChild(toast)

    var bootstrapToast = new bootstrap.Toast(toast)
    bootstrapToast.show()
}


// Set up map and tile layer
map.on('locationfound', onLocationFound)
map.on('locationerror', onLocationError)

map.locate({
    setView: true, 
    maxZoom: 14, 
    timeout: 17000
})

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map)


// Use Haversine formula to calculate distance between two points. 
// It is used to calculate the great-circle distance between two points on
// the Earth's surface given their latitude and longitude coordinates. 
function calculateDistance(lat1, lon1, lat2, lon2) {
    var R = 6371; // Radius of the earth in km
    var dLat = (lat2 - lat1) * Math.PI / 180  // deg2rad below
    var dLon = (lon2 - lon1) * Math.PI / 180
    var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2)
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    var d = R * c; // Distance in km
    return d
}

// Create FastMarkerCluster group for accident spots and crime scenes
var incidentsClusterGroup = L.markerClusterGroup()

// Get user's current position and calculate distance from the accident spot
navigator.geolocation.getCurrentPosition(function(position) {
    // Retrieve latitude and longitude from the position object
    var userLatitude = position.coords.latitude
    var userLongitude = position.coords.longitude

    incident_spots.forEach(spot => {
        var distance = calculateDistance(userLatitude, userLongitude, spot.latitude, spot.longitude)
        var distanceMetres = (distance * 1000).toFixed(2)   // Convert kilometers to metres
        var distanceKilometers = distance.toFixed(2)
        var distanceMiles = (distance * 0.621371).toFixed(2)     // Convert kilometers to miles
    
        var tooltipContent = "Distance to your location:<br>" +
            "Meters: " + distanceMetres + " <b>metres</b><br>" +
            "Kilometers: " + distanceKilometers + " <b>km</b><br>" +
            "Miles: " + distanceMiles + " <b>miles</b><br>" +
            '<hr class="my-1"><b>Click marker for more info.</b>'
    
        latitude_coord = spot.latitude < 0 ? '&deg;S' : '&deg;N'
        var marker = L.marker([spot.latitude, spot.longitude], {
            icon: L.AwesomeMarkers.icon({
                prefix: 'fas fa',
                icon:  spot.incident_type === 'Road accident' ? 'car fa-2x' : 'exclamation-triangle',
                markerColor: spot.incident_type === 'Road accident' ? 'red' : 'orange'
            })
        })
        var popupContent = (
            "<h5>" + spot.incident_type + "</h5>" +
            '<table class="table table-sm table-condensed table-striped table-bordered">' + "<tbody>" +
            "<tr><td><b>Latitude</b></td><td>" + spot.latitude + "<b>" + latitude_coord +  "</b>" + "</td>" +
            "<tr><td><b>Longitude</b></td><td>" + spot.longitude + "<b>&deg;E</b>" + "</td>" +
            "<tr><td><b>County</b></td><td>" + spot.county + "</td>" +
            "<tr><td><b>Subcounty</b></td><td>" + spot.sub_county + "</td>" +
            "<tr><td><b>Place</b></td><td>" + spot.place + "</td>" +
            "<tr><td><b>Incident date</b></td><td>" + spot.incident_date + "</td>" +
            "<tr><td><b>Incident time</b></td><td>" + spot.incident_time + "</td>" +
            "<tr><td><b>Reported by</b></td><td>" + spot.reported_by + "</td>" +
            "</tbody>" + "</table>"
        )
        marker.bindPopup(popupContent)
        marker.bindTooltip(tooltipContent).openTooltip()
        incidentsClusterGroup.addLayer(marker)
    })

}, function(error) {
    alert("Error: ", error)
})

// Add cluster groups to the map
map.addLayer(incidentsClusterGroup)
