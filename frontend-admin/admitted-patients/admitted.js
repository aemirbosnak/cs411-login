document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');
    const admittedPatientsTableBody = document.querySelector('#admittedPatientsTable tbody');
    const addInpatientForm = document.getElementById('addInpatientForm');
    const patientIdInput = document.getElementById('patientId');

    if (!token) {
        alert('Not authorized. Redirecting to login...');
        window.location.href = '../login/login.html';
        return;
    }

    // Load admitted patients
    function loadAdmittedPatients() {
        fetch('http://localhost:5000/api/patient/admitted', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(data => {
            admittedPatientsTableBody.innerHTML = '';
            data.patients.forEach(p => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${p._id}</td>
                    <td>${p.firstName} ${p.lastName}</td>
                    <td>${p.complaint}</td>
                    <td>${p.severity}</td>
                    <td>${p.doctorId}</td>
                    <td><button class="select-patient-btn" data-id="${p._id}" data-doctor="${p.doctorId}">Select</button></td>
                `;
                admittedPatientsTableBody.appendChild(row);
            });

            document.querySelectorAll('.select-patient-btn').forEach(btn => {
                btn.addEventListener('click', function () {
                    patientIdInput.value = this.getAttribute('data-id');
                    document.getElementById('assignedDoctor').value = this.getAttribute('data-doctor');
                    alert('Patient selected. Fill the form below to create an inpatient entry.');
                });
            });
        })
        .catch(error => console.error('Error loading admitted patients:', error));
    }

    addInpatientForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const inpatientData = {
            patientId: patientIdInput.value,
            roomNumber: document.getElementById('roomNumber').value.trim(),
            assignedDoctor: document.getElementById('assignedDoctor').value.trim(),
            admissionReason: document.getElementById('admissionReason').value.trim(),
            admissionDate: document.getElementById('admissionDate').value,
            operationDetails: document.getElementById('operationDetails').value.trim() || null
        };

        fetch('http://localhost:5000/api/inpatient/add', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inpatientData)
        })
        .then(res => res.json())
        .then(data => {
            if (data.message === 'Inpatient entry created successfully') {
                alert('Inpatient added successfully!');
                addInpatientForm.reset();
                loadAdmittedPatients(); // refresh admitted patients list
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error adding inpatient:', error));
    });

    loadAdmittedPatients();
});
