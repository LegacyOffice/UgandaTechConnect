/**
 * Uganda Tech Connect - Main TypeScript Application
 * Enhanced interactivity and type safety for the platform
 */

// Type definitions
interface AlertConfig {
    type: 'success' | 'error' | 'warning' | 'info';
    message: string;
    duration?: number;
    dismissible?: boolean;
}

interface NavigationState {
    isMobileMenuOpen: boolean;
    isSearchOpen: boolean;
    activeSection: string | null;
}

interface FormValidationRule {
    field: string;
    rules: {
        required?: boolean;
        minLength?: number;
        maxLength?: number;
        pattern?: RegExp;
        email?: boolean;
        phone?: boolean;
        url?: boolean;
    };
    message: string;
}

interface AnimationConfig {
    duration: number;
    easing: string;
    delay?: number;
}

// Main Application Class
class UgandaTechConnectApp {
    private navigationState: NavigationState;
    private alertContainer: HTMLElement | null;
    private searchInput: HTMLInputElement | null;
    private validationRules: Map<string, FormValidationRule[]>;

    constructor() {
        this.navigationState = {
            isMobileMenuOpen: false,
            isSearchOpen: false,
            activeSection: null
        };
        
        this.alertContainer = null;
        this.searchInput = null;
        this.validationRules = new Map();
        
        this.init();
    }

    private init(): void {
        document.addEventListener('DOMContentLoaded', () => {
            this.initializeComponents();
            this.setupEventListeners();
            this.initializeAnimations();
            this.setupFormValidation();
            this.initializeSearch();
            this.loadEnhancementModules();
        });
    }

    // Module loading and initialization
    private async loadEnhancementModules(): Promise<void> {
        try {
            // Detect page type and load appropriate enhancements
            const pageType = this.detectPageType();
            console.log('🎯 Detected page type:', pageType);

            // Load form enhancements if forms are present
            if (document.querySelector('form')) {
                try {
                    const formEnhancementsModule = await import('./form-enhancements.js');
                    new formEnhancementsModule.FormEnhancements(this);
                    console.log('✅ Form enhancements module loaded');
                } catch (error) {
                    console.warn('⚠️ Form enhancements module not available:', error);
                }
            }

            switch (pageType) {
                case 'home':
                    try {
                        const homeModule = await import('./home.js');
                        new homeModule.HomePage(this);
                        console.log('✅ Home page module loaded');
                    } catch (error) {
                        console.warn('⚠️ Home page module not available:', error);
                    }
                    break;

                case 'list':
                    try {
                        const listModule = await import('./list-enhancements.js');
                        new listModule.ListEnhancements(this);
                        console.log('✅ List enhancements module loaded');
                    } catch (error) {
                        console.warn('⚠️ List enhancements module not available:', error);
                    }
                    break;

                case 'detail':
                    try {
                        const detailModule = await import('./detail-enhancements.js');
                        new detailModule.DetailEnhancements(this);
                        console.log('✅ Detail enhancements module loaded');
                    } catch (error) {
                        console.warn('⚠️ Detail enhancements module not available:', error);
                    }
                    break;

                case 'form':
                    try {
                        const detailModule = await import('./detail-enhancements.js');
                        new detailModule.DetailEnhancements(this);
                        console.log('✅ Detail enhancements module loaded for form page');
                    } catch (error) {
                        console.warn('⚠️ Detail enhancements module not available for form page:', error);
                    }
                    break;
            }

            // Load API module for data operations
            try {
                const apiModule = await import('./api.js');
                // Initialize API services if available
                if ((apiModule as any).APIManager) {
                    new (apiModule as any).APIManager(this);
                }
                console.log('✅ API module loaded');
            } catch (error) {
                console.warn('⚠️ API module not available:', error);
            }

        } catch (error) {
            console.warn('⚠️ Module loading encountered errors:', error);
        }
    }

    // Detect the type of page we're on
    private detectPageType(): string {
        const path = window.location.pathname;
        const body = document.body;
        
        // Check for home page
        if (path === '/' || body.classList.contains('home-page')) {
            return 'home';
        }
        
        // Check for list pages
        if (path.includes('/list') || 
            document.querySelector('.list-item, .card-deck, .row > .col:has(.card)') ||
            document.querySelector('table tbody tr') ||
            document.querySelector('.pagination') ||
            document.querySelectorAll('.card').length > 3) {
            return 'list';
        }
        
        // Check for detail pages
        if (path.includes('/detail') || path.match(/\/\d+\/$/) ||
            document.querySelector('.detail-view, .item-detail') ||
            (!document.querySelector('form:not([role="search"])') && document.querySelector('.btn[href*="edit"]'))) {
            return 'detail';
        }
        
        // Check for form pages
        if (path.includes('/create') || path.includes('/edit') || path.includes('/form') ||
            document.querySelector('form:not([role="search"])')) {
            return 'form';
        }
        
        // Default to generic page
        return 'generic';
    }

