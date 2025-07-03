// Update your search function to call the Flask API
document.getElementById('search-btn').addEventListener('click', async () => {
    const location = document.getElementById('search-location').value;
    const category = document.getElementById('search-category').value;
    
    if (!location || !category) {
        alert('தயவு செய்து இடம் மற்றும் வகையை தேர்ந்தெடுக்கவும்');
        return;
    }
    
    try {
        const response = await fetch(`YOUR_FLASK_API_URL/api/search?location=${location}&category=${category}`);
        const workers = await response.json();
        
        displayResults(workers);
    } catch (error) {
        console.error('Error:', error);
        alert('தேடல் தோல்வியுற்றது. மீண்டும் முயற்சிக்கவும்');
    }
});

function displayResults(workers) {
    const workerResults = document.getElementById('worker-results');
    workerResults.innerHTML = '';
    
    if (workers.length === 0) {
        workerResults.innerHTML = '<p>எந்த தொழிலாளர்களும் கிடைக்கவில்லை</p>';
        return;
    }
    
    workers.forEach(worker => {
        const workerCard = document.createElement('div');
        workerCard.className = 'worker-card';
        workerCard.innerHTML = `
            <div class="worker-name">${worker.name}</div>
            <div class="worker-details"><strong>தொலைபேசி:</strong> ${worker.phone}</div>
            <div class="worker-details"><strong>இடம்:</strong> ${worker.location}</div>
            <div class="worker-details"><strong>வேலை வகை:</strong> ${worker.category}</div>
            <div class="worker-details"><strong>சேவை தூரம்:</strong> ${worker.distance} கிமீ</div>
            <div class="worker-details"><strong>கட்டணம்:</strong> ₹${worker.charge}/நாள்</div>
            ${worker.experience ? `<div class="worker-details"><strong>அனுபவம்:</strong> ${worker.experience}</div>` : ''}
        `;
        workerResults.appendChild(workerCard);
    });
    
    document.getElementById('results-grid').style.display = 'block';
}
