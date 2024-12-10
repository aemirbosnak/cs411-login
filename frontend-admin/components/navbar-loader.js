document.addEventListener('DOMContentLoaded', function () {
    const navbarContainer = document.createElement('div');
    navbarContainer.id = 'navbarContainer';
    document.body.insertBefore(navbarContainer, document.body.firstChild);

    fetch('../components/navbar.html')
        .then(response => response.text())
        .then(html => {
            navbarContainer.innerHTML = html;

            // Add logout functionality
            const logoutButton = document.getElementById('logoutButton');
            if (logoutButton) {
                logoutButton.addEventListener('click', function () {
                    localStorage.removeItem('token');
                    window.location.href = '../login/login.html';
                });
            }
        })
        .catch(error => console.error('Error loading navbar:', error));
});
