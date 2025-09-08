/**
 * Form Enhancement Module for Uganda Tech Connect
 * Advanced form validation, submission handling, and UX improvements
 */

import { handleApiError, handleApiSuccess } from './api';

interface ValidationRules {
    required?: boolean;
    minLength?: number;
    maxLength?: number;
    pattern?: RegExp;
    email?: boolean;
    phone?: boolean;
    url?: boolean;
}

interface FormConfig {
    submitUrl?: string;
    method?: 'GET' | 'POST' | 'PUT' | 'PATCH';
    validateOnInput?: boolean;
    showProgressBar?: boolean;
    autoSave?: boolean;
    autoSaveInterval?: number;
    confirmBeforeSubmit?: boolean;
    redirectOnSuccess?: string;
}

interface FieldConfig {
    element: HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;
    rules: ValidationRules;
    message?: string;
}

class FormEnhancer {
    private form: HTMLFormElement;
    private config: FormConfig;
    private fields: Map<string, FieldConfig> = new Map();
    private progressBar: HTMLElement | null = null;
    private autoSaveTimer: number | null = null;
    private isSubmitting: boolean = false;

    constructor(form: HTMLFormElement, config: FormConfig = {}) {
        this.form = form;
        this.config = {
            validateOnInput: true,
            showProgressBar: true,
            autoSave: false,
            autoSaveInterval: 30000, // 30 seconds
            confirmBeforeSubmit: false,
            method: 'POST',
            ...config
        };

        this.init();
    }

    private init(): void {
        this.setupFormAttributes();
        this.createProgressBar();
        this.setupEventListeners();
        this.setupFieldValidation();
        this.setupAutoSave();
        this.enhanceSelectFields();
        this.addLoadingStates();
    }

    private setupFormAttributes(): void {
        this.form.setAttribute('novalidate', 'true');
        this.form.classList.add('enhanced-form');
    }

    private createProgressBar(): void {
        if (!this.config.showProgressBar) return;

        this.progressBar = document.createElement('div');
        this.progressBar.className = 'form-progress-bar hidden';
        this.progressBar.innerHTML = `
            <div class="bg-gray-200 rounded-full h-2 mb-4">
                <div class="bg-primary-500 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
            </div>
        `;
        
        this.form.insertBefore(this.progressBar, this.form.firstChild);
    }

    private updateProgressBar(): void {
        if (!this.progressBar) return;

        const totalFields = this.form.querySelectorAll('input, select, textarea').length;
        const validFields = this.form.querySelectorAll('input.valid, select.valid, textarea.valid').length;
        const progress = totalFields > 0 ? (validFields / totalFields) * 100 : 0;

        const bar = this.progressBar.querySelector('div div') as HTMLElement;
        if (bar) {
            bar.style.width = `${progress}%`;
        }

        if (progress > 0) {
            this.progressBar.classList.remove('hidden');
        }
    }

