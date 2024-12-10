document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');
    const inpatientTableBody = document.querySelector('#inpatientTable tbody');

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '../login/login.html';
        return;
    }

    // Load all inpatients
    function loadInpatients() {
        fetch('http://localhost:5000/api/inpatient/list', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            inpatientTableBody.innerHTML = ''; // Clear existing rows
            data.inpatients.forEach(inpatient => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${inpatient.patientId}</td>
                    <td>${inpatient.roomNumber}</td>
                    <td>${inpatient.assignedDoctor}</td>
                    <td>${inpatient.admissionReason}</td>
                    <td>${inpatient.admissionDate}</td>
                    <td>${inpatient.dischargeDate || 'N/A'}</td>
                `;
                inpatientTableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading inpatients:', error));
    }

    // Add new inpatient
    document.getElementById('addInpatientForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const inpatientData = {
            patientId: document.getElementById('patientId').value.trim(),
            roomNumber: document.getElementById('roomNumber').value.trim(),
            assignedDoctor: document.getElementById('assignedDoctor').value.trim(),
            admissionReason: document.getElementById('admissionReason').value.trim(),
            admissionDate: document.getElementById('admissionDate').value,
        };

        fetch('http://localhost:5000/api/inpatient/add', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inpatientData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Inpatient entry created successfully') {
                alert('Inpatient added successfully!');
                document.getElementById('addInpatientForm').reset();
                loadInpatients(); // Refresh the table
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error adding inpatient:', error));
    });

    loadInpatients(); // Load inpatients on page load
});
