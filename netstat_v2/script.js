document.addEventListener("DOMContentLoaded", function() {
    // Fetch results from output.txt
    fetch('output.txt')
        .then(response => response.text())
        .then(data => {
            const openPorts = data.split('\n'); // assuming each line represents a port

            // Select the ul element where we will add list items
            const openPortsList = document.getElementById('openPorts');

            // Iterate through each open port and create a list item
            openPorts.forEach(portInfo => {
                if (portInfo.trim() !== '') {
                    const listItem = document.createElement('li');
                    listItem.textContent = portInfo;
                    openPortsList.appendChild(listItem);
                }
            });

            // If no open ports found, display a message
            if (openPorts.length === 0) {
                const listItem = document.createElement('li');
                listItem.textContent = 'No open ports found';
                openPortsList.appendChild(listItem);
            }
        })
        .catch(error => console.error('Error fetching data:', error));
});
