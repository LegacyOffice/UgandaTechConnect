import { UgandaTechConnectApp } from './main.js';

// Detail view enhancements for all detail templates
export class DetailEnhancements {
    private app: UgandaTechConnectApp;
    private actionButtons: NodeListOf<HTMLButtonElement>;
    private shareButton: HTMLButtonElement | null;
    private printButton: HTMLButtonElement | null;
    private favoriteButton: HTMLButtonElement | null;
    private contentSections: NodeListOf<Element>;
    private imageGallery: NodeListOf<HTMLImageElement>;

    constructor(app: UgandaTechConnectApp) {
        this.app = app;
        this.actionButtons = document.querySelectorAll('.btn, button');
        this.shareButton = document.querySelector('[data-action="share"]') as HTMLButtonElement;
        this.printButton = document.querySelector('[data-action="print"]') as HTMLButtonElement;
        this.favoriteButton = document.querySelector('[data-action="favorite"]') as HTMLButtonElement;
        this.contentSections = document.querySelectorAll('.content-section, .card-body, .detail-section');
        this.imageGallery = document.querySelectorAll('img[src*="media"], .gallery-image');
        
        this.init();
    }

    private init(): void {
        this.setupActionEnhancements();
        this.setupContentNavigation();
        this.setupImageGallery();
        this.setupPrintStyles();
        this.setupShareFunctionality();
        this.setupFavorites();
        this.setupReadingProgress();
        this.setupKeyboardShortcuts();
        this.setupRelatedItems();
        this.setupComments();
        
        console.log('Detail view enhancements loaded');
    }