    private initializeComponents(): void {
        // Initialize alert container
        this.alertContainer = document.getElementById('alert-container') || this.createAlertContainer();
        
        // Initialize search input
        this.searchInput = document.querySelector('input[name="q"]') as HTMLInputElement;
        
        // Set active navigation section
        this.setActiveNavigationSection();
        
        console.log('🚀 Uganda Tech Connect initialized successfully');
    }

    private createAlertContainer(): HTMLElement {
        const container = document.createElement('div');
        container.id = 'alert-container';
        container.className = 'fixed top-20 right-4 z-50 space-y-3 max-w-md';
        document.body.appendChild(container);
        return container;
    }

    private setupEventListeners(): void {
        // Mobile menu toggle
        const mobileMenuButton = document.querySelector('[data-mobile-menu-button]');
        if (mobileMenuButton) {
            mobileMenuButton.addEventListener('click', () => this.toggleMobileMenu());
        }

        // Search toggle
        const searchButton = document.querySelector('[data-search-button]');
        if (searchButton) {
            searchButton.addEventListener('click', () => this.toggleSearch());
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', (event) => this.handleOutsideClick(event));

        // Keyboard shortcuts
        document.addEventListener('keydown', (event) => this.handleKeyboardShortcuts(event));

        // Form submissions with loading states
        this.setupFormSubmissionHandlers();

        // Smooth scrolling for anchor links
        this.setupSmoothScrolling();

        // Table sorting functionality
        this.setupTableSorting();

        // Image lazy loading
        this.setupLazyLoading();
    }

    // Navigation Methods
    public toggleMobileMenu(): void {
        const mobileMenu = document.getElementById('mobile-menu');
        const icon = document.getElementById('mobile-menu-icon');
        
        if (!mobileMenu || !icon) return;

        this.navigationState.isMobileMenuOpen = !this.navigationState.isMobileMenuOpen;

        if (this.navigationState.isMobileMenuOpen) {
            this.showMobileMenu(mobileMenu, icon);
        } else {
            this.hideMobileMenu(mobileMenu, icon);
        }
    }

    private showMobileMenu(menu: HTMLElement, icon: HTMLElement): void {
        menu.classList.remove('hidden');
        menu.classList.add('animate-slideUp');
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
        
        // Accessibility
        menu.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden'; // Prevent scroll
    }

    private hideMobileMenu(menu: HTMLElement, icon: HTMLElement): void {
        menu.classList.add('hidden');
        menu.classList.remove('animate-slideUp');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
        
        // Accessibility
        menu.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = ''; // Restore scroll
    }

    public toggleSearch(): void {
        const searchBar = document.getElementById('search-bar');
        if (!searchBar) return;

        this.navigationState.isSearchOpen = !this.navigationState.isSearchOpen;

        if (this.navigationState.isSearchOpen) {
            this.showSearchBar(searchBar);
        } else {
            this.hideSearchBar(searchBar);
        }
    }

    private showSearchBar(searchBar: HTMLElement): void {
        searchBar.classList.remove('hidden');
        searchBar.classList.add('animate-slideUp');
        
        if (this.searchInput) {
            setTimeout(() => this.searchInput?.focus(), 100);
        }
    }

    private hideSearchBar(searchBar: HTMLElement): void {
        searchBar.classList.add('hidden');
        searchBar.classList.remove('animate-slideUp');
    }

    private setActiveNavigationSection(): void {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('nav a[href]');
        
        navLinks.forEach(link => {
            const href = (link as HTMLAnchorElement).getAttribute('href');
            if (href && currentPath.includes(href)) {
                link.classList.add('bg-white', 'bg-opacity-20', 'font-semibold');
                this.navigationState.activeSection = href;
            }
        });
    }

    // Alert System
    public showAlert(config: AlertConfig): void {
        const alert = this.createAlert(config);
        this.alertContainer?.appendChild(alert);

        // Auto-dismiss after duration
        if (config.duration !== 0) {
            setTimeout(() => {
                this.dismissAlert(alert);
            }, config.duration || 5000);
        }
    }

    private createAlert(config: AlertConfig): HTMLElement {
        const alert = document.createElement('div');
        const colorClasses = this.getAlertColorClasses(config.type);
        
        alert.className = `p-4 rounded-lg shadow-lg border animate-slideUp ${colorClasses}`;
        alert.innerHTML = `
            <div class="flex items-start justify-between">
                <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0">
                        <i class="fa-solid ${this.getAlertIcon(config.type)} ${this.getAlertIconColor(config.type)}"></i>
                    </div>
                    <div class="flex-1">
                        <p class="font-medium">${config.message}</p>
                    </div>
                </div>
                ${config.dismissible !== false ? `
                    <button type="button" class="flex-shrink-0 ml-3 p-1 rounded-md hover:bg-black hover:bg-opacity-5 transition-colors duration-200" onclick="this.parentElement.parentElement.remove()">
                        <i class="fa-solid fa-times text-sm opacity-60"></i>
                    </button>
                ` : ''}
            </div>
        `;

        return alert;
    }

    private getAlertColorClasses(type: string): string {
        const colorMap = {
            success: 'bg-success-50 border-success-200 text-success-800',
            error: 'bg-danger-50 border-danger-200 text-danger-800',
            warning: 'bg-warning-50 border-warning-200 text-warning-800',
            info: 'bg-info-50 border-info-200 text-info-800'
        };
        return colorMap[type as keyof typeof colorMap] || colorMap.info;
    }

    private getAlertIcon(type: string): string {
        const iconMap = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-triangle',
            warning: 'fa-exclamation-circle',
            info: 'fa-info-circle'
        };
        return iconMap[type as keyof typeof iconMap] || iconMap.info;
    }

