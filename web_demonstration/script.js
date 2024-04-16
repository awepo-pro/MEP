document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('nlpForm');
    const input = document.getElementById('input');
    const outputDiv = document.getElementById('output');

    function sendData() {
        const formData = new FormData(form);  // Create a FormData object, capturing form data
        fetch('process.php', {  // Assuming 'process.php' processes the form data and returns the output
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            outputDiv.innerHTML = data;  // Display the processed data in the output div
        })
        .catch(error => console.error('Error:', error));
    }

    setInterval(sendData, 5000);  // Set to send data every 5 seconds
});