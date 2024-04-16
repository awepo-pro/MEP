document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('nlpForm');
    const input = document.getElementById('input');
    const outputDiv = document.getElementById('output');
    let timer = null;  // Variable to keep track of the interval

    function sendData() {
        if (timer !== null) {  // Check if there's an existing timer
            clearInterval(timer);  // Clear the timer
            timer = null;
        }

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

    sendData();

    input.addEventListener('input', function() {
        if (timer !== null) {
            clearInterval(timer);  // If there's an existing timer, clear it
        }
        timer = setTimeout(sendData, 500);  // Reset the timer to send data after 0.5 seconds of inactivity
    });
});