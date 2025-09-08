import { UgandaTechConnectApp } from './main.js';

// Form enhancements for all form templates
export class FormEnhancements {
    private app: UgandaTechConnectApp;
    private forms: NodeListOf<HTMLFormElement>;
    private submitButtons: NodeListOf<HTMLButtonElement>;
    private textAreas: NodeListOf<HTMLTextAreaElement>;
    private selectElements: NodeListOf<HTMLSelectElement>;
    private inputElements: NodeListOf<HTMLInputElement>;

    constructor(app: UgandaTechConnectApp) {
        this.app = app;
        this.forms = document.querySelectorAll('form');
        this.submitButtons = document.querySelectorAll('button[type="submit"]');
        this.textAreas = document.querySelectorAll('textarea');
        this.selectElements = document.querySelectorAll('select');
        this.inputElements = document.querySelectorAll('input[type="text"], input[type="email"], input[type="number"]');
        
        this.init();
    }

    private init(): void {
        this.setupFormValidation();
        this.setupAutoSave();
        this.setupCharacterCounters();
        this.setupSmartPlaceholders();
        this.setupFieldDependencies();
        this.setupSubmitEnhancements();
        this.setupKeyboardShortcuts();
        this.setupAutoComplete();
        
        console.log('Form enhancements loaded for', this.forms.length, 'forms');
    }

    // Real-time form validation
    private setupFormValidation(): void {
        this.inputElements.forEach(input => {
            input.addEventListener('blur', (e) => {
                this.validateField(e.target as HTMLInputElement);
            });

            input.addEventListener('input', (e) => {
                this.clearFieldErrors(e.target as HTMLInputElement);
            });
        });

        this.textAreas.forEach(textarea => {
            textarea.addEventListener('blur', (e) => {
                this.validateField(e.target as HTMLTextAreaElement);
            });
        });

        this.selectElements.forEach(select => {
            select.addEventListener('change', (e) => {
                this.validateField(e.target as HTMLSelectElement);
            });
        });
    }

    // Auto-save form data to localStorage
    private setupAutoSave(): void {
        const saveForm = (formElement: HTMLFormElement) => {
            const formData = new FormData(formElement);
            const formId = formElement.id || formElement.className || 'default-form';
            const savedData: { [key: string]: string } = {};
            
            formData.forEach((value, key) => {
                savedData[key] = value.toString();
            });
            
            localStorage.setItem(`form_autosave_${formId}`, JSON.stringify(savedData));
            
            // Show auto-save indicator
            this.showAutoSaveIndicator();
        };

        this.forms.forEach(form => {
            // Load saved data on page load
            this.loadAutoSavedData(form);
            
            // Save on input changes
            form.addEventListener('input', () => {
                clearTimeout((form as any).autoSaveTimeout);
                (form as any).autoSaveTimeout = setTimeout(() => {
                    saveForm(form);
                }, 1000); // Save after 1 second of inactivity
            });
            
            // Clear saved data on successful submit
            form.addEventListener('submit', () => {
                const formId = form.id || form.className || 'default-form';
                localStorage.removeItem(`form_autosave_${formId}`);
            });
        });
    }

    // Character counters for textareas
    private setupCharacterCounters(): void {
        this.textAreas.forEach(textarea => {
            const maxLength = parseInt(textarea.getAttribute('maxlength') || '');
            if (maxLength > 0) {
                this.addCharacterCounter(textarea, maxLength);
            }
        });
    }

    // Smart placeholders that appear as hints
    private setupSmartPlaceholders(): void {
        const hints: { [key: string]: string[] } = {
            'name': ['Enter a clear, descriptive name', 'Use title case for names'],
            'description': ['Provide a detailed description', 'Include key features and benefits'],
            'focus_areas': ['Separate multiple areas with commas', 'e.g., IoT, AI, Robotics'],
            'budget': ['Enter amount in Ugandan Shillings', 'Use whole numbers without currency symbols'],
            'email': ['Enter a valid email address', 'This will be used for notifications']
        };

        this.inputElements.forEach(input => {
            const fieldName = input.name.toLowerCase();
            const matchingHints = Object.keys(hints).find(key => fieldName.includes(key));
            
            if (matchingHints) {
                this.addSmartHints(input, hints[matchingHints]);
            }
        });
    }

