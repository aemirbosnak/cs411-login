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
        console.log("list inpatients endpont called");
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
    
    loadInpatients(); // Load inpatients on page load
});
