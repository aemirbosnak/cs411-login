document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');
    const admitForm = document.getElementById('admitPatientForm');

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '../login/login.html';
        return;
    }

    admitForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const doctorId = JSON.parse(atob(token.split('.')[1])).email; // Use doctor email as ID
        const patientData = {
            firstName: document.getElementById('firstName').value,
            lastName: document.getElementById('lastName').value,
            dob: document.getElementById('dob').value,
            address: document.getElementById('address').value,
            doctorId: doctorId
        };

        fetch('http://localhost:5000/api/patient/admit', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(patientData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Patient admitted successfully') {
                alert('Patient admitted successfully!');
                admitForm.reset();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
