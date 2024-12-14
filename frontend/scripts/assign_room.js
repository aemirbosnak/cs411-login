document.addEventListener('DOMContentLoaded', function () {
    const addRoomForm = document.getElementById('addRoomForm');

    // API base URL
    const apiBaseUrl = "http://localhost:5003/api/room";

    // Add Room Form Submission
    addRoomForm.addEventListener('submit', function (event) {
        console.log("submit clicked")
        event.preventDefault();

        const roomData = {
            roomNumber: document.getElementById('roomNumber').value.trim(),
            roomType: document.getElementById('roomType').value,
        };

        if (!roomData.roomNumber || !roomData.roomType) {
            alert('Please fill in all required fields.');
            return;
        }

        fetch(`${apiBaseUrl}/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(roomData),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("alert")
                if (data.error) {
                    alert(`Error: ${data.error}`);
                } else {
                    alert('Room successfully added!');
                    addRoomForm.reset();
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Failed to add the room.');
            });
    });
});
