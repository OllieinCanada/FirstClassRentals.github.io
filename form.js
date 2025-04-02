// JavaScript code to handle form submission and AJAX request
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rentalForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Collect form data
        const formData = new FormData(form);
        
        // Convert FormData to JSON object
        const formDataJson = {};
        formData.forEach((value, key) => {
            formDataJson[key] = value;
        });

        // Send AJAX request to Flask backend
        fetch('/submit_form', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formDataJson),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Form submitted successfully!');
            // Optionally, redirect or perform further actions
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while submitting the form.');
        });
    });
});