    // Enhanced action buttons
    private setupActionEnhancements(): void {
        this.actionButtons.forEach(button => {
            // Add loading states
            button.addEventListener('click', (e) => {
                if (button.type === 'submit' || button.closest('form')) {
                    this.addLoadingState(button);
                }
            });

            // Add tooltips for icon-only buttons
            if (button.querySelector('i') && !button.textContent?.trim()) {
                this.addTooltip(button);
            }
        });

        // Add confirmation for delete actions
        const deleteButtons = document.querySelectorAll('[href*="delete"], [data-action="delete"]');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.confirmDelete(button as HTMLElement);
            });
        });
    }

    // Content section navigation
    private setupContentNavigation(): void {
        if (this.contentSections.length <= 2) return;

        this.createTableOfContents();
        this.setupSmoothScrolling();
        this.setupSectionHighlighting();
    }

    // Image gallery with lightbox
    private setupImageGallery(): void {
        if (this.imageGallery.length === 0) return;

        this.imageGallery.forEach((img, index) => {
            img.style.cursor = 'pointer';
            img.addEventListener('click', () => {
                this.openLightbox(index);
            });
        });

        this.createLightboxNavigation();
    }

    // Print optimization
    private setupPrintStyles(): void {
        // Add print button if not present
        if (!this.printButton) {
            this.createPrintButton();
        }

        this.printButton?.addEventListener('click', (e) => {
            e.preventDefault();
            this.optimizeForPrint();
            window.print();
        });

        // Print-specific styles
        const printStyles = `
            @media print {
                .btn, .navbar, .footer, .sidebar { display: none !important; }
                .container { max-width: none !important; margin: 0 !important; }
                .card { border: none !important; box-shadow: none !important; }
                a[href]:after { content: " (" attr(href) ")"; }
                .page-break { page-break-before: always; }
            }
        `;
        
        const style = document.createElement('style');
        style.textContent = printStyles;
        document.head.appendChild(style);
    }

    // Share functionality
    private setupShareFunctionality(): void {
        if (!this.shareButton) {
            this.createShareButton();
        }

        this.shareButton?.addEventListener('click', (e) => {
            e.preventDefault();
            this.showShareOptions();
        });
    }

    // Favorites system
    private setupFavorites(): void {
        if (!this.favoriteButton) {
            this.createFavoriteButton();
        }

        this.favoriteButton?.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleFavorite();
        });

        this.loadFavoriteState();
    }

    // Reading progress indicator
    private setupReadingProgress(): void {
        const progressBar = this.createProgressBar();
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
            const progress = (scrolled / maxScroll) * 100;
            
            progressBar.style.width = `${Math.min(progress, 100)}%`;
        });
    }

    // Keyboard shortcuts
    private setupKeyboardShortcuts(): void {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'p':
                        e.preventDefault();
                        this.printButton?.click();
                        break;
                    case 's':
                        e.preventDefault();
                        this.shareButton?.click();
                        break;
                    case 'd':
                        e.preventDefault();
                        this.favoriteButton?.click();
                        break;
                }
            }
            
            // ESC to close modals
            if (e.key === 'Escape') {
                this.closeLightbox();
                this.closeShareModal();
            }
        });
    }

    // Related items suggestions
    private setupRelatedItems(): void {
        const relatedContainer = document.querySelector('.related-items');
        if (!relatedContainer) {
            this.createRelatedItemsSection();
        }
    }

    // Comments system
    private setupComments(): void {
        const commentsSection = document.querySelector('.comments-section');
        if (!commentsSection) {
            this.createCommentsSection();
        }
    }

    // Helper methods
    private addLoadingState(button: HTMLButtonElement): void {
        const originalText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i>Processing...';
        
        setTimeout(() => {
            button.disabled = false;
            button.innerHTML = originalText;
        }, 3000);
    }

    private addTooltip(button: HTMLButtonElement): void {
        const tooltipText = this.getTooltipText(button);
        if (tooltipText) {
            button.setAttribute('title', tooltipText);
            button.setAttribute('data-bs-toggle', 'tooltip');
        }
    }

    private getTooltipText(button: HTMLButtonElement): string {
        const iconClass = button.querySelector('i')?.className || '';
        
        if (iconClass.includes('edit')) return 'Edit';
        if (iconClass.includes('delete') || iconClass.includes('trash')) return 'Delete';
        if (iconClass.includes('share')) return 'Share';
        if (iconClass.includes('print')) return 'Print';
        if (iconClass.includes('heart') || iconClass.includes('favorite')) return 'Add to Favorites';
        if (iconClass.includes('download')) return 'Download';
        
        return '';
    }

    private confirmDelete(button: HTMLElement): void {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Confirm Delete</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to delete this item? This action cannot be undone.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger confirm-delete">Delete</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        const confirmBtn = modal.querySelector('.confirm-delete');
        confirmBtn?.addEventListener('click', () => {
            const href = button.getAttribute('href');
            if (href) {
                window.location.href = href;
            }
        });
        
        // Show modal (assuming Bootstrap is available)
        (window as any).bootstrap?.Modal?.getOrCreateInstance(modal).show();
    }

    private createTableOfContents(): void {
        const toc = document.createElement('div');
        toc.className = 'table-of-contents position-sticky';
        toc.style.cssText = 'top: 20px; max-height: 70vh; overflow-y: auto;';
        
        const tocTitle = document.createElement('h6');
        tocTitle.textContent = 'Table of Contents';
        tocTitle.className = 'border-bottom pb-2 mb-3';
        toc.appendChild(tocTitle);
        
        const tocList = document.createElement('ul');
        tocList.className = 'list-unstyled';
        
        this.contentSections.forEach((section, index) => {
            const heading = section.querySelector('h1, h2, h3, h4, h5, h6');
            if (heading) {
                const id = `section-${index}`;
                heading.id = id;
                
                const li = document.createElement('li');
                li.innerHTML = `<a href="#${id}" class="text-decoration-none">${heading.textContent}</a>`;
                tocList.appendChild(li);
            }
        });
        
        toc.appendChild(tocList);
        
        let sidebar = document.querySelector('.col-md-3, .sidebar');
        if (!sidebar) {
            const container = document.querySelector('.container');
            if (container) {
                sidebar = document.createElement('div');
                container.appendChild(sidebar);
            }
        }
        if (sidebar) {
            sidebar.appendChild(toc);
        }
    }

    private setupSmoothScrolling(): void {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector((anchor as HTMLAnchorElement).getAttribute('href') || '');
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    private setupSectionHighlighting(): void {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    document.querySelectorAll('.table-of-contents a').forEach(link => {
                        link.classList.remove('active');
                    });
                    document.querySelector(`a[href="#${id}"]`)?.classList.add('active');
                }
            });
        }, { threshold: 0.3 });

        this.contentSections.forEach(section => {
            if (section.id) {
                observer.observe(section);
            }
        });
    }

    private openLightbox(index: number): void {
        const lightbox = this.createLightboxModal();
        const img = lightbox.querySelector('.lightbox-image') as HTMLImageElement;
        const counter = lightbox.querySelector('.lightbox-counter');
        
        img.src = this.imageGallery[index].src;
        img.alt = this.imageGallery[index].alt || '';
        
        if (counter) {
            counter.textContent = `${index + 1} of ${this.imageGallery.length}`;
        }
        
        lightbox.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Store current index
        (lightbox as any).currentIndex = index;
    }

    private createLightboxModal(): HTMLElement {
        let lightbox = document.querySelector('.lightbox-modal') as HTMLElement;
        
        if (!lightbox) {
            lightbox = document.createElement('div');
            lightbox.className = 'lightbox-modal position-fixed d-flex align-items-center justify-content-center';
            lightbox.style.cssText = `
                top: 0; left: 0; width: 100%; height: 100%; 
                background: rgba(0,0,0,0.9); z-index: 2000; 
                opacity: 0; transition: opacity 0.3s;
            `;
            
            lightbox.innerHTML = `
                <div class="lightbox-content position-relative">
                    <img class="lightbox-image" style="max-width: 90vw; max-height: 90vh;">
                    <div class="lightbox-counter position-absolute text-white" style="top: 20px; right: 20px;"></div>
                    <button class="lightbox-close position-absolute btn btn-link text-white" style="top: 20px; right: 60px;">
                        <i class="fa-solid fa-times fa-2x"></i>
                    </button>
                    <button class="lightbox-prev position-absolute btn btn-link text-white" style="left: 20px; top: 50%; transform: translateY(-50%);">
                        <i class="fa-solid fa-chevron-left fa-2x"></i>
                    </button>
                    <button class="lightbox-next position-absolute btn btn-link text-white" style="right: 20px; top: 50%; transform: translateY(-50%);">
                        <i class="fa-solid fa-chevron-right fa-2x"></i>
                    </button>
                </div>
            `;
            
            document.body.appendChild(lightbox);
            
            // Event listeners
            lightbox.querySelector('.lightbox-close')?.addEventListener('click', () => this.closeLightbox());
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox) this.closeLightbox();
            });
        }
        
        return lightbox;
    }

    private createLightboxNavigation(): void {
        document.addEventListener('keydown', (e) => {
            const lightbox = document.querySelector('.lightbox-modal.show');
            if (!lightbox) return;
            
            const currentIndex = (lightbox as any).currentIndex || 0;
            
            switch (e.key) {
                case 'ArrowLeft':
                    if (currentIndex > 0) {
                        this.openLightbox(currentIndex - 1);
                    }
                    break;
                case 'ArrowRight':
                    if (currentIndex < this.imageGallery.length - 1) {
                        this.openLightbox(currentIndex + 1);
                    }
                    break;
            }
        });
    }

    private closeLightbox(): void {
        const lightbox = document.querySelector('.lightbox-modal');
        if (lightbox) {
            lightbox.classList.remove('show');
            document.body.style.overflow = '';
        }
    }

    private createPrintButton(): void {
        this.printButton = document.createElement('button');
        this.printButton.className = 'btn btn-outline-secondary';
        this.printButton.innerHTML = '<i class="fa-solid fa-print me-1"></i>Print';
        this.printButton.setAttribute('data-action', 'print');
        
        const actionContainer = document.querySelector('.d-flex.gap-3, .btn-group') || 
                               document.querySelector('.card-body');
        if (actionContainer) {
            actionContainer.appendChild(this.printButton);
        }
    }

    private optimizeForPrint(): void {
        // Hide interactive elements
        document.querySelectorAll('.btn, .navbar, .modal').forEach(el => {
            (el as HTMLElement).style.display = 'none';
        });
        
        // Expand collapsed sections
        document.querySelectorAll('.collapse:not(.show)').forEach(el => {
            el.classList.add('show');
        });
    }

    private createShareButton(): void {
        this.shareButton = document.createElement('button');
        this.shareButton.className = 'btn btn-outline-primary';
        this.shareButton.innerHTML = '<i class="fa-solid fa-share me-1"></i>Share';
        this.shareButton.setAttribute('data-action', 'share');
        
        const actionContainer = document.querySelector('.d-flex.gap-3, .btn-group') || 
                               document.querySelector('.card-body');
        if (actionContainer) {
            actionContainer.appendChild(this.shareButton);
        }
    }

    private showShareOptions(): void {
        const modal = document.createElement('div');
        modal.className = 'share-modal position-fixed d-flex align-items-center justify-content-center';
        modal.style.cssText = `
            top: 0; left: 0; width: 100%; height: 100%; 
            background: rgba(0,0,0,0.5); z-index: 1500;
        `;
        
        const url = window.location.href;
        const title = document.title;
        
        modal.innerHTML = `
            <div class="bg-white rounded p-4" style="min-width: 300px;">
                <h5 class="mb-3">Share this page</h5>
                <div class="d-grid gap-2">
                    <button class="btn btn-primary" onclick="window.open('https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}')">
                        <i class="fab fa-twitter me-2"></i>Twitter
                    </button>
                    <button class="btn btn-primary" onclick="window.open('https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}')">
                        <i class="fab fa-facebook me-2"></i>Facebook
                    </button>
                    <button class="btn btn-success copy-link">
                        <i class="fa-solid fa-copy me-2"></i>Copy Link
                    </button>
                    <button class="btn btn-secondary close-share">Close</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        modal.querySelector('.copy-link')?.addEventListener('click', () => {
            navigator.clipboard.writeText(url);
            alert('Link copied to clipboard!');
        });
        
        modal.querySelector('.close-share')?.addEventListener('click', () => {
            modal.remove();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });
    }

    private closeShareModal(): void {
        document.querySelector('.share-modal')?.remove();
    }

    private createFavoriteButton(): void {
        this.favoriteButton = document.createElement('button');
        this.favoriteButton.className = 'btn btn-outline-warning';
        this.favoriteButton.innerHTML = '<i class="fa-regular fa-heart me-1"></i>Favorite';
        this.favoriteButton.setAttribute('data-action', 'favorite');
        
        const actionContainer = document.querySelector('.d-flex.gap-3, .btn-group') || 
                               document.querySelector('.card-body');
        if (actionContainer) {
            actionContainer.appendChild(this.favoriteButton);
        }
    }

    private toggleFavorite(): void {
        const url = window.location.href;
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        const index = favorites.indexOf(url);
        
        if (index > -1) {
            favorites.splice(index, 1);
            this.favoriteButton!.innerHTML = '<i class="fa-regular fa-heart me-1"></i>Favorite';
            this.favoriteButton!.classList.remove('btn-warning');
            this.favoriteButton!.classList.add('btn-outline-warning');
        } else {
            favorites.push(url);
            this.favoriteButton!.innerHTML = '<i class="fa-solid fa-heart me-1"></i>Favorited';
            this.favoriteButton!.classList.remove('btn-outline-warning');
            this.favoriteButton!.classList.add('btn-warning');
        }
        
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }

    private loadFavoriteState(): void {
        const url = window.location.href;
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        
        if (favorites.includes(url) && this.favoriteButton) {
            this.favoriteButton.innerHTML = '<i class="fa-solid fa-heart me-1"></i>Favorited';
            this.favoriteButton.classList.remove('btn-outline-warning');
            this.favoriteButton.classList.add('btn-warning');
        }
    }

    private createProgressBar(): HTMLElement {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress position-fixed';
        progressBar.style.cssText = `
            top: 0; left: 0; height: 3px; 
            background: var(--bs-primary); 
            z-index: 1030; transition: width 0.1s;
        `;
        
        document.body.appendChild(progressBar);
        return progressBar;
    }

    private createRelatedItemsSection(): void {
        const section = document.createElement('div');
        section.className = 'related-items mt-4';
        section.innerHTML = `
            <h5 class="border-bottom pb-2 mb-3">Related Items</h5>
            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Similar Projects</h6>
                            <p class="card-text small text-muted">Discover related innovation projects</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const mainContent = document.querySelector('.container, .card-body');
        if (mainContent) {
            mainContent.appendChild(section);
        }
    }

    private createCommentsSection(): void {
        const section = document.createElement('div');
        section.className = 'comments-section mt-4 pt-4 border-top';
        section.innerHTML = `
            <h5 class="mb-3">Comments</h5>
            <div class="comment-form mb-4">
                <textarea class="form-control mb-2" placeholder="Add a comment..." rows="3"></textarea>
                <button class="btn btn-primary btn-sm">Post Comment</button>
            </div>
            <div class="comments-list">
                <p class="text-muted">No comments yet. Be the first to comment!</p>
            </div>
        `;
        
        const mainContent = document.querySelector('.container, .card-body');
        if (mainContent) {
            mainContent.appendChild(section);
        }
    }
}

// Export for module loading
declare global {
    interface Window {
        DetailEnhancements: typeof DetailEnhancements;
    }
}

window.DetailEnhancements = DetailEnhancements;
