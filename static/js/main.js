// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        });
    }, 5000);
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Password strength indicator
function checkPasswordStrength(password) {
    const strengthBar = document.getElementById('password-strength');
    if (!strengthBar) return;

    const strength = {
        1: 'Very Weak',
        2: 'Weak',
        3: 'Medium',
        4: 'Strong',
        5: 'Very Strong'
    };

    let score = 0;
    if (password.length >= 8) score++;
    if (password.match(/[a-z]/)) score++;
    if (password.match(/[A-Z]/)) score++;
    if (password.match(/[0-9]/)) score++;
    if (password.match(/[^a-zA-Z0-9]/)) score++;

    strengthBar.style.width = `${score * 20}%`;
    strengthBar.textContent = strength[score];
    strengthBar.className = `progress-bar bg-${score > 3 ? 'success' : score > 2 ? 'warning' : 'danger'}`;
}

// Seat selection functionality
function initializeSeatSelection() {
    const seatMap = document.getElementById('seat-map');
    if (!seatMap) return;

    seatMap.addEventListener('click', function(e) {
        if (e.target.classList.contains('seat')) {
            const seats = seatMap.getElementsByClassName('seat');
            Array.from(seats).forEach(seat => seat.classList.remove('selected'));
            e.target.classList.add('selected');
            document.getElementById('selected-seat').value = e.target.dataset.seat;
        }
    });
}

// Initialize all interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

    // Initialize seat selection if on booking page
    initializeSeatSelection();

    // Add password strength checker to registration form
    const passwordInput = document.querySelector('input[type="password"]');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });
    }
});
