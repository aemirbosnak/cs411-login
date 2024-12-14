document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('http://localhost:5003/api/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, password, role: 'doctor' }) // currently doctor
    })
    .then(response => response.ok ? response.json() : Promise.reject('Login failed'))
    .then(data => {
        localStorage.setItem('token', data.token);
        localStorage.setItem('role', data.user.role);
        window.location.href = '/dashboard/';
    })
    .catch(error => alert(error));
});
