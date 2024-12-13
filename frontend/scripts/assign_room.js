document.addEventListener('DOMContentLoaded', function () {
    const assignRoomForm = document.getElementById('assignRoomForm');
    const token = localStorage.getItem('token'); // Ensure token is stored in localStorage

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '/login/';
        return;
    }

    assignRoomForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const staffId = JSON.parse(atob(token.split('.')[1])).email; // Use staff email as ID
        const roomData = {
            patientId: document.getElementById('patientId').value.trim(),
            roomNumber: document.getElementById('roomNumber').value.trim(),
            roomType: document.getElementById('roomType').value,
            assigningStaff: staffId
        };

        // Validate required fields
        if (!roomData.patientId || !roomData.roomNumber || !roomData.roomType) {
            alert('Please fill out all required fields.');
            return;
        }

        fetch('http://localhost:5003/api/room/assign', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(roomData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.message === 'Room assigned successfully') {
                    alert('Room assigned successfully!');
                    assignRoomForm.reset();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    console.log('Event listener attached to room assignment form');
});
