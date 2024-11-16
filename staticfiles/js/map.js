let map;
let tempMarker = null;

function map_init(mapInstance) {
    map = mapInstance;
    
    try {
        // 加载已有的点位
        if (window.existingPoints && Array.isArray(window.existingPoints)) {
            window.existingPoints.forEach(point => {
                L.marker([point.lat, point.lng], {
                    icon: L.divIcon({
                        className: 'existing-point',
                        html: '<div style="background-color: red; width: 10px; height: 10px; border-radius: 50%;"></div>'
                    })
                }).addTo(map)
                .bindPopup(`<b>${point.name}</b><br>${point.description}`);
            });
        }
    } catch (error) {
        console.error('Error loading existing points:', error);
    }

    // 点击地图时的处理
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        
        // 移除之前的临时标记（如果存在）
        if (tempMarker) {
            map.removeLayer(tempMarker);
        }
        
        // 添加新的临时标记
        tempMarker = L.marker([lat, lng], {
            icon: L.divIcon({
                className: 'temp-point',
                html: '<div style="background-color: blue; width: 10px; height: 10px; border-radius: 50%;"></div>'
            })
        }).addTo(map);
        
        // 更新表单中的坐标
        document.getElementById('lat').value = lat;
        document.getElementById('lng').value = lng;
    });

    // 表单提交处理
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
                // 添加永久标记
                L.marker([data.point.lat, data.point.lng], {
                    icon: L.divIcon({
                        className: 'existing-point',
                        html: '<div style="background-color: red; width: 10px; height: 10px; border-radius: 50%;"></div>'
                    })
                }).addTo(map)
                .bindPopup(`<b>${data.point.name}</b><br>${data.point.description}`);
                
                // 移除临时标记
                if (tempMarker) {
                    map.removeLayer(tempMarker);
                }
                
                // 重置表单
                this.reset();
                
                // 刷新页面以更新点位列表
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
}

// 获取CSRF Token的辅助函数
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