    private getAlertIconColor(type: string): string {
        const colorMap = {
            success: 'text-success-500',
            error: 'text-danger-500',
            warning: 'text-warning-500',
            info: 'text-info-500'
        };
        return colorMap[type as keyof typeof colorMap] || colorMap.info;
    }

    private dismissAlert(alert: HTMLElement): void {
        alert.style.transform = 'translateX(100%)';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }

    // Form Validation
    private setupFormValidation(): void {
        const forms = document.querySelectorAll('form[data-validate]');
        
        forms.forEach(form => {
            const formElement = form as HTMLFormElement;
            this.addFormValidation(formElement);
        });
    }

    private addFormValidation(form: HTMLFormElement): void {
        const formId = form.id || 'default';
        const rules = this.getFormValidationRules(form);
        this.validationRules.set(formId, rules);

        form.addEventListener('submit', (event) => {
            if (!this.validateForm(form)) {
                event.preventDefault();
            }
        });

        // Real-time validation
        form.addEventListener('input', (event) => {
            const target = event.target as HTMLInputElement;
            this.validateField(target, form);
        });
    }

    private getFormValidationRules(form: HTMLFormElement): FormValidationRule[] {
        const rules: FormValidationRule[] = [];
        const fields = form.querySelectorAll('[data-validation]');

        fields.forEach(field => {
            const fieldElement = field as HTMLInputElement;
            const validationData = fieldElement.dataset.validation;
            
            if (validationData) {
                try {
                    const rule: FormValidationRule = JSON.parse(validationData);
                    rules.push(rule);
                } catch (e) {
                    console.error('Invalid validation rule:', validationData);
                }
            }
        });

        return rules;
    }

    private validateForm(form: HTMLFormElement): boolean {
        const formId = form.id || 'default';
        const rules = this.validationRules.get(formId) || [];
        let isValid = true;

        rules.forEach(rule => {
            const field = form.querySelector(`[name="${rule.field}"]`) as HTMLInputElement;
            if (field && !this.validateField(field, form)) {
                isValid = false;
            }
        });

        return isValid;
    }

