document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token'); // Ensure token is stored in localStorage

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '/login/';
        return;
    }

    const loadingSpinner = document.getElementById('loadingSpinner');
    const roomsTable = document.getElementById('roomsTable');
    const tbody = roomsTable.querySelector('tbody');

    let allRooms = []; // Cache all rooms for filtering

    // Fetch rooms data
    async function fetchRooms() {
        try {
            const response = await fetch('http://localhost:5003/api/room/list', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch room data');
            }

            const data = await response.json();
            allRooms = data.rooms || [];
            renderRooms(allRooms);
        } catch (error) {
            console.error('Error fetching rooms:', error);
            alert('Error fetching room data. Please try again later.');
        } finally {
            loadingSpinner.style.display = 'none';
            roomsTable.style.display = 'table';
        }
    }

    // Render rooms into the table
    function renderRooms(rooms) {
        tbody.innerHTML = ''; // Clear table body
        if (rooms.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7">No rooms found.</td></tr>`;
            return;
        }

        rooms.forEach(room => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${room.roomNumber}</td>
                <td>${room.occupied ? 'Assigned' : 'Empty'}</td>
                <td>${room.patientFirstName && room.patientLastName ? `${room.patientFirstName} ${room.patientLastName}` : 'N/A'}</td>
                <td>${room.admissionDate || 'N/A'}</td>
                <td>${room.admissionReason || 'N/A'}</td>
                <td>${room.operationDetails || 'N/A'}</td>
            `;
            tbody.appendChild(row);
        });
    }
    
    // Initialize page
    (async function init() {
        loadingSpinner.style.display = 'block';
        roomsTable.style.display = 'none';
        await fetchRooms();
        await fetchDoctors();
        filterRooms(); // Apply default filters
    })();
});
