document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '../login/login.html';
        return;
    }

    const doctorId = JSON.parse(atob(token.split('.')[1])).email; // Use doctor email as ID

    fetch(`http://localhost:5000/api/patient/list?doctorId=${doctorId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.patients) {
            const tableBody = document.querySelector('#patientsTable tbody');
            tableBody.innerHTML = ''; // Clear table before populating

            data.patients.forEach(patient => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${patient.firstName}</td>
                    <td>${patient.lastName}</td>
                    <td>${patient.dob}</td>
                    <td>${patient.address}</td>
                    <td>${patient.complaint || 'N/A'}</td>
                    <td>${patient.severity || 'N/A'}</td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            alert('No patients found.');
        }
    })
    .catch(error => {
        console.error('Error fetching patients:', error);
        alert('Failed to fetch patients.');
    });
});
