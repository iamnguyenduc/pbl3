// autoreload.js

// Function to reload the page every 5 seconds
function reloadPage() {
    setTimeout(function () {
        location.reload();
    }, 5000); // 5000 milliseconds = 5 seconds
}

// Call the reloadPage function
reloadPage();