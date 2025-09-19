// Results page JavaScript

// Global variables
let currentResults = null;
let resultId = null;

// Initialize results page
document.addEventListener('DOMContentLoaded', () => {
    // Get result ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    resultId = urlParams.get('id');
    
    if (resultId) {
        loadResults();
    } else {
        // Show sample results for demo purposes
        loadSampleResults();
    }
    
    // Set up modal functionality
    setupModals();
});

// Load results from backend
async function loadResults() {
    try {
        showLoadingState();
        
        // TODO: Replace with actual API call
        // const response = await fetch(`/api/results/${resultId}`, {
        //     headers: {
        //         'Authorization': `Bearer ${localStorage.getItem('token')}`
        //     }
        // });
        
        // For now, simulate API response
        setTimeout(() => {
            const sampleResults = generateSampleResults();
            displayResults(sampleResults);
        }, 2000);
        
    } catch (error) {
        console.error('Error loading results:', error);
        showErrorState();
    }
}

// Load sample results for demonstration
function loadSampleResults() {
    setTimeout(() => {
        const sampleResults = generateSampleResults();
        displayResults(sampleResults);
    }, 1500);
}

// Generate sample results for demo
function generateSampleResults() {
    return {
        hasLearningDifference: true,
        primaryType: 'dyslexia',
        categoryScores: {
            dyslexia: 28,
            dyscalculia: 15,
            dysgraphia: 12
        },
        totalScore: 55,
        mentalHealthFlag: false,
        confidence: 0.87,
        recommendations: [
            {
                type: 'professional',
                message: 'Consult with a qualified educational psychologist for a comprehensive evaluation.'
            },
            {
                type: 'educational',
                message: 'Consider structured literacy programs and multisensory reading approaches.'
            },
            {
                type: 'general',
                message: 'Maintain regular communication with your child\'s teachers about learning accommodations.'
            },
            {
                type: 'disclaimer',
                message: 'This screening is not a diagnosis. Always consult qualified professionals for comprehensive assessment.'
            }
        ]
    };
}

// Show loading state
function showLoadingState() {
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('errorState').style.display = 'none';
    document.getElementById('resultsContent').style.display = 'none';
}

// Show error state
function showErrorState() {
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('errorState').style.display = 'block';
    document.getElementById('resultsContent').style.display = 'none';
}

// Display results
function displayResults(results) {
    currentResults = results;
    
    // Hide loading and error states
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('errorState').style.display = 'none';
    
    // Populate main result card
    populateMainResultCard(results);
    
    // Populate detailed results
    populateDetailedResults(results);
    
    // Populate recommendations
    populateRecommendations(results.recommendations || []);
    
    // Show results content
    document.getElementById('resultsContent').style.display = 'block';
}

// Populate main result card
function populateMainResultCard(results) {
    const resultIcon = document.getElementById('resultIcon');
    const mainResultTitle = document.getElementById('mainResultTitle');
    const resultSummary = document.getElementById('resultSummary');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceText = document.getElementById('confidenceText');
    
    if (results.hasLearningDifference) {
        resultIcon.textContent = '🎯';
        mainResultTitle.textContent = 'Learning Difference Detected';
        resultSummary.textContent = `Based on the screening responses, there are indicators suggesting a learning difference, with characteristics most consistent with ${results.primaryType}. This information can help guide next steps for support and evaluation.`;
    } else {
        resultIcon.textContent = '🌈';
        mainResultTitle.textContent = 'Typical Learning Profile';
        resultSummary.textContent = 'The screening results suggest a typical learning profile. Continue to monitor and support your child\'s educational journey with regular check-ins.';
    }
    
    // Set confidence level
    const confidencePercent = Math.round(results.confidence * 100);
    confidenceFill.style.width = `${confidencePercent}%`;
    confidenceText.textContent = `${confidencePercent}%`;
}

// Populate detailed results
function populateDetailedResults(results) {
    // Learning Difference Status
    const ldStatus = document.getElementById('ldStatus');
    const ldDescription = document.getElementById('ldDescription');
    
    ldStatus.innerHTML = `<span class="status-text">${results.hasLearningDifference ? 'Learning difference indicators detected' : 'No significant indicators detected'}</span>`;
    ldStatus.className = `status-indicator ${results.hasLearningDifference ? 'positive' : 'negative'}`;
    
    if (results.hasLearningDifference) {
        ldDescription.textContent = 'The screening suggests characteristics that may indicate a learning difference. Professional evaluation is recommended for comprehensive assessment.';
    } else {
        ldDescription.textContent = 'The screening results fall within typical ranges. Continue supporting your child\'s learning with regular monitoring.';
    }
    
    // Primary Type
    const typeIndicator = document.getElementById('typeIndicator');
    const typeName = document.getElementById('typeName');
    const typeDescription = document.getElementById('typeDescription');
    
    if (results.hasLearningDifference && results.primaryType) {
        const typeInfo = getTypeInfo(results.primaryType);
        typeIndicator.querySelector('.type-icon').textContent = typeInfo.icon;
        typeName.textContent = typeInfo.name;
        typeDescription.textContent = typeInfo.description;
    } else {
        typeIndicator.querySelector('.type-icon').textContent = '🌟';
        typeName.textContent = 'Balanced Profile';
        typeDescription.textContent = 'No single area shows significant concern patterns.';
    }
    
    // Category Scores
    populateCategoryScores(results.categoryScores);
    
    // Mental Health Status
    populateMentalHealthStatus(results.mentalHealthFlag);
}

