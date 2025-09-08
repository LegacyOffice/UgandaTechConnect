// Home page specific functionality
export class HomePage {
    constructor(app) {
        this.app = app;
        this.counters = document.querySelectorAll('.counter');
        this.statsCards = document.querySelectorAll('.stat-card');
        this.featureCards = document.querySelectorAll('.feature-card');
        this.progressBars = document.querySelectorAll('.progress-bar');
        this.lastUpdated = document.getElementById('last-updated');
        this.init();
    }
    init() {
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
    setupAnimatedCounters() {
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px'
        };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                    this.animateCounter(entry.target);
                    entry.target.classList.add('animated');
                }
            });
        }, observerOptions);
        this.counters.forEach(counter => observer.observe(counter));
    }
    animateCounter(element) {
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
    startProgressBarAnimations() {
        setTimeout(() => {
            this.progressBars.forEach(bar => {
                const progress = bar.getAttribute('data-progress') || '0';
                bar.style.width = `${progress}%`;
            });
        }, 500);
    }
    setupStatsInteraction() {
        this.statsCards.forEach(card => {
            card.addEventListener('click', () => {
                const statType = card.getAttribute('data-stat');
                this.showStatDetails(statType);
            });
            // Hover effect for additional info
            card.addEventListener('mouseenter', () => {
                this.showStatTooltip(card);
            });
            card.addEventListener('mouseleave', () => {
                this.hideStatTooltip();
            });
        });
    }
    showStatDetails(statType) {
        if (!statType)
            return;
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
            const content = modal.querySelector('div > div');
            content.style.transform = 'scale(1)';
        }, 100);
    }
    getStatTitle(type) {
        const titles = {
            programs: 'Active Programs',
            facilities: 'Partner Facilities',
            projects: 'Innovation Projects',
            participants: 'Active Participants'
        };
        return titles[type] || 'Statistics';
    }
    getStatDescription(type) {
        const descriptions = {
            programs: 'Comprehensive collaboration programs driving Uganda\'s digital transformation across multiple sectors.',
            facilities: 'State-of-the-art facilities equipped with advanced technology for research and development.',
            projects: 'Innovative projects addressing real-world challenges through technology and collaboration.',
            participants: 'Diverse community of students, researchers, and industry professionals working together.'
        };
        return descriptions[type] || 'Detailed information about this metric.';
    }
    showStatTooltip(card) {
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
    hideStatTooltip() {
        document.querySelectorAll('.tooltip').forEach(tooltip => tooltip.remove());
    }
    setupFeatureFiltering() {
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
    filterFeatures(category) {
        this.featureCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            const shouldShow = category === 'all' || cardCategory === category;
            if (shouldShow) {
                card.style.display = 'block';
                setTimeout(() => {
                    card.classList.add('animate-fadeIn');
                }, 100);
            }
            else {
                card.classList.remove('animate-fadeIn');
                setTimeout(() => {
                    card.style.display = 'none';
                }, 300);
            }
        });
    }
    setupFeatureNavigation() {
        this.featureCards.forEach(card => {
            card.addEventListener('click', () => {
                const url = card.getAttribute('data-navigate');
                if (url) {
                    this.navigateWithAnimation(url);
                }
            });
        });
    }
    navigateWithAnimation(url) {
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
    setupScrollAnimations() {
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
    setupRealTimeUpdates() {
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
    updateTimestamp() {
        if (this.lastUpdated) {
            const now = new Date();
            const timeString = now.toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit'
            });
            this.lastUpdated.textContent = timeString;
        }
    }
    simulateLiveUpdates() {
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
    startCounterAnimations() {
        this.counters.forEach(counter => {
            if (!counter.classList.contains('animated')) {
                this.animateCounter(counter);
                counter.classList.add('animated');
            }
        });
    }
    scrollToStats() {
        document.getElementById('stats-section')?.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
    scrollToFeatures() {
        document.getElementById('features')?.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}
// Initialize home page functionality
document.addEventListener('DOMContentLoaded', () => {
    const app = window.ugandaTechConnect;
    if (app && document.getElementById('hero-section')) {
        const homePage = new HomePage(app);
        // Make methods globally accessible
        window.scrollToStats = () => homePage.scrollToStats();
        window.scrollToFeatures = () => homePage.scrollToFeatures();
        window.navigateWithAnimation = (url) => homePage['navigateWithAnimation'](url);
        window.filterFeatures = (category) => homePage['filterFeatures'](category);
    }
});
