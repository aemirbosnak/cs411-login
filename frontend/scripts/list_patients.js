document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');
    console.log(token)

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '/login/';
        return;
    }

    const doctorId = JSON.parse(atob(token.split('.')[1])).email; // Use doctor email as ID
    const spinner = document.getElementById('loadingSpinner');
    const patientsTable = document.getElementById('patientsTable');
    const tableBody = patientsTable.querySelector('tbody');

    spinner.style.display = 'block'; // Show spinner
    patientsTable.style.display = 'none'; // Hide table initially

    const apiUrl = `http://localhost:5003/api/patient/list${doctorId ? `?doctorId=${encodeURIComponent(doctorId)}` : ''}`;

    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.patients && data.patients.length > 0) {
                tableBody.innerHTML = ''; // Clear table before populating

                data.patients.forEach(patient => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${patient.firstName}</td>
                        <td>${patient.lastName}</td>
                        <td>${patient.dob || 'N/A'}</td>
                        <td>${patient.gender || 'N/A'}</td>
                        <td>${patient.address || 'N/A'}</td>
                        <td>${patient.contactNumber || 'N/A'}</td>
                        <td>${patient.emergencyContact || 'N/A'}</td>
                        <td>${patient.insuranceInfo || 'N/A'}</td>
                        <td>${patient.occupation || 'N/A'}</td>
                        <td>${patient.maritalStatus || 'N/A'}</td>
                        <td>${patient.complaint || 'N/A'}</td>
                        <td>${patient.severity || 'N/A'}</td>
                        <td>${patient.roomNumber || 'N/A'}</td>
                        <td>${patient.admissionReason || 'N/A'}</td>
                        <td>${patient.admissionDate || 'N/A'}</td>
                        <td>${patient.dischargeDate || 'N/A'}</td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                tableBody.innerHTML = `<tr><td colspan="16">No patients found.</td></tr>`;
            }
        })
        .catch(error => {
            console.error('Error fetching patients:', error);
            tableBody.innerHTML = `<tr><td colspan="16">Error loading patients.</td></tr>`;
        })
        .finally(() => {
            spinner.style.display = 'none'; // Hide spinner
            patientsTable.style.display = 'table'; // Show table
        });
});
