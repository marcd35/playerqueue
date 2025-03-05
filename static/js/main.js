// Queue Tracker Client-side JavaScript
// static\js\main.js

// DOM elements
const startQueueCard = document.getElementById('start-queue-card');
const updateQueueCard = document.getElementById('update-queue-card');
const startQueueSize = document.getElementById('start-queue-size');
const startQueueBtn = document.getElementById('start-queue-btn');
const updateQueueSize = document.getElementById('update-queue-size');
const updateQueueBtn = document.getElementById('update-queue-btn');
const queueMessage = document.getElementById('queue-message');
const statusContainer = document.getElementById('status-container');
const statusDetails = document.getElementById('status-details');

// Fetch current status on page load
window.addEventListener('load', fetchStatus);

// Poll for status updates every second
setInterval(fetchStatus, 1000);

// Start queue
startQueueBtn.addEventListener('click', async () => {
    const queueSize = parseInt(startQueueSize.value);
    if (isNaN(queueSize) || queueSize <= 0) {
        alert('Please enter a valid queue size (greater than 0)');
        return;
    }
    
    try {
        const response = await fetch('/start_queue', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ queue_size: queueSize })
        });
        
        const data = await response.json();
        if (data.success) {
            updateQueueSize.value = queueSize;
            updateStatus(data.status);
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error starting queue:', error);
        alert('An error occurred while starting the queue.');
    }
});

// Update queue
updateQueueBtn.addEventListener('click', async () => {
    const queueSize = parseInt(updateQueueSize.value);
    if (isNaN(queueSize) || queueSize < 0) {
        alert('Please enter a valid queue size (0 or greater)');
        return;
    }
    
    try {
        const response = await fetch('/update_queue', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ queue_size: queueSize })
        });
        
        const data = await response.json();
        if (data.success) {
            updateStatus(data.status);
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error updating queue:', error);
        alert('An error occurred while updating the queue.');
    }
});

// Fetch status
async function fetchStatus() {
    try {
        const response = await fetch('/get_status');
        const data = await response.json();
        updateStatus(data);
    } catch (error) {
        console.error('Error fetching status:', error);
    }
}

// Update UI with status
function updateStatus(status) {
    if (status.is_active) {
        startQueueCard.classList.add('hidden');
        updateQueueCard.classList.remove('hidden');
        statusContainer.classList.remove('hidden');
        queueMessage.classList.remove('hidden');
        
        queueMessage.textContent = `Estimated completion time: ${status.estimated_finish_time}`;
        queueMessage.style.color = '#4CAF50';
        
        statusDetails.innerHTML = `
            <div class="status-item">
                <span class="status-label">Current Queue Size:</span>
                <span class="status-value">${status.current_size} people</span>
            </div>
            <div class="status-item">
                <span class="status-label">Initial Queue Size:</span>
                <span class="status-value">${status.initial_size} people</span>
            </div>
            <div class="status-item">
                <span class="status-label">Queue Started:</span>
                <span class="status-value">${status.start_time}</span>
            </div>
            <div class="status-item">
                <span class="status-label">Current Time:</span>
                <span class="status-value">${status.current_time}</span>
            </div>
            <div class="status-item">
                <span class="status-label">Elapsed Time:</span>
                <span class="status-value">${status.elapsed_time}</span>
            </div>
            <div class="status-item">
                <span class="status-label">Average Time Per Person:</span>
                <span class="status-value">${status.estimated_time_per_person} (${status.raw_seconds_per_person} seconds)</span>
            </div>
            <div class="status-item">
                <span class="status-label">Estimated Finish Time:</span>
                <span class="status-value">${status.estimated_finish_time}</span>
            </div>
            <div class="status-item">
                <span class="status-label">Remaining Time:</span>
                <span class="status-value">${status.remaining_time}</span>
            </div>
        `;
    } else if (status.message === "Queue complete") {
        startQueueCard.classList.remove('hidden');
        updateQueueCard.classList.add('hidden');
        statusContainer.classList.add('hidden');
        queueMessage.classList.remove('hidden');
        queueMessage.textContent = `Queue completed at ${status.finish_time}`;
        queueMessage.style.color = '#4CAF50';
    } else {
        startQueueCard.classList.remove('hidden');
        updateQueueCard.classList.add('hidden');
        statusContainer.classList.add('hidden');
        queueMessage.classList.add('hidden');
    }
}