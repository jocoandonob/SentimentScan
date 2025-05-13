document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const reviewForm = document.getElementById('review-form');
    const reviewText = document.getElementById('review-text');
    const analyzeBtn = document.getElementById('analyze-btn');
    const errorMessage = document.getElementById('error-message');

    // Results elements
    const resultsContainer = document.getElementById('results-container');
    const sentimentBadge = document.getElementById('sentiment-badge');
    const sentimentIcon = sentimentBadge.querySelector('.sentiment-icon');
    const sentimentLabel = document.getElementById('sentiment-label');
    const confidenceBar = document.getElementById('confidence-bar');
    const polarityValue = document.getElementById('polarity-value');
    const subjectivityValue = document.getElementById('subjectivity-value');
    const analyzeAnotherBtn = document.getElementById('analyze-another-btn');

    // Function to validate and submit the form
    reviewForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Reset any previous error state
        reviewText.classList.remove('is-invalid');
        errorMessage.textContent = '';
        
        // Get the review text
        const review = reviewText.value.trim();
        
        // Check if the review is empty
        if (!review) {
            reviewText.classList.add('is-invalid');
            errorMessage.textContent = 'Please enter a movie review to analyze';
            return;
        }
        
        // Show loading state
        analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing...';
        analyzeBtn.disabled = true;
        
        // Send the review to the server for analysis
        const formData = new FormData();
        formData.append('review', review);
        
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'An error occurred during analysis');
                });
            }
            return response.json();
        })
        .then(data => {
            // Update the results UI
            displayResults(data);
        })
        .catch(error => {
            // Show error message
            reviewText.classList.add('is-invalid');
            errorMessage.textContent = error.message;
        })
        .finally(() => {
            // Reset button state
            analyzeBtn.innerHTML = '<i class="fas fa-search me-2"></i>Analyze Sentiment';
            analyzeBtn.disabled = false;
        });
    });
    
    // Function to display the analysis results
    function displayResults(data) {
        // Update sentiment badge
        let iconClass = '';
        let badgeClass = '';
        let progressBarClass = '';
        
        // Configure badge based on sentiment
        switch (data.sentiment) {
            case 'positive':
                iconClass = 'fa-smile';
                badgeClass = 'positive';
                progressBarClass = 'bg-success';
                break;
            case 'negative':
                iconClass = 'fa-frown';
                badgeClass = 'negative';
                progressBarClass = 'bg-danger';
                break;
            case 'neutral':
                iconClass = 'fa-meh';
                badgeClass = 'neutral';
                progressBarClass = 'bg-warning';
                break;
        }
        
        // Update sentiment badge
        sentimentIcon.className = `sentiment-icon fas ${iconClass}`;
        sentimentLabel.textContent = data.sentiment.charAt(0).toUpperCase() + data.sentiment.slice(1);
        sentimentBadge.className = `sentiment-badge ${badgeClass}`;
        
        // Update confidence score
        confidenceBar.style.width = `${data.confidence}%`;
        confidenceBar.textContent = `${data.confidence}%`;
        confidenceBar.className = `progress-bar ${progressBarClass}`;
        
        // Update analysis explanation if it exists
        const analysisText = document.getElementById('analysis-text');
        if (analysisText && data.analysis) {
            analysisText.textContent = data.analysis;
        }
        
        // Show results container
        reviewForm.parentElement.parentElement.classList.add('d-none');
        resultsContainer.classList.remove('d-none');
    }
    
    // Function to reset the form and show it again
    analyzeAnotherBtn.addEventListener('click', function() {
        // Clear the form
        reviewText.value = '';
        
        // Hide results and show form
        resultsContainer.classList.add('d-none');
        reviewForm.parentElement.parentElement.classList.remove('d-none');
        
        // Focus on the textarea
        reviewText.focus();
    });
});