// Get type information
function getTypeInfo(type) {
    const typeMap = {
        dyslexia: {
            name: 'Reading & Language',
            icon: '📖',
            description: 'Indicators suggest challenges primarily in reading, spelling, and language processing areas.'
        },
        dyscalculia: {
            name: 'Math & Numbers',
            icon: '🔢',
            description: 'Indicators suggest challenges primarily in mathematical concepts and number processing.'
        },
        dysgraphia: {
            name: 'Writing & Expression',
            icon: '✏️',
            description: 'Indicators suggest challenges primarily in writing, fine motor skills, and written expression.'
        }
    };
    
    return typeMap[type] || { name: 'Mixed Profile', icon: '🎯', description: 'Multiple areas show indicators.' };
}

// Populate category scores with animation
function populateCategoryScores(scores) {
    const maxScore = Math.max(...Object.values(scores));
    
    Object.entries(scores).forEach(([category, score]) => {
        const scoreElement = document.getElementById(`${category}Score`);
        const valueElement = document.getElementById(`${category}Value`);
        
        // Calculate percentage (assuming max possible score is around 34 for each category)
        const percentage = Math.min(100, (score / 34) * 100);
        
        // Animate the score bar
        setTimeout(() => {
            scoreElement.style.width = `${percentage}%`;
            valueElement.textContent = score;
        }, 500);
    });
}

// Populate mental health status
function populateMentalHealthStatus(flagged) {
    const mentalHealthStatus = document.getElementById('mentalHealthStatus');
    const mhTitle = document.getElementById('mhTitle');
    const mhDescription = document.getElementById('mhDescription');
    
    if (flagged) {
        mentalHealthStatus.className = 'mental-health-status flagged';
        mentalHealthStatus.querySelector('.mh-icon').textContent = '💛';
        mhTitle.textContent = 'Additional Support Recommended';
        mhDescription.textContent = 'Some responses suggest your child might benefit from emotional or behavioral support. Consider discussing with a counselor or pediatrician.';
    } else {
        mentalHealthStatus.className = 'mental-health-status';
        mentalHealthStatus.querySelector('.mh-icon').textContent = '💚';
        mhTitle.textContent = 'Emotional Well-being Appears Stable';
        mhDescription.textContent = 'The responses don\'t indicate significant emotional or behavioral concerns at this time.';
    }
}

// Populate recommendations
function populateRecommendations(recommendations) {
    const recommendationsGrid = document.getElementById('recommendationsGrid');
    recommendationsGrid.innerHTML = '';
    
    recommendations.forEach(recommendation => {
        const card = createRecommendationCard(recommendation);
        recommendationsGrid.appendChild(card);
    });
}

// Create recommendation card
function createRecommendationCard(recommendation) {
    const card = document.createElement('div');
    card.className = `recommendation-card ${recommendation.type}`;
    
    const icon = getRecommendationIcon(recommendation.type);
    const title = getRecommendationTitle(recommendation.type);
    
    card.innerHTML = `
        <div class="rec-icon">${icon}</div>
        <div class="rec-content">
            <h4>${title}</h4>
            <p>${recommendation.message}</p>
        </div>
    `;
    
    return card;
}

// Get recommendation icon
function getRecommendationIcon(type) {
    const iconMap = {
        professional: '👩‍⚕️',
        educational: '📚',
        support: '🤝',
        general: '💡',
        disclaimer: '⚠️'
    };
    
    return iconMap[type] || '💡';
}

// Get recommendation title
function getRecommendationTitle(type) {
    const titleMap = {
        professional: 'Professional Consultation',
        educational: 'Educational Support',
        support: 'Additional Support',
        general: 'General Guidance',
        disclaimer: 'Important Notice'
    };
    
    return titleMap[type] || 'Recommendation';
}

// Save results to profile
async function saveResults() {
    if (!currentResults) {
        alert('No results to save');
        return;
    }
    
    try {
        // TODO: Implement actual save functionality
        // const response = await fetch('/api/results/save', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'Authorization': `Bearer ${localStorage.getItem('token')}`
        //     },
        //     body: JSON.stringify(currentResults)
        // });
        
        // For now, just show success message
        alert('Results saved to your profile successfully! 🎉');
        
    } catch (error) {
        console.error('Error saving results:', error);
        alert('Failed to save results. Please try again.');
    }
}

// Share results functionality
function shareResults() {
    const shareModal = document.getElementById('shareModal');
    shareModal.style.display = 'block';
    
    // Generate shareable link (demo)
    const shareLink = document.getElementById('shareLink');
    const demoLink = `${window.location.origin}/results?shared=${Date.now()}`;
    shareLink.value = demoLink;
}

// Copy share link
function copyShareLink() {
    const shareLink = document.getElementById('shareLink');
    shareLink.select();
    document.execCommand('copy');
    alert('Link copied to clipboard! 📋');
}

// Email results
function emailResults() {
    const subject = encodeURIComponent('Learning Helper - Screening Results');
    const body = encodeURIComponent(`Please find the learning difference screening results at: ${document.getElementById('shareLink').value}`);
    
    window.open(`mailto:?subject=${subject}&body=${body}`);
}

// Show profile (placeholder)
function showProfile() {
    alert('Profile functionality coming soon! 👤');
}

// Setup modal functionality
function setupModals() {
    const shareModal = document.getElementById('shareModal');
    const closeButtons = document.querySelectorAll('.modal .close');
    
    // Close modals when clicking close button
    closeButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.target.closest('.modal').style.display = 'none';
        });
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === shareModal) {
            shareModal.style.display = 'none';
        }
    });
}