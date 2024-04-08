// $(document).ready(function() {
//     $('#register-form').submit(function(e) {
//         e.preventDefault(); // Prevent form submission
//         // Serialize the form data
//         var formData = $(this).serialize();
//         var csrfToken = "{{ csrf_token }}";
//         // Remove previous error styles
//         $('.field').removeClass('error-field');
//         // Make the AJAX request to the API endpoint
//         $.ajax({
//             headers: {
//                 "X-CSRFToken": csrfToken
//             },
//             url: '/api/registration',
//             type: 'POST',
//             data: new FormData(this),
//             contentType: false,
//             processData: false,
//             success: function(response) {
//                 // Handling the successful registration response
//                 console.log(response);
//                 alert('Registration successful');
//                 window.location.href = 'api/login/';
//             },
//             error: function(xhr, status, error) {
//                 // Handle the registration error
//                 console.log(xhr.responseText);
//                 var errors = JSON.parse(xhr.responseText);
//                 for (var key in errors) {
//                     $('[name="' + key + '"]').closest('.form-group').addClass('error-field');
//                 }
//                 var errorMessage = errors.email[0];
//                 $('#error-message').text(errorMessage);
//             }
//         });
//     });
// });


$(document).ready(function() {
    $('#register-form').submit(function(e) {
        e.preventDefault(); // Prevent form submission
        var formData = new FormData(this);
        var csrfToken = "{{ csrf_token }}";

        // Extract team data from input fields and add it to the formData object
        var teamData = {
            TeamName: $('[name="team[TeamName]"]').val(),
            TeamStadium: $('[name="team[TeamStadium]"]').val(),
            TeamCity: $('[name="team[TeamCity]"]').val()
        };
        formData.append('team', JSON.stringify(teamData));

        // Remove previous error styles
        $('.field').removeClass('error-field');

        // Make the AJAX request to the API endpoint
        $.ajax({
            headers: { "X-CSRFToken": csrfToken },
            url: '/api/registration',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // Handling the successful registration response
                console.log(response);
                alert('Registration successful');
                window.location.href = 'api/login/';
            },
            error: function(xhr, status, error) {
                // Handle the registration error
                console.log(xhr.responseText);
                var errors = JSON.parse(xhr.responseText);
                for (var key in errors) {
                    $('[name="' + key + '"]').closest('.form-group').addClass('error-field');
                }
                var errorMessage = errors.email[0];
                $('#error-message').text(errorMessage);
            }
        });
    });
});