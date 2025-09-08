import { UgandaTechConnectApp } from './main.js';

// Home page specific functionality
export class HomePage {
    private app: UgandaTechConnectApp;
    private counters: NodeListOf<Element>;
    private statsCards: NodeListOf<Element>;
    private featureCards: NodeListOf<Element>;
    private progressBars: NodeListOf<Element>;
    private lastUpdated: HTMLElement | null;

    constructor(app: UgandaTechConnectApp) {
        this.app = app;
        this.counters = document.querySelectorAll('.counter');
        this.statsCards = document.querySelectorAll('.stat-card');
        this.featureCards = document.querySelectorAll('.feature-card');
        this.progressBars = document.querySelectorAll('.progress-bar');
        this.lastUpdated = document.getElementById('last-updated');
        
        this.init();
    }

    private init(): void {
        this.setupAnimatedCounters();
        this.setupStatsInteraction();
        this.setupFeatureFiltering();
        this.setupFeatureNavigation();
        this.setupScrollAnimations();
        this.setupRealTimeUpdates();
        
        // Initialize animations when page loads
        window.addEventListener('load', () => {
            this.startCounterAnimations();
            this.startProgressBarAnimations();
        });
    }

    private setupAnimatedCounters(): void {
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                    this.animateCounter(entry.target as HTMLElement);
                    entry.target.classList.add('animated');
                }
            });
        }, observerOptions);

        this.counters.forEach(counter => observer.observe(counter));
    }

    private animateCounter(element: HTMLElement): void {
        const target = parseInt(element.dataset.target || '0');
        const duration = parseInt(element.dataset.duration || '2000');
        const increment = target / (duration / 16); // 60 FPS
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 16);
    }

    private startProgressBarAnimations(): void {
        setTimeout(() => {
            this.progressBars.forEach(bar => {
                const progress = bar.getAttribute('data-progress') || '0';
                (bar as HTMLElement).style.width = `${progress}%`;
            });
        }, 500);
    }

    private setupStatsInteraction(): void {
        this.statsCards.forEach(card => {
            card.addEventListener('click', () => {
                const statType = card.getAttribute('data-stat');
                this.showStatDetails(statType);
            });

            // Hover effect for additional info
            card.addEventListener('mouseenter', () => {
                this.showStatTooltip(card as HTMLElement);
            });

            card.addEventListener('mouseleave', () => {
                this.hideStatTooltip();
            });
        });
    }

    private showStatDetails(statType: string | null): void {
        if (!statType) return;

        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4';
        modal.innerHTML = `
            <div class="bg-white rounded-2xl p-8 max-w-md w-full transform transition-all duration-300 scale-95">
                <div class="text-center">
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">${this.getStatTitle(statType)}</h3>
                    <p class="text-gray-600 mb-6">${this.getStatDescription(statType)}</p>
                    <button onclick="this.closest('.fixed').remove()" 
                            class="px-6 py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-colors">
                        Close
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        
        // Animate in
        setTimeout(() => {
            const content = modal.querySelector('div > div') as HTMLElement;
            content.style.transform = 'scale(1)';
        }, 100);
    }

    private getStatTitle(type: string): string {
        const titles: { [key: string]: string } = {
            programs: 'Active Programs',
            facilities: 'Partner Facilities', 
            projects: 'Innovation Projects',
            participants: 'Active Participants'
        };
        return titles[type] || 'Statistics';
    }

    private getStatDescription(type: string): string {
        const descriptions: { [key: string]: string } = {
            programs: 'Comprehensive collaboration programs driving Uganda\'s digital transformation across multiple sectors.',
            facilities: 'State-of-the-art facilities equipped with advanced technology for research and development.',
            projects: 'Innovative projects addressing real-world challenges through technology and collaboration.',
            participants: 'Diverse community of students, researchers, and industry professionals working together.'
        };
        return descriptions[type] || 'Detailed information about this metric.';
    }

    private showStatTooltip(card: HTMLElement): void {
        const tooltip = document.createElement('div');
        tooltip.className = 'absolute bg-black text-white px-3 py-2 rounded-lg text-sm z-10 tooltip';
        tooltip.textContent = 'Click for details';
        
        card.style.position = 'relative';
        card.appendChild(tooltip);
        
        // Position tooltip
        tooltip.style.bottom = '100%';
        tooltip.style.left = '50%';
        tooltip.style.transform = 'translateX(-50%)';
        tooltip.style.marginBottom = '8px';
    }

    private hideStatTooltip(): void {
        document.querySelectorAll('.tooltip').forEach(tooltip => tooltip.remove());
    }

    private setupFeatureFiltering(): void {
        const filterButtons = document.querySelectorAll('.feature-tab');
        
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Update active tab
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Filter features
                const filter = button.textContent?.toLowerCase().replace(' features', '') || 'all';
                this.filterFeatures(filter);
            });
        });
    }

    private filterFeatures(category: string): void {
        this.featureCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            const shouldShow = category === 'all' || cardCategory === category;
            
            if (shouldShow) {
                (card as HTMLElement).style.display = 'block';
                setTimeout(() => {
                    card.classList.add('animate-fadeIn');
                }, 100);
            } else {
                card.classList.remove('animate-fadeIn');
                setTimeout(() => {
                    (card as HTMLElement).style.display = 'none';
                }, 300);
            }
        });
    }

    private setupFeatureNavigation(): void {
        this.featureCards.forEach(card => {
            card.addEventListener('click', () => {
                const url = card.getAttribute('data-navigate');
                if (url) {
                    this.navigateWithAnimation(url);
                }
            });
        });
    }

    private navigateWithAnimation(url: string): void {
        // Add loading state
        const loader = document.createElement('div');
        loader.className = 'fixed inset-0 bg-white bg-opacity-90 z-50 flex items-center justify-center';
        loader.innerHTML = `
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                <p class="text-gray-600">Loading...</p>
            </div>
        `;
        
        document.body.appendChild(loader);
        
        // Simulate navigation delay for smooth transition
        setTimeout(() => {
            window.location.href = url;
        }, 500);
    }

    private setupScrollAnimations(): void {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fadeInUp');
                }
            });
        }, observerOptions);

        // Observe animated elements
        document.querySelectorAll('.feature-card, .stat-card').forEach(el => {
            observer.observe(el);
        });
    }

    private setupRealTimeUpdates(): void {
        if (this.lastUpdated) {
            this.updateTimestamp();
            
            // Update timestamp every minute
            setInterval(() => {
                this.updateTimestamp();
            }, 60000);
        }

        // Simulate live data updates (in real app, this would be WebSocket or polling)
        this.simulateLiveUpdates();
    }

    private updateTimestamp(): void {
        if (this.lastUpdated) {
            const now = new Date();
            const timeString = now.toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            this.lastUpdated.textContent = timeString;
        }
    }

    private simulateLiveUpdates(): void {
        // Simulate random small updates to counters
        setInterval(() => {
            const randomCounter = this.counters[Math.floor(Math.random() * this.counters.length)];
            const currentValue = parseInt(randomCounter.textContent?.replace(/,/g, '') || '0');
            
            // Small random change (±1)
            const change = Math.random() > 0.5 ? 1 : -1;
            const newValue = Math.max(0, currentValue + change);
            
            // Animate the change
            randomCounter.classList.add('animate-pulse');
            setTimeout(() => {
                randomCounter.textContent = newValue.toLocaleString();
                randomCounter.classList.remove('animate-pulse');
            }, 200);
        }, 30000); // Every 30 seconds
    }

    // Public methods for global access
    public startCounterAnimations(): void {
        this.counters.forEach(counter => {
            if (!counter.classList.contains('animated')) {
                this.animateCounter(counter as HTMLElement);
                counter.classList.add('animated');
            }
        });
    }

    public scrollToStats(): void {
        document.getElementById('stats-section')?.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }

    public scrollToFeatures(): void {
        document.getElementById('features')?.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Global functions for inline event handlers
declare global {
    interface Window {
        scrollToStats: () => void;
        scrollToFeatures: () => void;
        navigateWithAnimation: (url: string) => void;
        filterFeatures: (category: string) => void;
    }
}

// Initialize home page functionality
document.addEventListener('DOMContentLoaded', () => {
    const app = (window as any).ugandaTechConnect;
    if (app && document.getElementById('hero-section')) {
        const homePage = new HomePage(app);
        
        // Make methods globally accessible
        window.scrollToStats = () => homePage.scrollToStats();
        window.scrollToFeatures = () => homePage.scrollToFeatures();
        window.navigateWithAnimation = (url: string) => homePage['navigateWithAnimation'](url);
        window.filterFeatures = (category: string) => homePage['filterFeatures'](category);
    }
});
