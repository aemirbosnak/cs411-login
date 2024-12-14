document.addEventListener('DOMContentLoaded', function () {
    const admitForm = document.getElementById('admitPatientForm');
    console.log(admitForm)
    const token = localStorage.getItem('token'); // Ensure token is stored in localStorage

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '/login/';
        return;
    }

    admitForm.addEventListener('submit', function (event) {
        console.log('button clicked');
        event.preventDefault();

        const doctorId = JSON.parse(atob(token.split('.')[1])).email; // Use doctor email as ID
        const patientData = {
            firstName: document.getElementById('firstName').value.trim(),
            lastName: document.getElementById('lastName').value.trim(),
            dob: document.getElementById('dob').value,
            doctorId: doctorId,
            admissionReason: document.getElementById('admissionReason').value.trim(),
            gender: document.getElementById('gender').value || 'N/A', // Optional field
            address: document.getElementById('address').value.trim() || 'N/A',
            contactNumber: document.getElementById('contactNumber').value.trim() || 'N/A',
            emergencyContact: document.getElementById('emergencyContact').value.trim() || 'N/A',
            insuranceInfo: document.getElementById('insuranceInfo').value.trim() || 'N/A',
            occupation: document.getElementById('occupation').value.trim() || 'N/A',
            maritalStatus: document.getElementById('maritalStatus').value || 'N/A',
            complaint: document.getElementById('complaint').value.trim() || 'N/A',
            severity: document.getElementById('severity').value || 'low', // Default to "low"
            roomNumber: document.getElementById('roomNumber').value.trim() || null,
            admissionDate: document.getElementById('admissionDate').value || new Date().toISOString(),
            operationDetails: document.getElementById('operationDetails').value.trim() || null // Optional field
        };

        // Validate required fields
        if (!patientData.firstName || !patientData.lastName || !patientData.dob || !patientData.doctorId || !patientData.admissionReason) {
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
