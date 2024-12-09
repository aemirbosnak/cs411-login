document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '../login/login.html';
        return;
    }

    const doctorId = JSON.parse(atob(token.split('.')[1])).email; // Use doctor email as ID
    const spinner = document.getElementById('loadingSpinner');
    const patientsTable = document.getElementById('patientsTable');
    const tableBody = patientsTable.querySelector('tbody');

    spinner.style.display = 'block'; // Show spinner
    patientsTable.style.display = 'none'; // Hide table initially

    fetch(`http://localhost:5000/api/patient/list?doctorId=${doctorId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.patients) {
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
                tableBody.innerHTML = `<tr><td colspan="6">No patients found.</td></tr>`;
            }
        })
        .catch(error => {
            console.error('Error fetching patients:', error);
            tableBody.innerHTML = `<tr><td colspan="6">Error loading patients.</td></tr>`;
        })
        .finally(() => {
            spinner.style.display = 'none'; // Hide spinner
            patientsTable.style.display = 'table'; // Show table
        });
});