    private setupEventListeners(): void {
        // Form submission
        this.form.addEventListener('submit', (event) => {
            event.preventDefault();
            this.handleSubmit();
        });

        // File upload handling
        const fileInputs = this.form.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', (event) => {
                this.handleFileUpload(event.target as HTMLInputElement);
            });
        });

        // Dynamic field addition
        const addFieldButtons = this.form.querySelectorAll('[data-add-field]');
        addFieldButtons.forEach(button => {
            button.addEventListener('click', (event) => {
                event.preventDefault();
                this.addDynamicField((event.target as HTMLElement).dataset.addField!);
            });
        });

        // Field removal
        this.form.addEventListener('click', (event) => {
            const target = event.target as HTMLElement;
            if (target.matches('[data-remove-field]')) {
                event.preventDefault();
                this.removeDynamicField(target);
            }
        });
    }

    private setupFieldValidation(): void {
        const fields = this.form.querySelectorAll('input, select, textarea');
        
        fields.forEach(field => {
            const fieldElement = field as HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;
            const validationData = fieldElement.dataset.validation;
            
            if (validationData) {
                try {
                    const rules = JSON.parse(validationData);
                    this.fields.set(fieldElement.name, {
                        element: fieldElement,
                        rules,
                        message: fieldElement.dataset.validationMessage
                    });
                } catch (e) {
                    console.warn('Invalid validation data:', validationData);
                }
            }

            // Real-time validation
            if (this.config.validateOnInput) {
                fieldElement.addEventListener('input', () => {
                    this.validateField(fieldElement.name);
                    this.updateProgressBar();
                });

                fieldElement.addEventListener('blur', () => {
                    this.validateField(fieldElement.name);
                });
            }
        });
    }

    private setupAutoSave(): void {
        if (!this.config.autoSave) return;

        const autoSaveUrl = this.form.dataset.autoSaveUrl;
        if (!autoSaveUrl) return;

        this.form.addEventListener('input', () => {
            if (this.autoSaveTimer) {
                window.clearTimeout(this.autoSaveTimer);
            }

            this.autoSaveTimer = window.setTimeout(() => {
                this.performAutoSave();
            }, this.config.autoSaveInterval);
        });
    }

    private async performAutoSave(): Promise<void> {
        const formData = new FormData(this.form);
        const autoSaveUrl = this.form.dataset.autoSaveUrl;

        try {
            const response = await fetch(autoSaveUrl!, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken() || ''
                }
            });

            if (response.ok) {
                this.showAutoSaveIndicator();
            }
        } catch (error) {
            console.warn('Auto-save failed:', error);
        }
    }

    private showAutoSaveIndicator(): void {
        const indicator = document.createElement('div');
        indicator.className = 'fixed top-4 right-4 bg-success-500 text-white px-3 py-1 rounded-md text-sm z-50';
        indicator.textContent = 'Auto-saved';
        document.body.appendChild(indicator);

        window.setTimeout(() => {
            indicator.remove();
        }, 2000);
    }

    private enhanceSelectFields(): void {
        const selectFields = this.form.querySelectorAll('select[data-enhance]');
        
        selectFields.forEach(select => {
            this.createCustomSelect(select as HTMLSelectElement);
        });
    }

    private createCustomSelect(select: HTMLSelectElement): void {
        const wrapper = document.createElement('div');
        wrapper.className = 'custom-select-wrapper relative';

        const customSelect = document.createElement('div');
        customSelect.className = 'custom-select bg-white border border-gray-300 rounded-lg px-3 py-2 cursor-pointer';
        
        const selectedValue = document.createElement('span');
        selectedValue.className = 'selected-value';
        selectedValue.textContent = select.options[select.selectedIndex]?.text || 'Select an option';

        const dropdown = document.createElement('div');
        dropdown.className = 'custom-dropdown hidden absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg mt-1 z-10 max-h-48 overflow-y-auto';

        // Create options
        Array.from(select.options).forEach((option, index) => {
            if (index === 0 && option.value === '') return; // Skip placeholder

            const optionElement = document.createElement('div');
            optionElement.className = 'custom-option px-3 py-2 hover:bg-gray-100 cursor-pointer';
            optionElement.textContent = option.text;
            optionElement.dataset.value = option.value;

            optionElement.addEventListener('click', () => {
                select.selectedIndex = index;
                selectedValue.textContent = option.text;
                dropdown.classList.add('hidden');
                select.dispatchEvent(new Event('change'));
            });

            dropdown.appendChild(optionElement);
        });

        customSelect.appendChild(selectedValue);
        customSelect.appendChild(dropdown);

        customSelect.addEventListener('click', () => {
            dropdown.classList.toggle('hidden');
        });

        // Hide original select
        select.style.display = 'none';

        wrapper.appendChild(customSelect);
        select.parentNode?.insertBefore(wrapper, select);
    }

    private addLoadingStates(): void {
        const submitButton = this.form.querySelector('button[type="submit"]') as HTMLButtonElement;
        if (!submitButton) return;

        // Store original content
        if (!submitButton.dataset.originalText) {
            submitButton.dataset.originalText = submitButton.innerHTML;
        }
    }

    public validateField(fieldName: string): boolean {
        const fieldConfig = this.fields.get(fieldName);
        if (!fieldConfig) return true;

        const { element, rules } = fieldConfig;
        const value = element.value.trim();

        // Clear previous validation state
        this.clearFieldValidation(element);

        let isValid = true;
        let errorMessage = '';

        // Required validation
        if (rules.required && !value) {
            isValid = false;
            errorMessage = `${fieldName} is required`;
        }

        // Length validations
        if (value && rules.minLength && value.length < rules.minLength) {
            isValid = false;
            errorMessage = `${fieldName} must be at least ${rules.minLength} characters`;
        }

        if (value && rules.maxLength && value.length > rules.maxLength) {
            isValid = false;
            errorMessage = `${fieldName} must be no more than ${rules.maxLength} characters`;
        }

        // Pattern validation
        if (value && rules.pattern && !rules.pattern.test(value)) {
            isValid = false;
            errorMessage = fieldConfig.message || `${fieldName} format is invalid`;
        }

        // Email validation
        if (value && rules.email) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
        }

        // Phone validation
        if (value && rules.phone) {
            const phonePattern = /^[\+]?[\d\s\-\(\)]{10,}$/;
            if (!phonePattern.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid phone number';
            }
        }

        // URL validation
        if (value && rules.url) {
            try {
                new URL(value);
            } catch {
                isValid = false;
                errorMessage = 'Please enter a valid URL';
            }
        }

        this.showFieldValidation(element, isValid, errorMessage);
        return isValid;
    }

    private clearFieldValidation(element: HTMLElement): void {
        element.classList.remove('valid', 'invalid', 'border-success-500', 'border-danger-500');
        const errorElement = document.getElementById(`${element.getAttribute('name')}-error`);
        errorElement?.remove();
    }

    private showFieldValidation(element: HTMLElement, isValid: boolean, message: string): void {
        if (isValid) {
            element.classList.add('valid', 'border-success-500');
            element.classList.remove('invalid', 'border-danger-500');
        } else {
            element.classList.add('invalid', 'border-danger-500');
            element.classList.remove('valid', 'border-success-500');
            
            if (message) {
                const errorElement = document.createElement('div');
                errorElement.id = `${element.getAttribute('name')}-error`;
                errorElement.className = 'text-danger-600 text-sm mt-1';
                errorElement.textContent = message;
                element.parentElement?.appendChild(errorElement);
            }
        }
    }

    private async handleSubmit(): Promise<void> {
        if (this.isSubmitting) return;

        // Validate all fields
        let isFormValid = true;
        for (const fieldName of this.fields.keys()) {
            if (!this.validateField(fieldName)) {
                isFormValid = false;
            }
        }

        if (!isFormValid) {
            this.showFormError('Please correct the errors above before submitting.');
            return;
        }

        // Confirmation dialog
        if (this.config.confirmBeforeSubmit) {
            const confirmed = confirm('Are you sure you want to submit this form?');
            if (!confirmed) return;
        }

        this.isSubmitting = true;
        this.setSubmitButtonLoading(true);

        try {
            const formData = new FormData(this.form);
            const response = await fetch(this.config.submitUrl || this.form.action, {
                method: this.config.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken() || ''
                }
            });

            const data = await response.json();

            if (response.ok) {
                handleApiSuccess({ success: true, data, message: data.message });
                
                if (this.config.redirectOnSuccess) {
                    window.setTimeout(() => {
                        window.location.href = this.config.redirectOnSuccess!;
                    }, 1500);
                }
            } else {
                throw new Error(data.error || 'Submission failed');
            }
        } catch (error) {
            handleApiError({ success: false, error: (error as Error).message });
        } finally {
            this.isSubmitting = false;
            this.setSubmitButtonLoading(false);
        }
    }

    private setSubmitButtonLoading(loading: boolean): void {
        const submitButton = this.form.querySelector('button[type="submit"]') as HTMLButtonElement;
        if (!submitButton) return;

        if (loading) {
            submitButton.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Processing...';
            submitButton.disabled = true;
        } else {
            submitButton.innerHTML = submitButton.dataset.originalText || 'Submit';
            submitButton.disabled = false;
        }
    }

    private showFormError(message: string): void {
        const existingError = this.form.querySelector('.form-error');
        existingError?.remove();

        const errorElement = document.createElement('div');
        errorElement.className = 'form-error bg-danger-50 border border-danger-200 text-danger-800 px-4 py-3 rounded-lg mb-4';
        errorElement.innerHTML = `
            <div class="flex items-center">
                <i class="fa-solid fa-exclamation-triangle text-danger-500 mr-2"></i>
                <span>${message}</span>
            </div>
        `;

        this.form.insertBefore(errorElement, this.form.firstChild);
    }

    private handleFileUpload(input: HTMLInputElement): void {
        const files = input.files;
        if (!files || files.length === 0) return;

        // Validate file types and sizes
        const allowedTypes = input.dataset.allowedTypes?.split(',') || [];
        const maxSize = parseInt(input.dataset.maxSize || '0');

        for (const file of Array.from(files)) {
            // Check file type
            if (allowedTypes.length > 0 && !allowedTypes.includes(file.type)) {
                this.showFormError(`File type ${file.type} is not allowed`);
                input.value = '';
                return;
            }

            // Check file size
            if (maxSize > 0 && file.size > maxSize) {
                this.showFormError(`File size exceeds ${maxSize} bytes`);
                input.value = '';
                return;
            }
        }

        // Show file preview for images
        if (input.dataset.showPreview === 'true') {
            this.showFilePreview(input, files[0]);
        }
    }

    private showFilePreview(input: HTMLInputElement, file: File): void {
        if (!file.type.startsWith('image/')) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            let preview = input.parentElement?.querySelector('.file-preview') as HTMLElement;
            
            if (!preview) {
                preview = document.createElement('div');
                preview.className = 'file-preview mt-2';
                input.parentElement?.appendChild(preview);
            }

            preview.innerHTML = `
                <img src="${e.target?.result}" alt="Preview" class="max-w-xs h-auto rounded-lg border">
                <button type="button" class="mt-2 text-sm text-danger-600 hover:text-danger-800" onclick="this.parentElement.remove(); this.parentElement.previousElementSibling.value=''">
                    <i class="fa-solid fa-times mr-1"></i>Remove
                </button>
            `;
        };

        reader.readAsDataURL(file);
    }

    private addDynamicField(fieldType: string): void {
        const template = document.querySelector(`template[data-field="${fieldType}"]`) as HTMLTemplateElement;
        if (!template) return;

        const clone = template.content.cloneNode(true) as DocumentFragment;
        const container = this.form.querySelector(`[data-field-container="${fieldType}"]`);
        
        if (container) {
            container.appendChild(clone);
            this.setupFieldValidation(); // Re-setup validation for new fields
        }
    }

    private removeDynamicField(button: HTMLElement): void {
        const fieldContainer = button.closest('[data-field-item]');
        fieldContainer?.remove();
    }

    private getCSRFToken(): string | null {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        
        return cookieValue || null;
    }

    // Public API methods
    public addField(fieldName: string, config: Omit<FieldConfig, 'element'>): void {
        const element = this.form.querySelector(`[name="${fieldName}"]`) as HTMLInputElement;
        if (element) {
            this.fields.set(fieldName, { ...config, element });
        }
    }

    public removeField(fieldName: string): void {
        this.fields.delete(fieldName);
    }

    public validateForm(): boolean {
        let isValid = true;
        for (const fieldName of this.fields.keys()) {
            if (!this.validateField(fieldName)) {
                isValid = false;
            }
        }
        return isValid;
    }

    public reset(): void {
        this.form.reset();
        this.fields.forEach((_, fieldName) => {
            const element = this.form.querySelector(`[name="${fieldName}"]`) as HTMLElement;
            this.clearFieldValidation(element);
        });
        this.updateProgressBar();
    }
}

// Auto-enhance forms on page load
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form[data-enhance]');
    
    forms.forEach(form => {
        const config: FormConfig = {};
        
        // Read configuration from data attributes
        const formElement = form as HTMLFormElement;
        if (formElement.dataset.submitUrl) config.submitUrl = formElement.dataset.submitUrl;
        if (formElement.dataset.method) config.method = formElement.dataset.method as any;
        if (formElement.dataset.validateOnInput) config.validateOnInput = formElement.dataset.validateOnInput === 'true';
        if (formElement.dataset.showProgressBar) config.showProgressBar = formElement.dataset.showProgressBar === 'true';
        if (formElement.dataset.autoSave) config.autoSave = formElement.dataset.autoSave === 'true';
        if (formElement.dataset.confirmBeforeSubmit) config.confirmBeforeSubmit = formElement.dataset.confirmBeforeSubmit === 'true';
        if (formElement.dataset.redirectOnSuccess) config.redirectOnSuccess = formElement.dataset.redirectOnSuccess;

        new FormEnhancer(formElement, config);
    });
});

// Export FormEnhancer class
(window as any).FormEnhancer = FormEnhancer;
