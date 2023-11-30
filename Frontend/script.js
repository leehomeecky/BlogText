document.addEventListener('DOMContentLoaded', function () {
    // Add your JavaScript code here

    // Example: Change the background color of the body
    document.body.style.backgroundColor = 'lightblue';

    // Example: Add a click event listener to the submit button
    var submitButton = document.querySelector('.btn-primary');
    submitButton.addEventListener('click', function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Add your form submission logic here
        console.log('Form submitted!');
    });
});
