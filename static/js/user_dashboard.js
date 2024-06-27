document.addEventListener('DOMContentLoaded', function() {
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
    console.log(csrftoken);

    // Fetch user information and display it
    fetch('/api/putdelete', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user information.');
            }
            return response.json();
        })
        .then(user => {
            console.log('User Data:', user);
            // Display user information in the template
            var userInfo = `
            <div class="row">
                <div class="col-md-3">
                    <div class="profile-picture">
                        <img src="${user.userImage}" class="img-fluid " alt="Profile Picture">
                    </div>
                </div>
                <div class="col-md-9">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title">Name: ${user.first_name} ${user.last_name}</h3>
                            <p class="card-text">Email: ${user.email}</p>
                            <p class="card-text">Phone No: ${user.phoneNo}</p>
                            <p class="card-text">Team Name: ${user.team.TeamName}</p>
                            <p class="card-text">Team Stadium: ${user.team.TeamStadium}</p>
                            <p class="card-text">Team City: ${user.team.TeamCity}</p>
                        </div>
                    </div>
                </div>
            </div>`;
            // Log the user info HTML to the console
            console.log('User Info:', userInfo);

            // Select the user-info element using querySelector
            const userInfoElement = document.querySelector('.card-body');
            // Append userInfo HTML to the user-info element
            userInfoElement.innerHTML = userInfo;

            // Get references to the profile image and admin name elements
            const profileImage = document.getElementById('profile-image');
            const adminName = document.getElementById('admin-name');

            // Update the profile image source with the user's image
            profileImage.src = user.userImage;
            // Update the admin name with the user's first name
            adminName.textContent = user.first_name;

        })
        .catch(error => {
            console.error(error);

        });
});

// FOR USER PROFILE DETAILS
const updation = document.getElementById('updating');
const updationInfo = document.getElementById('updates');

updation.addEventListener('click', () => {
    updationInfo.style.display = 'block';
});

const close = document.getElementById('closing');
close.addEventListener('click', () => {
    updationInfo.style.display = 'none';
});