document.addEventListener('DOMContentLoaded', function () {
    const admitForm = document.getElementById('admitPatientForm');
    const token = localStorage.getItem('token'); // Ensure token is stored in localStorage

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '/login/';
        return;
    }

    admitForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const doctorId = JSON.parse(atob(token.split('.')[1])).email; // Use doctor email as ID
        const patientData = {
            firstName: document.getElementById('firstName').value.trim(),
            lastName: document.getElementById('lastName').value.trim(),
            dob: document.getElementById('dob').value,
            gender: document.getElementById('gender').value,
            address: document.getElementById('address').value.trim(),
            contactNumber: document.getElementById('contactNumber').value.trim(),
            emergencyContact: document.getElementById('emergencyContact').value.trim(),
            insuranceInfo: document.getElementById('insuranceInfo').value.trim(),
            occupation: document.getElementById('occupation').value.trim(),
            maritalStatus: document.getElementById('maritalStatus').value,
            complaint: document.getElementById('complaint').value,
            severity: document.getElementById('severity').value,
            doctorId: doctorId
        };

        // Validate required fields
        if (!patientData.firstName || !patientData.lastName || !patientData.dob || !patientData.gender || !patientData.address || !patientData.contactNumber) {
            alert('Please fill out all required fields.');
            return;
        }

        fetch('http://localhost:5003/api/patient/admit', {
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


    console.log('Event listener attached to admit form');
});
