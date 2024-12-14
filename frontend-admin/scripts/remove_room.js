document.addEventListener('DOMContentLoaded', function () {
    const addRoomForm = document.getElementById('removeRoomForm');

    // API base URL
    const apiBaseUrl = "http://localhost:5003/api/room";

    // Add Room Form Submission
    addRoomForm.addEventListener('submit', function (event) {
        console.log('submit clicked')
        event.preventDefault();

        const roomNumber = document.getElementById('removeRoomNumber').value.trim();
        console.log("roomNumber: ", roomNumber)

        fetch(`${apiBaseUrl}/remove/${roomNumber}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    alert(`Error: ${data.error}`);
                } else {
                    alert('Room successfully deleted!');
                    addRoomForm.reset();
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Failed to delete the room.');
            });
    });
});
