document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token'); // Ensure token is stored in localStorage

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '/login/';
        return;
    }

    const loadingSpinner = document.getElementById('loadingSpinner');
    const roomsTable = document.getElementById('roomsTable');
    const filterStatus = document.getElementById('filterStatus');
    const tbody = roomsTable.querySelector('tbody');

    // Fetch rooms data
    async function fetchRooms() {
        try {
            const response = await fetch('http://localhost:5003/api/rooms', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch room data');
            }

            const rooms = await response.json();
            renderRooms(rooms);
            return rooms;
        } catch (error) {
            console.error('Error fetching rooms:', error);
        }
    }

    // Render rooms into the table
    function renderRooms(rooms) {
        tbody.innerHTML = ''; // Clear table body
        rooms.forEach(room => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${room.roomNumber}</td>
                <td>${room.roomType}</td>
                <td>${room.status}</td>
                <td>${room.assignedPatient || 'N/A'}</td>
            `;
            tbody.appendChild(row);
        });
        loadingSpinner.style.display = 'none';
        roomsTable.style.display = 'table';
    }

    // Filter rooms by status
    function filterRooms(status, rooms) {
        const filteredRooms = rooms.filter(room => {
            if (status === 'empty') return room.status === 'Empty';
            if (status === 'assigned') return room.status === 'Assigned';
            return true; // 'all'
        });
        renderRooms(filteredRooms);
    }

    // Event listener for filter dropdown
    filterStatus.addEventListener('change', async function () {
        const status = filterStatus.value;
        const rooms = await fetchRooms();
        filterRooms(status, rooms);
    });

    // Initialize page
    (async function init() {
        const rooms = await fetchRooms();
        filterRooms('all', rooms); // Default to showing all rooms
    })();
});
