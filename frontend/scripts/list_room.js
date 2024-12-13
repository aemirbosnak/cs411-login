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
    const filterDoctor = document.getElementById('filterDoctor');
    const tbody = roomsTable.querySelector('tbody');

    let allRooms = []; // Cache all rooms for filtering

    // Fetch rooms data
    async function fetchRooms() {
        try {
            const response = await fetch('http://localhost:5003/api/admission/rooms/available', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch room data');
            }

            const data = await response.json();
            allRooms = data.rooms;
            renderRooms(allRooms);
        } catch (error) {
            console.error('Error fetching rooms:', error);
            alert('Error fetching room data. Please try again later.');
        }
    }

    // Fetch doctors for the filter
    async function fetchDoctors() {
        try {
            const response = await fetch('http://localhost:5003/api/doctors', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch doctor data');
            }

            const doctors = await response.json();
            populateDoctorFilter(doctors);
        } catch (error) {
            console.error('Error fetching doctors:', error);
            alert('Error fetching doctor data. Please try again later.');
        }
    }

    // Populate doctor filter options
    function populateDoctorFilter(doctors) {
        doctors.forEach(doctor => {
            const option = document.createElement('option');
            option.value = doctor.email;
            option.textContent = doctor.name || doctor.email;
            filterDoctor.appendChild(option);
        });
    }

    // Render rooms into the table
    function renderRooms(rooms) {
        tbody.innerHTML = ''; // Clear table body
        rooms.forEach(room => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${room.roomNumber}</td>
                <td>${room.status}</td>
                <td>${room.assignedPatient || 'N/A'}</td>
                <td>${room.assignedDoctor || 'N/A'}</td>
                <td>${room.admissionDate || 'N/A'}</td>
                <td>${room.admissionReason || 'N/A'}</td>
                <td>${room.operationDetails || 'N/A'}</td>
            `;
            tbody.appendChild(row);
        });
        loadingSpinner.style.display = 'none';
        roomsTable.style.display = 'table';
    }

    // Filter rooms based on selected filters
    function filterRooms() {
        const status = filterStatus.value;
        const doctor = filterDoctor.value;

        let filteredRooms = allRooms;

        if (status !== 'all') {
            filteredRooms = filteredRooms.filter(room =>
                status === 'empty' ? room.status === 'Empty' : room.status === 'Assigned'
            );
        }

        if (doctor !== 'all') {
            filteredRooms = filteredRooms.filter(room => room.assignedDoctor === doctor);
        }

        renderRooms(filteredRooms);
    }

    // Event listener for filter dropdowns
    filterStatus.addEventListener('change', filterRooms);
    filterDoctor.addEventListener('change', filterRooms);

    // Initialize page
    (async function init() {
        loadingSpinner.style.display = 'block';
        roomsTable.style.display = 'none';
        await fetchRooms();
        await fetchDoctors();
        filterRooms(); // Apply default filters
    })();
});