    // Field dependencies (show/hide based on other fields)
    private setupFieldDependencies(): void {
        // Example: Show budget-related fields only when project type is selected
        const projectTypeSelect = document.querySelector('select[name*="type"], select[name*="Type"]') as HTMLSelectElement;
        const budgetFields = document.querySelectorAll('[name*="budget"], [name*="Budget"]');
        
        if (projectTypeSelect && budgetFields.length > 0) {
            projectTypeSelect.addEventListener('change', () => {
                const showBudget = projectTypeSelect.value !== '';
                budgetFields.forEach(field => {
                    const container = field.closest('.col-md-6, .mb-3, .form-group');
                    if (container) {
                        if (showBudget) {
                            container.classList.remove('d-none');
                            (container as HTMLElement).style.display = '';
                        } else {
                            container.classList.add('d-none');
                        }
                    }
                });
            });
        }
    }

    // Enhanced submit button behavior
    private setupSubmitEnhancements(): void {
        this.forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
                if (submitBtn) {
                    this.enhanceSubmitButton(submitBtn);
                }
            });
        });
    }

    // Keyboard shortcuts
    private setupKeyboardShortcuts(): void {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + S to save form
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                const activeForm = document.querySelector('form') as HTMLFormElement;
                if (activeForm) {
                    const submitBtn = activeForm.querySelector('button[type="submit"]') as HTMLButtonElement;
                    if (submitBtn) {
                        submitBtn.click();
                    }
                }
            }
            
            // Escape to cancel/go back
            if (e.key === 'Escape') {
                const cancelBtn = document.querySelector('a[href*="list"], .btn-outline-secondary') as HTMLAnchorElement;
                if (cancelBtn) {
                    cancelBtn.click();
                }
            }
        });
    }

    // Auto-complete suggestions
    private setupAutoComplete(): void {
        const commonSuggestions: { [key: string]: string[] } = {
            'focus_areas': ['IoT', 'Artificial Intelligence', 'Machine Learning', 'Robotics', 'Blockchain', 'Renewable Energy', 'Agriculture Tech', 'Health Tech'],
            'phases': ['Research', 'Design', 'Prototyping', 'Testing', 'Validation', 'Commercialization'],
            'key_innovation': ['AI-powered', 'IoT-enabled', 'Blockchain-based', 'Machine Learning', 'Automated', 'Smart sensing']
        };

        this.inputElements.forEach(input => {
            const fieldName = input.name.toLowerCase();
            const matchingSuggestions = Object.keys(commonSuggestions).find(key => 
                fieldName.includes(key.replace('_', ''))
            );
            
            if (matchingSuggestions) {
                this.addAutoComplete(input, commonSuggestions[matchingSuggestions]);
            }
        });
    }

    // Helper methods
    private validateField(field: HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement): void {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required') || field.closest('.form-group')?.querySelector('.text-danger');
        
        if (isRequired && !value) {
            this.showFieldError(field, 'This field is required');
            return;
        }
        
        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                this.showFieldError(field, 'Please enter a valid email address');
                return;
            }
        }
        
        // Number validation
        if (field.type === 'number' && value) {
            const num = parseFloat(value);
            if (isNaN(num) || num < 0) {
                this.showFieldError(field, 'Please enter a valid positive number');
                return;
            }
        }
        
        this.clearFieldErrors(field);
    }

    private showFieldError(field: HTMLElement, message: string): void {
        this.clearFieldErrors(field);
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentNode?.appendChild(errorDiv);
    }

    private clearFieldErrors(field: HTMLElement): void {
        field.classList.remove('is-invalid');
        const existingError = field.parentNode?.querySelector('.invalid-feedback:not([data-django])');
        if (existingError) {
            existingError.remove();
        }
    }

    private addCharacterCounter(textarea: HTMLTextAreaElement, maxLength: number): void {
        const counter = document.createElement('div');
        counter.className = 'character-counter text-muted small mt-1';
        counter.textContent = `0/${maxLength} characters`;
        
        textarea.parentNode?.appendChild(counter);
        
        textarea.addEventListener('input', () => {
            const currentLength = textarea.value.length;
            counter.textContent = `${currentLength}/${maxLength} characters`;
            
            if (currentLength > maxLength * 0.9) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
            
            if (currentLength >= maxLength) {
                counter.classList.add('text-danger');
                counter.classList.remove('text-warning');
            }
        });
    }

    private addSmartHints(input: HTMLInputElement, hints: string[]): void {
        let hintIndex = 0;
        
        input.addEventListener('focus', () => {
            if (!input.value) {
                const hint = document.createElement('div');
                hint.className = 'smart-hint text-muted small mt-1';
                hint.innerHTML = `<i class="fa-solid fa-lightbulb me-1"></i>${hints[hintIndex]}`;
                
                input.parentNode?.appendChild(hint);
                
                setTimeout(() => {
                    hint.remove();
                    hintIndex = (hintIndex + 1) % hints.length;
                }, 3000);
            }
        });
    }

    private enhanceSubmitButton(button: HTMLButtonElement): void {
        const originalText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i>Processing...';
        
        // Re-enable if form submission fails
        setTimeout(() => {
            if (button.disabled) {
                button.disabled = false;
                button.innerHTML = originalText;
            }
        }, 5000);
    }

    private loadAutoSavedData(form: HTMLFormElement): void {
        const formId = form.id || form.className || 'default-form';
        const savedData = localStorage.getItem(`form_autosave_${formId}`);
        
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(fieldName => {
                    const field = form.querySelector(`[name="${fieldName}"]`) as HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement;
                    if (field && !field.value) {
                        field.value = data[fieldName];
                    }
                });
                
                this.showAutoSaveNotification();
            } catch (e) {
                console.error('Failed to load auto-saved data:', e);
            }
        }
    }

    private showAutoSaveIndicator(): void {
        const indicator = document.querySelector('.auto-save-indicator') || this.createAutoSaveIndicator();
        indicator.classList.add('show');
        
        setTimeout(() => {
            indicator.classList.remove('show');
        }, 2000);
    }

    private createAutoSaveIndicator(): HTMLElement {
        const indicator = document.createElement('div');
        indicator.className = 'auto-save-indicator position-fixed';
        indicator.style.cssText = `
            top: 20px; right: 20px; z-index: 1050;
            background: #28a745; color: white; padding: 8px 16px;
            border-radius: 20px; font-size: 12px; opacity: 0;
            transition: opacity 0.3s ease;
        `;
        indicator.innerHTML = '<i class="fa-solid fa-check me-1"></i>Auto-saved';
        document.body.appendChild(indicator);
        return indicator;
    }

    private showAutoSaveNotification(): void {
        const notification = document.createElement('div');
        notification.className = 'alert alert-info alert-dismissible fade show';
        notification.innerHTML = `
            <i class="fa-solid fa-info-circle me-2"></i>
            Previous form data has been restored.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container, .max-w-7xl');
        if (container) {
            container.insertBefore(notification, container.firstChild);
        }
    }

    private addAutoComplete(input: HTMLInputElement, suggestions: string[]): void {
        const datalist = document.createElement('datalist');
        datalist.id = `suggestions_${input.name}`;
        
        suggestions.forEach(suggestion => {
            const option = document.createElement('option');
            option.value = suggestion;
            datalist.appendChild(option);
        });
        
        document.body.appendChild(datalist);
        input.setAttribute('list', datalist.id);
    }
}

// Export for module loading
declare global {
    interface Window {
        FormEnhancements: typeof FormEnhancements;
    }
}

window.FormEnhancements = FormEnhancements;
