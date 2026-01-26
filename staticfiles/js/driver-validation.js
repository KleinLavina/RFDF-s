/**
 * Driver Registration Form Validator
 * Provides real-time validation using rules from validation_rules.py
 */

class DriverFormValidator {
    constructor(validationConfig) {
        this.config = validationConfig;
        this.form = document.getElementById('driverForm');
        
        if (!this.form) {
            console.warn('Driver form not found, validation skipped');
            return;
        }
        
        this.init();
    }
    
    init() {
        // Add real-time validation to all fields
        Object.keys(this.config).forEach(fieldName => {
            const input = document.getElementById(`id_${fieldName}`);
            if (!input) return;
            
            // Validate on blur (when user leaves field)
            input.addEventListener('blur', () => this.validateField(fieldName));
            
            // Validate on input for immediate feedback (but silent for typing)
            input.addEventListener('input', () => {
                // Only show validation after first blur
                if (input.classList.contains('was-validated')) {
                    this.validateField(fieldName, true);
                }
            });
            
            // Mark as validated after first blur
            input.addEventListener('blur', () => {
                input.classList.add('was-validated');
            }, { once: false });
        });
        
        // Validate on submit
        this.form.addEventListener('submit', (e) => {
            if (!this.validateForm()) {
                e.preventDefault();
                
                // Scroll to first error
                const firstError = this.form.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    }
    
    validateField(fieldName, silent = false) {
        const rules = this.config[fieldName];
        if (!rules) return true;
        
        const input = document.getElementById(`id_${fieldName}`);
        if (!input) return true;
        
        const value = input.value.trim();
        
        // Required check
        if (rules.required && !value) {
            return this.showError(input, rules.errors.required, silent);
        }
        
        // Skip other validations if field is empty and not required
        if (!value && !rules.required) {
            this.clearError(input);
            return true;
        }
        
        // Min length
        if (rules.minLength && value.length < rules.minLength) {
            return this.showError(input, rules.errors.min_length, silent);
        }
        
        // Max length
        if (rules.maxLength && value.length > rules.maxLength) {
            return this.showError(input, rules.errors.max_length, silent);
        }
        
        // Pattern validation
        if (rules.pattern && value) {
            const regex = new RegExp(rules.pattern);
            if (!regex.test(value)) {
                return this.showError(input, rules.errors.invalid, silent);
            }
        }
        
        // Email validation
        if (rules.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                return this.showError(input, rules.errors.invalid, silent);
            }
        }
        
        // Date validation for birth_date (min age 18)
        if (fieldName === 'birth_date' && value) {
            const birthDate = new Date(value);
            const today = new Date();
            const age = today.getFullYear() - birthDate.getFullYear();
            const monthDiff = today.getMonth() - birthDate.getMonth();
            
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }
            
            if (age < 18) {
                return this.showError(input, rules.errors.min_age, silent);
            }
            
            if (age > 100) {
                return this.showError(input, rules.errors.max_age, silent);
            }
        }
        
        // Date validation for license_expiry (must be future date)
        if (fieldName === 'license_expiry' && value) {
            const expiryDate = new Date(value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (expiryDate < today) {
                return this.showError(input, rules.errors.expired, silent);
            }
        }
        
        // Clear error if valid
        this.clearError(input);
        return true;
    }
    
    validateForm() {
        let isValid = true;
        
        Object.keys(this.config).forEach(fieldName => {
            if (!this.validateField(fieldName)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    showError(input, message, silent = false) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        
        if (!silent) {
            // Find or create feedback element
            let feedback = input.nextElementSibling;
            
            // Check if next sibling is the feedback div
            if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                // Look for feedback div after small/help text
                feedback = input.parentElement.querySelector('.invalid-feedback');
            }
            
            if (feedback && feedback.classList.contains('invalid-feedback')) {
                feedback.textContent = message;
                feedback.style.display = 'block';
            }
        }
        
        return false;
    }
    
    clearError(input) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        
        // Find feedback element
        let feedback = input.nextElementSibling;
        
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = input.parentElement.querySelector('.invalid-feedback');
        }
        
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.style.display = 'none';
        }
    }
    
    /**
     * Map backend errors to frontend fields
     * Called when form submission returns validation errors
     */
    displayBackendErrors(errors) {
        Object.entries(errors).forEach(([fieldName, messages]) => {
            const input = document.getElementById(`id_${fieldName}`);
            if (input && messages.length > 0) {
                this.showError(input, messages[0]);
            }
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const configElement = document.getElementById('validation-config');
    if (configElement) {
        try {
            const config = JSON.parse(configElement.textContent);
            window.driverValidator = new DriverFormValidator(config);
        } catch (e) {
            console.error('Failed to initialize driver validation:', e);
        }
    }
});
