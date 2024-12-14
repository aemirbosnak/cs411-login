document.addEventListener('DOMContentLoaded', function () {
    const navbarContainer = document.createElement('div');
    navbarContainer.id = 'navbarContainer';
    document.body.insertBefore(navbarContainer, document.body.firstChild);

    // Function to dynamically load CSS
    function loadCSS(href) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        link.type = 'text/css';
        document.head.appendChild(link);
    }

    // Load the navbar.html
    fetch('/components/doctor/navbar.html')
        .then(response => response.text())
        .then(html => {
            navbarContainer.innerHTML = html;

            // Load the navbar.css dynamically
            loadCSS('/components/doctor/navbar.css');

            // Add logout functionality
            const logoutButton = document.getElementById('logoutButton');
            if (logoutButton) {
                logoutButton.addEventListener('click', function() {
                    localStorage.removeItem('token');
                    localStorage.removeItem('role');
                    window.location.href = '/login/';
                });
            }
        })
        .catch(error => console.error('Error loading navbar:', error));
});
