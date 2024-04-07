var accident_spots = JSON.parse(document.getElementById('black-spots').textContent)
var crime_scenes = JSON.parse(document.getElementById('crime-scenes').textContent)

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
    map.setMaxBounds(maxBounds);    // limit max map view to user's current location
    map.setView(loc.latlng, 14)     // zoom the map to user's current location. Zoom start - 14
    L.marker(loc.latlng, {icon: userIcon}).addTo(map).bindPopup("You are here!").openPopup()
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


// Create FastMarkerCluster group for accident spots and crime scenes
var accidentsClusterGroup = L.markerClusterGroup()
var crimesClusterGroup = L.markerClusterGroup()

// Add markers for accidents
accident_spots.forEach(spot => {
    latitude_coord = spot.latitude < 0 ? '&deg;S' : '&deg;N'
    var marker = L.marker([spot.latitude, spot.longitude])
    var popupContent = (
        "<h5>Road accident</h5>" +
        '<table class="table table-sm table-condensed table-striped table-bordered">' + "<tbody>" +
        "<tr><td><b>Latitude:</b></td><td>" + spot.latitude + "<b>" + latitude_coord +  "</b>" + "</td>" +
        "<tr><td><b>Longitude:</b></td><td>" + spot.longitude + "<b>&deg;E</b>" + "</td>" +
        "<tr><td><b>County:</b></td><td>" + spot.county + "</td>" +
        "<tr><td><b>Subcounty:</b></td><td>" + spot.sub_county + "</td>" +
        "<tr><td><b>Road/Highway:</b></td><td>" + spot.road + "</td>" +
        "<tr><td><b>Vehicle(s) involved:</b></td><td>" + spot.vehicles_count + "</td>" +
        "<tr><td><b>Victim(s):</b></td><td>" + spot.road_user + "</td>" +
        "<tr><td><b>Injuries:</b></td><td>" + spot.injuries_count + "</td>" +
        "<tr><td><b>Fatalities:</b></td><td>" + spot.fatalities + "</td>" +
        "</tbody>" + "</table>"
    )
    marker.bindPopup(popupContent).bindTooltip("Click for more info.")
    accidentsClusterGroup.addLayer(marker)
})

// Add markers for crimes
crime_scenes.forEach(scene => {
    latitude_coord = 'S' ? scene.latitude < 0 : 'N'
    var marker = L.marker([scene.latitude, scene.longitude])
    var popupContent = (
        "<h5>Crime</h5>" +
        '<table class="table table-sm table-condensed table-striped table-bordered">' + "<tbody>" +
        "<tr><td><b>Latitude:</b></td><td>" + scene.latitude +  "<b>" + latitude_coord +  "</b>" + "</td>" +
        "<tr><td><b>Longitude:</b></td><td>" + scene.longitude + "</td>" +
        "<tr><td><b>County:</b></td><td>" + scene.county + "</td>" +
        "<tr><td><b>Subcounty:</b></td><td>" + scene.sub_county + "</td>" +
        "</tbody>" + "</table>"
    )
    marker.bindPopup(popupContent)
    crimesClusterGroup.addLayer(marker)
})

// Add cluster groups to the map
map.addLayer(accidentsClusterGroup)
map.addLayer(crimesClusterGroup)
