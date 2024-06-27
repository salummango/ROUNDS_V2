document.addEventListener('DOMContentLoaded', function() {
    var logoutButton = document.getElementById('logout-button');

    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();

            if (confirm("Are you sure you want to log out?")) {
                console.log('Logout confirmed');

                // Fetch CSRF token from the cookie
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = cookies[i].trim();
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }

                var csrftoken = getCookie('csrftoken');

                // Perform AJAX logout request
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/api/logout/');
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('X-CSRFToken', csrftoken); // Include CSRF token
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        console.log('Logout successful');
                        localStorage.removeItem('jwt');
                        window.location.href = '/'; // Redirect to homepage after logout
                    } else {
                        console.error('Failed to log out:', xhr.responseText);
                        alert('Failed to log out. Please try again.');
                    }
                };
                xhr.onerror = function() {
                    console.error('Network error occurred');
                    alert('Network error occurred. Please try again.');
                };
                xhr.send();

            } else {
                console.log('Logout canceled');
                return false;
            }
        });
    } else {
        console.error('Logout button not found');
    }
});