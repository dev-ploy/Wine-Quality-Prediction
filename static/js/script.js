// Wine Quality Prediction - Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    
    // Form validation and enhancement
    const form = document.getElementById('predictionForm');
    const submitBtn = form?.querySelector('.btn-primary');
    
    if (form) {
        // Add input animations
        const inputs = form.querySelectorAll('input[type="number"]');
        
        inputs.forEach(input => {
            // Add focus effects
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
                this.parentElement.style.transition = 'transform 0.3s ease';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
            
            // Real-time validation
            input.addEventListener('input', function() {
                validateInput(this);
            });
        });
        
        // Form submission
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return;
            }
            
            // Add loading state
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.textContent = 'Analyzing...';
            }
        });
    }
    
    // Sample data filler
    const sampleBtn = document.getElementById('fillSample');
    if (sampleBtn) {
        sampleBtn.addEventListener('click', function() {
            fillSampleData();
        });
    }
    
    // Quality bar animation on results page
    const qualityFill = document.querySelector('.quality-fill');
    if (qualityFill) {
        const targetWidth = qualityFill.style.width;
        qualityFill.style.width = '0%';
        
        setTimeout(() => {
            qualityFill.style.width = targetWidth;
        }, 500);
    }
});

// Validate individual input
function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    if (isNaN(value)) {
        input.style.borderColor = '#ef4444';
        return false;
    }
    
    if ((min && value < min) || (max && value > max)) {
        input.style.borderColor = '#f59e0b';
        return false;
    }
    
    input.style.borderColor = '#10b981';
    return true;
}

// Validate entire form
function validateForm() {
    const inputs = document.querySelectorAll('input[type="number"]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateInput(input)) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        showNotification('Please check all fields and ensure valid values', 'error');
    }
    
    return isValid;
}

// Fill sample data for testing
function fillSampleData() {
    const sampleData = {
        'fixed_acidity': 7.4,
        'volatile_acidity': 0.7,
        'citric_acid': 0.0,
        'residual_sugar': 1.9,
        'chlorides': 0.076,
        'free_sulfur_dioxide': 11.0,
        'total_sulfur_dioxide': 34.0,
        'density': 0.9978,
        'pH': 3.51,
        'sulphates': 0.56,
        'alcohol': 9.4
    };
    
    Object.keys(sampleData).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            input.value = sampleData[key];
            
            // Animate the fill
            input.style.transform = 'scale(1.1)';
            input.style.borderColor = '#10b981';
            
            setTimeout(() => {
                input.style.transform = 'scale(1)';
            }, 200);
        }
    });
    
    showNotification('Sample data loaded successfully!', 'success');
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        font-weight: 600;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add CSS for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
