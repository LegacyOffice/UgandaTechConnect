// List view enhancements for all list templates
export class ListEnhancements {
    constructor(app) {
        this.app = app;
        this.searchInput = document.querySelector('#search, [name="search"], .search-input');
        this.filterButtons = document.querySelectorAll('[data-filter], .filter-btn');
        this.sortButtons = document.querySelectorAll('[data-sort], .sort-btn');
        this.listItems = document.querySelectorAll('.list-item, .card, .row > .col');
        this.paginationLinks = document.querySelectorAll('.pagination a');
        this.bulkActions = document.querySelector('.bulk-actions');
        this.selectAllCheckbox = document.querySelector('#select-all');
        this.itemCheckboxes = document.querySelectorAll('input[type="checkbox"][name="selected_items"]');
        this.init();
    }
    init() {
        this.setupRealTimeSearch();
        this.setupFiltering();
        this.setupSorting();
        this.setupBulkActions();
        this.setupInfiniteScroll();
        this.setupItemAnimations();
        this.setupKeyboardNavigation();
        this.setupViewModeToggle();
        this.setupItemPreview();
        this.setupItemActions();
        console.log('List enhancements loaded for', this.listItems.length, 'items');
    }
    // Real-time search functionality
    setupRealTimeSearch() {
        if (!this.searchInput)
            return;
        let searchTimeout;
        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const query = e.target.value.toLowerCase().trim();
            searchTimeout = window.setTimeout(() => {
                this.filterItems(query);
            }, 300); // Debounce search
        });
        // Search suggestions
        this.addSearchSuggestions();
    }
    // Advanced filtering
    setupFiltering() {
        this.filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const filter = button.getAttribute('data-filter') || '';
                const isActive = button.classList.contains('active');
                // Toggle active state
                this.filterButtons.forEach(btn => btn.classList.remove('active'));
                if (!isActive) {
                    button.classList.add('active');
                    this.applyFilter(filter);
                }
                else {
                    this.clearFilters();
                }
            });
        });
        // Add filter chips for active filters
        this.createFilterChips();
    }
    // Dynamic sorting
    setupSorting() {
        this.sortButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const sortField = button.getAttribute('data-sort') || '';
                const currentDirection = button.getAttribute('data-direction') || 'asc';
                const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
                // Update button state
                this.sortButtons.forEach(btn => {
                    btn.classList.remove('active');
                    btn.removeAttribute('data-direction');
                });
                button.classList.add('active');
                button.setAttribute('data-direction', newDirection);
                this.sortItems(sortField, newDirection);
                this.updateSortIcon(button, newDirection);
            });
        });
    }
    // Bulk actions functionality
    setupBulkActions() {
        if (!this.selectAllCheckbox || !this.bulkActions)
            return;
        // Select all functionality
        this.selectAllCheckbox.addEventListener('change', (e) => {
            const isChecked = e.target.checked;
            this.itemCheckboxes.forEach(checkbox => {
                checkbox.checked = isChecked;
            });
            this.updateBulkActionsVisibility();
        });
        // Individual item selection
        this.itemCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateSelectAllState();
                this.updateBulkActionsVisibility();
            });
        });
        // Bulk action execution
        this.bulkActions.addEventListener('change', (e) => {
            const action = e.target.value;
            if (action) {
                this.executeBulkAction(action);
            }
        });
    }
    // Infinite scroll for large lists
    setupInfiniteScroll() {
        if (this.listItems.length < 20)
            return; // Only for large lists
        let loading = false;
        let page = 2; // Start from page 2
        const loadMoreItems = async () => {
            if (loading)
                return;
            loading = true;
            try {
                const response = await fetch(`${window.location.pathname}?page=${page}`);
                const text = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(text, 'text/html');
                const newItems = doc.querySelectorAll('.list-item, .card');
                if (newItems.length > 0) {
                    newItems.forEach(item => {
                        const container = document.querySelector('.list-container, .row');
                        if (container) {
                            container.appendChild(item.cloneNode(true));
                        }
                    });
                    page++;
                }
                else {
                    // No more items, remove scroll listener
                    window.removeEventListener('scroll', scrollHandler);
                }
            }
            catch (error) {
                console.error('Failed to load more items:', error);
            }
            loading = false;
        };
        const scrollHandler = () => {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
                loadMoreItems();
            }
        };
        window.addEventListener('scroll', scrollHandler);
    }
    // Item animations
    setupItemAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fadeIn');
                }
            });
        }, { threshold: 0.1 });
        this.listItems.forEach(item => {
            observer.observe(item);
        });
    }
    // Keyboard navigation
    setupKeyboardNavigation() {
        let selectedIndex = -1;
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey)
                return;
            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    selectedIndex = Math.min(selectedIndex + 1, this.listItems.length - 1);
                    this.highlightItem(selectedIndex);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    selectedIndex = Math.max(selectedIndex - 1, 0);
                    this.highlightItem(selectedIndex);
                    break;
                case 'Enter':
                    if (selectedIndex >= 0) {
                        e.preventDefault();
                        this.activateItem(selectedIndex);
                    }
                    break;
                case 'Escape':
                    selectedIndex = -1;
                    this.clearHighlight();
                    break;
            }
        });
    }
    // View mode toggle (grid/list)
    setupViewModeToggle() {
        const viewToggle = document.querySelector('.view-toggle');
        if (!viewToggle) {
            this.createViewToggle();
        }
        document.addEventListener('click', (e) => {
            const target = e.target;
            if (target.matches('[data-view]')) {
                e.preventDefault();
                const viewMode = target.getAttribute('data-view');
                this.switchViewMode(viewMode || 'grid');
            }
        });
    }
    // Item preview on hover
    setupItemPreview() {
        this.listItems.forEach(item => {
            let previewTimeout;
            item.addEventListener('mouseenter', () => {
                previewTimeout = window.setTimeout(() => {
                    this.showItemPreview(item);
                }, 1000);
            });
            item.addEventListener('mouseleave', () => {
                clearTimeout(previewTimeout);
                this.hideItemPreview();
            });
        });
    }
    // Quick item actions
    setupItemActions() {
        this.listItems.forEach(item => {
            const actionsButton = item.querySelector('.item-actions-toggle');
            if (actionsButton) {
                actionsButton.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.toggleItemActions(item);
                });
            }
            // Add quick action buttons if not present
            this.addQuickActions(item);
        });
    }
    // Helper methods
    filterItems(query) {
        this.listItems.forEach(item => {
            const text = item.textContent?.toLowerCase() || '';
            const matches = text.includes(query) || query === '';
            if (matches) {
                item.classList.remove('d-none', 'hidden');
                item.classList.add('animate-fadeIn');
            }
            else {
                item.classList.add('d-none', 'hidden');
                item.classList.remove('animate-fadeIn');
            }
        });
        this.updateResultsCount();
    }
    applyFilter(filter) {
        this.listItems.forEach(item => {
            const itemData = item.getAttribute('data-category') || item.getAttribute('data-type') || '';
            const matches = itemData.includes(filter) || filter === 'all';
            if (matches) {
                item.classList.remove('d-none', 'hidden');
            }
            else {
                item.classList.add('d-none', 'hidden');
            }
        });
        this.updateResultsCount();
    }
    clearFilters() {
        this.listItems.forEach(item => {
            item.classList.remove('d-none', 'hidden');
        });
        this.updateResultsCount();
    }
    sortItems(field, direction) {
        const container = document.querySelector('.list-container, .row');
        if (!container)
            return;
        const itemsArray = Array.from(this.listItems);
        itemsArray.sort((a, b) => {
            const aValue = this.getItemValue(a, field);
            const bValue = this.getItemValue(b, field);
            if (direction === 'asc') {
                return aValue.localeCompare(bValue);
            }
            else {
                return bValue.localeCompare(aValue);
            }
        });
        // Re-append items in sorted order
        itemsArray.forEach(item => {
            container.appendChild(item);
        });
    }
    getItemValue(item, field) {
        const value = item.getAttribute(`data-${field}`) ||
            item.querySelector(`[data-${field}]`)?.textContent ||
            item.textContent || '';
        return value.toLowerCase().trim();
    }
    updateSortIcon(button, direction) {
        const icon = button.querySelector('i');
        if (icon) {
            icon.className = direction === 'asc' ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down';
        }
    }
    updateBulkActionsVisibility() {
        const selectedCount = Array.from(this.itemCheckboxes).filter(cb => cb.checked).length;
        const bulkActionsContainer = document.querySelector('.bulk-actions-container');
        if (bulkActionsContainer) {
            if (selectedCount > 0) {
                bulkActionsContainer.classList.remove('d-none', 'hidden');
            }
            else {
                bulkActionsContainer.classList.add('d-none', 'hidden');
            }
        }
    }
    updateSelectAllState() {
        if (!this.selectAllCheckbox)
            return;
        const checkedCount = Array.from(this.itemCheckboxes).filter(cb => cb.checked).length;
        if (checkedCount === 0) {
            this.selectAllCheckbox.checked = false;
            this.selectAllCheckbox.indeterminate = false;
        }
        else if (checkedCount === this.itemCheckboxes.length) {
            this.selectAllCheckbox.checked = true;
            this.selectAllCheckbox.indeterminate = false;
        }
        else {
            this.selectAllCheckbox.checked = false;
            this.selectAllCheckbox.indeterminate = true;
        }
    }
    executeBulkAction(action) {
        const selectedItems = Array.from(this.itemCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);
        if (selectedItems.length === 0)
            return;
        switch (action) {
            case 'delete':
                this.confirmBulkDelete(selectedItems);
                break;
            case 'export':
                this.exportItems(selectedItems);
                break;
            default:
                console.log('Bulk action:', action, 'for items:', selectedItems);
        }
    }
    confirmBulkDelete(items) {
        const confirmed = confirm(`Are you sure you want to delete ${items.length} item(s)?`);
        if (confirmed) {
            // Implement bulk delete logic
            console.log('Deleting items:', items);
        }
    }
    exportItems(items) {
        // Implement export logic
        console.log('Exporting items:', items);
    }
    highlightItem(index) {
        this.clearHighlight();
        if (index >= 0 && index < this.listItems.length) {
            this.listItems[index].classList.add('keyboard-selected');
            this.listItems[index].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
    clearHighlight() {
        this.listItems.forEach(item => {
            item.classList.remove('keyboard-selected');
        });
    }
    activateItem(index) {
        if (index >= 0 && index < this.listItems.length) {
            const item = this.listItems[index];
            const link = item.querySelector('a');
            if (link) {
                link.click();
            }
        }
    }
    createViewToggle() {
        const container = document.querySelector('.d-flex.justify-content-between, .flex.justify-between');
        if (!container)
            return;
        const toggle = document.createElement('div');
        toggle.className = 'view-toggle btn-group';
        toggle.innerHTML = `
            <button type="button" class="btn btn-sm btn-outline-secondary active" data-view="grid">
                <i class="fa-solid fa-th"></i>
            </button>
            <button type="button" class="btn btn-sm btn-outline-secondary" data-view="list">
                <i class="fa-solid fa-list"></i>
            </button>
        `;
        container.appendChild(toggle);
    }
    switchViewMode(mode) {
        const container = document.querySelector('.list-container, .row');
        if (!container)
            return;
        container.classList.remove('grid-view', 'list-view');
        container.classList.add(`${mode}-view`);
        // Update toggle buttons
        document.querySelectorAll('[data-view]').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-view="${mode}"]`)?.classList.add('active');
        // Save preference
        localStorage.setItem('list_view_mode', mode);
    }
    showItemPreview(item) {
        const preview = document.createElement('div');
        preview.className = 'item-preview position-absolute bg-white shadow-lg border rounded p-3';
        preview.style.cssText = 'z-index: 1000; max-width: 300px;';
        const title = item.querySelector('h5, .card-title, .item-title')?.textContent || 'Item Preview';
        const description = item.querySelector('p, .card-text, .item-description')?.textContent || '';
        preview.innerHTML = `
            <h6 class="mb-2">${title}</h6>
            <p class="small text-muted mb-0">${description.substring(0, 100)}...</p>
        `;
        document.body.appendChild(preview);
        // Position preview
        const rect = item.getBoundingClientRect();
        preview.style.left = `${rect.right + 10}px`;
        preview.style.top = `${rect.top}px`;
    }
    hideItemPreview() {
        const preview = document.querySelector('.item-preview');
        if (preview) {
            preview.remove();
        }
    }
    toggleItemActions(item) {
        const existingActions = item.querySelector('.item-actions-menu');
        if (existingActions) {
            existingActions.remove();
            return;
        }
        const actionsMenu = document.createElement('div');
        actionsMenu.className = 'item-actions-menu position-absolute bg-white shadow border rounded';
        actionsMenu.style.cssText = 'z-index: 1000; right: 0; top: 100%;';
        actionsMenu.innerHTML = `
            <a href="#" class="dropdown-item">
                <i class="fa-solid fa-eye me-2"></i>View
            </a>
            <a href="#" class="dropdown-item">
                <i class="fa-solid fa-edit me-2"></i>Edit
            </a>
            <a href="#" class="dropdown-item text-danger">
                <i class="fa-solid fa-trash me-2"></i>Delete
            </a>
        `;
        const actionsContainer = item.querySelector('.item-actions') || item;
        if (actionsContainer) {
            actionsContainer.style.position = 'relative';
            actionsContainer.appendChild(actionsMenu);
        }
    }
    addQuickActions(item) {
        if (item.querySelector('.quick-actions'))
            return;
        const quickActions = document.createElement('div');
        quickActions.className = 'quick-actions position-absolute';
        quickActions.style.cssText = 'top: 10px; right: 10px; opacity: 0; transition: opacity 0.2s;';
        quickActions.innerHTML = `
            <button class="btn btn-sm btn-outline-primary me-1" title="Quick Edit">
                <i class="fa-solid fa-edit"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger" title="Delete">
                <i class="fa-solid fa-trash"></i>
            </button>
        `;
        item.style.position = 'relative';
        item.appendChild(quickActions);
        // Show/hide on hover
        item.addEventListener('mouseenter', () => {
            quickActions.style.opacity = '1';
        });
        item.addEventListener('mouseleave', () => {
            quickActions.style.opacity = '0';
        });
    }
    addSearchSuggestions() {
        if (!this.searchInput)
            return;
        const suggestions = this.extractSearchSuggestions();
        const datalist = document.createElement('datalist');
        datalist.id = 'search-suggestions';
        suggestions.forEach(suggestion => {
            const option = document.createElement('option');
            option.value = suggestion;
            datalist.appendChild(option);
        });
        document.body.appendChild(datalist);
        this.searchInput.setAttribute('list', 'search-suggestions');
    }
    extractSearchSuggestions() {
        const suggestions = new Set();
        this.listItems.forEach(item => {
            const title = item.querySelector('h5, .card-title, .item-title')?.textContent?.trim();
            if (title) {
                suggestions.add(title);
                // Add individual words
                title.split(' ').forEach(word => {
                    if (word.length > 3) {
                        suggestions.add(word);
                    }
                });
            }
        });
        return Array.from(suggestions).slice(0, 20); // Limit suggestions
    }
    createFilterChips() {
        const activeFilters = Array.from(this.filterButtons)
            .filter(btn => btn.classList.contains('active'))
            .map(btn => btn.textContent?.trim() || '');
        const chipsContainer = document.querySelector('.filter-chips') || this.createChipsContainer();
        chipsContainer.innerHTML = '';
        activeFilters.forEach(filter => {
            const chip = document.createElement('span');
            chip.className = 'badge bg-primary me-2';
            chip.innerHTML = `
                ${filter}
                <button type="button" class="btn-close btn-close-white ms-1" style="font-size: 0.7em;"></button>
            `;
            chip.querySelector('.btn-close')?.addEventListener('click', () => {
                const filterBtn = Array.from(this.filterButtons)
                    .find(btn => btn.textContent?.trim() === filter);
                if (filterBtn) {
                    filterBtn.classList.remove('active');
                    this.clearFilters();
                }
                chip.remove();
            });
            chipsContainer.appendChild(chip);
        });
    }
    createChipsContainer() {
        const container = document.createElement('div');
        container.className = 'filter-chips mb-3';
        const searchContainer = this.searchInput?.parentElement || document.querySelector('.search-container');
        if (searchContainer) {
            searchContainer.appendChild(container);
        }
        return container;
    }
    updateResultsCount() {
        const visibleCount = Array.from(this.listItems).filter(item => !item.classList.contains('d-none') && !item.classList.contains('hidden')).length;
        let counter = document.querySelector('.results-count');
        if (!counter) {
            counter = document.createElement('div');
            counter.className = 'results-count text-muted small mb-3';
            const container = document.querySelector('.list-container, .row')?.parentElement;
            if (container) {
                container.insertBefore(counter, container.firstChild);
            }
        }
        counter.textContent = `Showing ${visibleCount} of ${this.listItems.length} items`;
    }
}
window.ListEnhancements = ListEnhancements;
