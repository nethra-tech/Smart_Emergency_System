/**
 * Smart Emergency Response System - Frontend API Integration
 * Technology: HTML5, CSS3, JavaScript (ES6)
 */
let hospitalMarkers = [];

// ===============================
// API Configuration
// ===============================
const API_BASE = 'http://localhost:3000/api';

// ===============================
// API Helper Functions
// ===============================

const api = {
    // Get all hospitals
    async getHospitals() {
        try {
            const response = await fetch(`${API_BASE}/hospitals`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching hospitals:', error);
            return [];
        }
    },

    // Find best hospital based on emergency
    async findBestHospital(lat, lng, emergencyType) {
        try {
            const response = await fetch(`${API_BASE}/hospitals/best`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lng, emergencyType })
            });
            return await response.json();
        } catch (error) {
            console.error('Error finding best hospital:', error);
            return null;
        }
    },

    // Get nearby hospitals
    async getNearbyHospitals(lat, lng, limit = 5) {
        try {
            const response = await fetch(`${API_BASE}/hospitals/nearby`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lng, limit })
            });
            return await response.json();
        } catch (error) {
            console.error('Error fetching nearby hospitals:', error);
            return [];
        }
    },

    // Trigger SOS
    async triggerSOS(lat, lng, emergencyType, peopleCount, userId = null) {
        try {
            const response = await fetch(`${API_BASE}/sos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    lat,
                    lng,
                    emergencyType,
                    peopleCount,
                    userId,
                    timestamp: new Date()
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Error triggering SOS:', error);
            return { success: false, error: error.message };
        }
    },

    // Optimize route
    async optimizeRoute(originLat, originLng, destLat, destLng) {
        try {
            const response = await fetch(`${API_BASE}/route/optimize`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    originLat, originLng, destLat, destLng
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Error optimizing route:', error);
            return null;
        }
    },

    // Send OTP
    async sendOTP(phone) {
        try {
            const response = await fetch(`${API_BASE}/auth/send-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone })
            });
            return await response.json();
        } catch (error) {
            console.error('Error sending OTP:', error);
            return { success: false, error: error.message };
        }
    },

    // Verify OTP
    async verifyOTP(phone, otp) {
        try {
            const response = await fetch(`${API_BASE}/auth/verify-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone, otp })
            });
            return await response.json();
        } catch (error) {
            console.error('Error verifying OTP:', error);
            return { success: false, error: error.message };
        }
    },

    // Get emergency contacts
    async getContacts() {
        try {
            const response = await fetch(`${API_BASE}/contacts`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching contacts:', error);
            return [];
        }
    }
};

// ===============================
// Location Functions
// ===============================

/**
 * Get current user location using Browser Geolocation API
 */
function getLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    resolve({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    });
                },
                error => {
                    // Use default location if geolocation fails
                    console.warn('Geolocation error:', error.message);
                    // Default to a sample location (can be changed)
                    resolve({
                        lat: 8.7139,
                        lng: 77.7567,
                        accuracy: null,
                        isDefault: true
                    });
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        } else {
            reject(new Error('Geolocation is not supported'));
        }
    });
}

// ===============================
// Emergency Functions
// ===============================

/**
 * Handle emergency form submission
 */
async function handleEmergencySubmit(emergencyType, peopleCount) {
    try {
        // Show loading state
        showLoading('Detecting your location...');

        // Get user location
        const location = await getLocation();

        // Hide loading
        hideLoading();

        // Show processing section
        showProcessingSection();

        // Update location status
        updateLocationStatus(location);

        // Find best hospital
        const hospital = await api.findBestHospital(
            location.lat,
            location.lng,
            emergencyType
        );

        if (hospital) {
            // Display hospital info
            displayHospitalInfo(hospital);

            // Initialize map
            initEmergencyMap(location, hospital);

            // Trigger SOS
            const sosResult = await api.triggerSOS(
                location.lat,
                location.lng,
                emergencyType,
                peopleCount
            );

            if (sosResult.success) {
                displayAmbulanceInfo(sosResult.ambulance);
                displayRouteInfo(sosResult);
            }
        }
    } catch (error) {
        console.error('Emergency error:', error);
        alert('Error processing emergency request. Please try again.');
    }
}

/**
 * Display hospital information
 */
function displayHospitalInfo(hospital) {
    const hospitalInfo = document.getElementById('hospitalInfo');
    if (hospitalInfo) {
        hospitalInfo.innerHTML = `
            <div class="info-card">
                <h4><i class="fas fa-hospital"></i> Nearest Best Hospital</h4>
                <p><strong>${hospital.name}</strong></p>
                <p>ICU Beds: ${hospital.icu} | Normal Beds: ${hospital.beds}</p>
                <p>Distance: ${hospital.distance} km</p>
                <p>Rating: ${hospital.rating} ⭐</p>
                <p>Contact: ${hospital.contact}</p>
            </div>
        `;
    }
}

/**
 * Display ambulance information
 */
function displayAmbulanceInfo(ambulance) {
    const ambulanceInfo = document.getElementById('ambulanceInfo');
    if (ambulanceInfo && ambulance) {
        ambulanceInfo.innerHTML = `
            <div class="info-card">
                <h4><i class="fas fa-ambulance"></i> Ambulance Assigned</h4>
                <p>Vehicle: AMB-${ambulance.id.toString().padStart(4, '0')}</p>
                <p>ETA: ${ambulance.eta} minutes</p>
                <p>Driver: John (+91 98765 43210)</p>
            </div>
        `;
    }
}

/**
 * Display route information
 */
function displayRouteInfo(sosResult) {
    const routeInfo = document.getElementById('routeInfo');
    if (routeInfo && sosResult.hospital) {
        routeInfo.innerHTML = `
            <div class="info-card">
                <h4><i class="fas fa-route"></i> Route Optimized</h4>
                <p>Distance: ${sosResult.hospital.distance} km</p>
                <p>ETA: ${sosResult.hospital.eta} minutes</p>
                <p>Traffic Status: Clear</p>
            </div>
        `;
    }
}

// ===============================
// Map Functions
// ===============================

let emergencyMap = null;

/**
 * Initialize emergency map with user and hospital locations
 */
function initEmergencyMap(userLocation, hospital) {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) return;

    // Initialize map
    emergencyMap = L.map('map').setView([
        userLocation.lat,
        userLocation.lng
    ], 13);

    // Add tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(emergencyMap);

    // Add user marker
    const userIcon = L.divIcon({
        className: 'user-marker',
        html: '<i class="fas fa-user" style="color: #3498db; font-size: 24px;"></i>',
        iconSize: [30, 30],
        iconAnchor: [15, 15]
    });

    L.marker([userLocation.lat, userLocation.lng], { icon: userIcon })
        .addTo(emergencyMap)
        .bindPopup('Your Location')
        .openPopup();

    // Add hospital marker
    const hospitalIcon = L.divIcon({
        className: 'hospital-marker',
        html: '<i class="fas fa-hospital" style="color: #e74c3c; font-size: 24px;"></i>',
        iconSize: [30, 30],
        iconAnchor: [15, 15]
    });

    L.marker([hospital.lat, hospital.lng], { icon: hospitalIcon })
        .addTo(emergencyMap)
        .bindPopup(`<b>${hospital.name}</b><br>${hospital.distance} km away`);

    // Draw route line
    const routeLine = L.polyline([
        [userLocation.lat, userLocation.lng],
        [hospital.lat, hospital.lng]
    ], {
        color: '#3498db',
        weight: 4,
        opacity: 0.7,
        dashArray: '10, 10'
    }).addTo(emergencyMap);

    // Fit bounds to show both markers
    emergencyMap.fitBounds(routeLine.getBounds(), {
        padding: [50, 50]
    });
}

// ===============================
// UI Helper Functions
// ===============================

function showLoading(message) {
    const locationStatus = document.getElementById('locationStatus');
    if (locationStatus) {
        locationStatus.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            ${message}
        `;
    }
}

function hideLoading() {
    const locationStatus = document.getElementById('locationStatus');
    if (locationStatus) {
        locationStatus.innerHTML = locationStatus.innerHTML
            .replace('fa-spinner fa-spin', 'fa-check-circle')
            .replace('Detecting', 'Location detected');
    }
}

function updateLocationStatus(location) {
    const locationStatus = document.getElementById('locationStatus');
    if (locationStatus) {
        const locationText = location.isDefault
            ? 'Using default location'
            : `Location: ${location.lat.toFixed(4)}, ${location.lng.toFixed(4)}`;
        
        locationStatus.innerHTML = `
            <i class="fas fa-check-circle" style="color: #2ecc71;"></i>
            ${locationText}
        `;
    }
}

function showProcessingSection() {
    const processingSection = document.getElementById('processingSection');
    const emergencyForm = document.getElementById('emergencyForm');
    
    if (processingSection) processingSection.style.display = 'block';
    if (emergencyForm) emergencyForm.style.display = 'none';
}

// ===============================
// Authentication Functions
// ===============================

/**
 * Send OTP for login
 */
async function sendLoginOTP(phone) {
    if (phone.length !== 10) {
        alert('Please enter a valid 10-digit phone number');
        return;
    }

    const result = await api.sendOTP(phone);
    
    if (result.success) {
        // Show OTP step
        document.getElementById('phoneStep').style.display = 'none';
        document.getElementById('otpStep').style.display = 'block';
        document.getElementById('displayPhone').textContent = '+91 ' + phone;
        
        // For demo, show OTP
        alert(`Demo OTP: ${result.otp}`);
    } else {
        alert('Error sending OTP. Please try again.');
    }
}

/**
 * Verify OTP and login
 */
async function verifyLoginOTP(phone, otp) {
    const result = await api.verifyOTP(phone, otp);
    
    if (result.success) {
        // Store token
        localStorage.setItem('authToken', result.token);
        localStorage.setItem('userPhone', phone);
        
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    } else {
        alert('Invalid OTP. Please try again.');
    }
}

// ===============================
// Export for use in HTML files
// ===============================
window.getLocation = getLocation;
window.handleEmergencySubmit = handleEmergencySubmit;
window.api = api;
