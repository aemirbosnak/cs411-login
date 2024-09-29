document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const currentPage = window.location.pathname.split("/").pop();

    if (!token) {
        // Redirect to login if no token is found and the current page is not login.html
        if (currentPage !== 'login.html') {
            window.location.href = '../login/login.html';
        }
    } else {
        // Decode the token to get user info (you may need a library like jwt-decode)
        const user = JSON.parse(atob(token.split('.')[1]));

        // Set welcome message if the current page is dashboard.html
        if (currentPage === 'dashboard.html') {
            document.getElementById('welcomeMessage').innerText = `Welcome, ${user.firstName} ${user.lastName} (${user.role})!`;
        }

        // Logout button functionality
        const logoutButton = document.getElementById('logoutButton');
        if (logoutButton) { // Ensure the logout button exists
            logoutButton.addEventListener('click', function(event) {
                event.preventDefault();

                // Send a logout request to the backend
                fetch('http://localhost:5000/api/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        localStorage.removeItem('token');
                        window.location.href = '../login/login.html';
                    } else {
                        throw new Error('Logout failed');
                    }
                })
                .catch(error => {
                    alert(error.message);
                });
            });
        }
    }
});