    private validateField(field: HTMLInputElement, form: HTMLFormElement): boolean {
        const formId = form.id || 'default';
        const rules = this.validationRules.get(formId) || [];
        const fieldRule = rules.find(r => r.field === field.name);

        if (!fieldRule) return true;

        const value = field.value.trim();
        const { rules: validationRules } = fieldRule;
        let isValid = true;
        let errorMessage = '';

        // Required validation
        if (validationRules.required && !value) {
            isValid = false;
            errorMessage = `${fieldRule.field} is required`;
        }

        // Length validations
        if (value && validationRules.minLength && value.length < validationRules.minLength) {
            isValid = false;
            errorMessage = `${fieldRule.field} must be at least ${validationRules.minLength} characters`;
        }

        if (value && validationRules.maxLength && value.length > validationRules.maxLength) {
            isValid = false;
            errorMessage = `${fieldRule.field} must be no more than ${validationRules.maxLength} characters`;
        }

        // Pattern validation
        if (value && validationRules.pattern && !validationRules.pattern.test(value)) {
            isValid = false;
            errorMessage = fieldRule.message;
        }

        // Email validation
        if (value && validationRules.email) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
        }

        // Phone validation
        if (value && validationRules.phone) {
            const phonePattern = /^[\+]?[\d\s\-\(\)]{10,}$/;
            if (!phonePattern.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid phone number';
            }
        }

        // URL validation
        if (value && validationRules.url) {
            try {
                new URL(value);
            } catch {
                isValid = false;
                errorMessage = 'Please enter a valid URL';
            }
        }

