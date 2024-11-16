let map;
let tempMarker = null;
let markers = {};

function map_init(mapInstance) {
    map = mapInstance;
    
    // Set initial view to Los Angeles with closer zoom
    map.setView([34.0522, -118.2437], 12);
    
    try {
        // Load existing points
        if (window.existingPoints && Array.isArray(window.existingPoints)) {
            window.existingPoints.forEach(point => {
                // Create marker
                const marker = L.marker([point.lat, point.lng], {
                    icon: L.divIcon({
                        className: 'existing-point',
                        html: '<div style="background-color: red; width: 10px; height: 10px; border-radius: 50%;"></div>'
                    })
                }).addTo(map)
                .bindPopup(`<b>${point.name}</b><br>${point.description}`);
                
                // Store marker in markers object
                markers[point.id] = marker;
            });
        }
    } catch (error) {
        console.error('Error loading existing points:', error);
    }

    // Handle map click events
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        
        // Remove previous temporary marker if exists
        if (tempMarker) {
            map.removeLayer(tempMarker);
        }
        
        // Add new temporary marker
        tempMarker = L.marker([lat, lng], {
            icon: L.divIcon({
                className: 'temp-point',
                html: '<div style="background-color: blue; width: 10px; height: 10px; border-radius: 50%;"></div>'
            })
        }).addTo(map);
        
        // Update form coordinates
        document.getElementById('lat').value = lat;
        document.getElementById('lng').value = lng;
    });

    // Handle form submission
    document.getElementById('add-point-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch('/map_app/add_point/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                // Add permanent marker
                const marker = L.marker([data.point.lat, data.point.lng], {
                    icon: L.divIcon({
                        className: 'existing-point',
                        html: '<div style="background-color: red; width: 10px; height: 10px; border-radius: 50%;"></div>'
                    })
                }).addTo(map)
                .bindPopup(`<b>${data.point.name}</b><br>${data.point.description}`);
                
                // Store new marker
                markers[data.point.id] = marker;
                
                // Remove temporary marker
                if (tempMarker) {
                    map.removeLayer(tempMarker);
                }
                
                // Reset form
                this.reset();
                
                // Refresh page to update points list
                window.location.reload();
            } else {
                alert('Error adding point: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding point: ' + error.message);
        });
    });

    // Add click event listeners for delete buttons
    document.querySelectorAll('.delete-point-btn').forEach(button => {
        button.addEventListener('click', function() {
            const pointId = this.getAttribute('data-point-id');
            if (confirm('Are you sure you want to delete this point?')) {
                deletePoint(pointId);
            }
        });
    });
}

function deletePoint(pointId) {
    // Add debug logs
    console.log('Attempting to delete point:', pointId);
    console.log('Available markers:', markers);
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/map_app/delete-point/${pointId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        console.log('Delete response:', response);
        return response.json();
    })
    .then(data => {
        console.log('Delete response data:', data);
        if (data.status === 'success') {
            // Remove row from table
            const row = document.querySelector(`tr[data-point-id="${pointId}"]`);
            if (row) {
                row.remove();
            }
            
            // Remove marker from map
            if (markers[pointId]) {
                map.removeLayer(markers[pointId]);
                delete markers[pointId];
            }
            
            // Show success message
            alert('Point successfully deleted');
        } else {
            alert('Delete failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error during delete:', error);
        alert('Error during delete: ' + error.message);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 