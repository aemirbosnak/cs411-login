document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password, role: 'admin' })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Login failed');
    })
    .then(data => {
        // Store the token in local storage
        localStorage.setItem('token', data.token);
        window.location.href = '../dashboard/dashboard.html';
    })
    .catch(error => {
        alert(error.message);
    });
});