        this.showFieldValidation(field, isValid, errorMessage);
        return isValid;
    }

    private showFieldValidation(field: HTMLInputElement, isValid: boolean, message: string): void {
        const errorElement = document.getElementById(`${field.name}-error`);
        
        if (isValid) {
            field.classList.remove('border-danger-500', 'focus:ring-danger-500');
            field.classList.add('border-success-500', 'focus:ring-success-500');
            errorElement?.remove();
        } else {
            field.classList.remove('border-success-500', 'focus:ring-success-500');
            field.classList.add('border-danger-500', 'focus:ring-danger-500');
            
            if (!errorElement) {
                const error = document.createElement('div');
                error.id = `${field.name}-error`;
                error.className = 'text-danger-600 text-sm mt-1';
                error.textContent = message;
                field.parentElement?.appendChild(error);
            }
        }
    }

    // Form Submission Handlers
    private setupFormSubmissionHandlers(): void {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (event) => {
                this.handleFormSubmission(event.target as HTMLFormElement);
            });
        });
    }

    private handleFormSubmission(form: HTMLFormElement): void {
        const submitButton = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        
        if (submitButton) {
            this.setButtonLoadingState(submitButton, true);
            
            // Reset button after timeout (fallback)
            setTimeout(() => {
                this.setButtonLoadingState(submitButton, false);
            }, 5000);
        }
    }

    private setButtonLoadingState(button: HTMLButtonElement, loading: boolean): void {
        if (loading) {
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Processing...';
            button.disabled = true;
        } else {
            button.innerHTML = button.dataset.originalText || 'Submit';
            button.disabled = false;
        }
    }

    // Search Functionality
    private initializeSearch(): void {
        if (this.searchInput) {
            this.setupSearchAutocomplete();
            this.setupSearchKeyboardNavigation();
        }
    }

    private setupSearchAutocomplete(): void {
        if (!this.searchInput) return;

        let searchTimeout: number | undefined;
        
        this.searchInput.addEventListener('input', (event) => {
            const query = (event.target as HTMLInputElement).value.trim();
            
            clearTimeout(searchTimeout);
            searchTimeout = window.setTimeout(() => {
                if (query.length >= 2) {
                    this.performSearch(query);
                }
            }, 300);
        });
    }

    private async performSearch(query: string): Promise<void> {
        try {
            const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            this.showSearchResults(results);
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    private showSearchResults(results: any[]): void {
        // Implementation for showing search results dropdown
        console.log('Search results:', results);
    }

    private setupSearchKeyboardNavigation(): void {
        if (!this.searchInput) return;

        this.searchInput.addEventListener('keydown', (event) => {
            switch (event.key) {
                case 'Escape':
                    this.hideSearchBar(document.getElementById('search-bar')!);
                    break;
                case 'Enter':
                    event.preventDefault();
                    this.performSearchSubmission();
                    break;
            }
        });
    }

    private performSearchSubmission(): void {
        if (this.searchInput && this.searchInput.value.trim()) {
            window.location.href = `/search/?q=${encodeURIComponent(this.searchInput.value.trim())}`;
        }
    }

    // Event Handlers
    private handleOutsideClick(event: Event): void {
        const target = event.target as HTMLElement;
        const mobileMenu = document.getElementById('mobile-menu');
        const searchBar = document.getElementById('search-bar');
        
        // Close mobile menu if clicking outside
        if (this.navigationState.isMobileMenuOpen && 
            !target.closest('#mobile-menu') && 
            !target.closest('[data-mobile-menu-button]')) {
            this.toggleMobileMenu();
        }
        
        // Close search if clicking outside
        if (this.navigationState.isSearchOpen && 
            !target.closest('#search-bar') && 
            !target.closest('[data-search-button]')) {
            this.toggleSearch();
        }
    }

    private handleKeyboardShortcuts(event: KeyboardEvent): void {
        // Ctrl/Cmd + K for search
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            this.toggleSearch();
        }
        
        // Escape to close modals/menus
        if (event.key === 'Escape') {
            if (this.navigationState.isMobileMenuOpen) {
                this.toggleMobileMenu();
            }
            if (this.navigationState.isSearchOpen) {
                this.toggleSearch();
            }
        }
    }

    // Animation and UI Enhancements
    private initializeAnimations(): void {
        this.setupIntersectionObserver();
        this.setupScrollAnimations();
        this.setupHoverEffects();
    }

    private setupIntersectionObserver(): void {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fadeIn');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });

        // Observe elements with animation classes
        document.querySelectorAll('[data-animate]').forEach(el => {
            observer.observe(el);
        });
    }

    private setupScrollAnimations(): void {
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    this.updateScrollAnimations();
                    ticking = false;
                });
                ticking = true;
            }
        });
    }

    private updateScrollAnimations(): void {
        const scrolled = window.pageYOffset;
        const navbar = document.querySelector('nav');
        
        if (navbar) {
            if (scrolled > 50) {
                navbar.classList.add('shadow-xl', 'backdrop-blur-md');
            } else {
                navbar.classList.remove('shadow-xl', 'backdrop-blur-md');
            }
        }
    }

    private setupHoverEffects(): void {
        // Add hover effects to interactive elements
        const interactiveElements = document.querySelectorAll('button, a, [role="button"]');
        
        interactiveElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.classList.add('transform', 'transition-transform', 'duration-200');
            });
        });
    }

    private setupSmoothScrolling(): void {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (event) => {
                event.preventDefault();
                const target = document.querySelector((anchor as HTMLAnchorElement).getAttribute('href')!);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    private setupTableSorting(): void {
        const tables = document.querySelectorAll('table[data-sortable]');
        
        tables.forEach(table => {
            const headers = table.querySelectorAll('th[data-sort]');
            headers.forEach(header => {
                (header as HTMLElement).style.cursor = 'pointer';
                header.addEventListener('click', () => {
                    this.sortTable(table as HTMLTableElement, header as HTMLElement);
                });
            });
        });
    }

    private sortTable(table: HTMLTableElement, header: HTMLElement): void {
        const column = header.dataset.sort;
        const tbody = table.querySelector('tbody');
        if (!tbody || !column) return;

        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isAscending = !header.classList.contains('sort-asc');
        
        rows.sort((a, b) => {
            const aVal = a.cells[parseInt(column)].textContent?.trim() || '';
            const bVal = b.cells[parseInt(column)].textContent?.trim() || '';
            
            if (isAscending) {
                return aVal.localeCompare(bVal, undefined, { numeric: true });
            } else {
                return bVal.localeCompare(aVal, undefined, { numeric: true });
            }
        });

        // Update DOM
        rows.forEach(row => tbody.appendChild(row));
        
        // Update header classes
        table.querySelectorAll('th').forEach(th => {
            th.classList.remove('sort-asc', 'sort-desc');
        });
        
        header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
    }

    private setupLazyLoading(): void {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target as HTMLImageElement;
                        img.src = img.dataset.src!;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        }
    }

    // Public API Methods
    public addValidationRule(formId: string, rule: FormValidationRule): void {
        const existingRules = this.validationRules.get(formId) || [];
        existingRules.push(rule);
        this.validationRules.set(formId, existingRules);
    }

    public showSuccess(message: string): void {
        this.showAlert({ type: 'success', message });
    }

    public showError(message: string): void {
        this.showAlert({ type: 'error', message });
    }

    public showWarning(message: string): void {
        this.showAlert({ type: 'warning', message });
    }

    public showInfo(message: string): void {
        this.showAlert({ type: 'info', message });
    }
}

// Initialize the application
const app = new UgandaTechConnectApp();

// Export for global access
(window as any).UgandaTechConnect = app;

// Export types and class for external use
export { UgandaTechConnectApp };
export type { AlertConfig, NavigationState, FormValidationRule, AnimationConfig };
