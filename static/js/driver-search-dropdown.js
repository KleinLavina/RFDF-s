/**
 * Driver Search Dropdown
 * Custom searchable dropdown for driver selection with photos
 * No external dependencies - pure vanilla JavaScript
 */

class DriverSearchDropdown {
    constructor(selectElement, drivers) {
        this.selectElement = selectElement;
        this.drivers = drivers;
        this.selectedDriver = null;
        this.highlightedIndex = -1;
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        // Hide original select
        this.selectElement.style.display = 'none';
        
        // Create custom dropdown
        this.createDropdown();
        
        // Bind events
        this.bindEvents();
        
        // Set initial value if select has one
        const initialValue = this.selectElement.value;
        if (initialValue) {
            const driver = this.drivers.find(d => d.id == initialValue);
            if (driver) {
                this.selectDriver(driver, false);
            }
        }
    }
    
    createDropdown() {
        // Create wrapper
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'driver-search-wrapper';
        
        // Create display button
        this.displayButton = document.createElement('button');
        this.displayButton.type = 'button';
        this.displayButton.className = 'driver-search-display';
        this.displayButton.innerHTML = `
            <div class="driver-search-placeholder">
                <i class="fas fa-search"></i>
                <span>Search and select driver...</span>
            </div>
            <i class="fas fa-chevron-down driver-search-arrow"></i>
        `;
        
        // Create dropdown panel
        this.dropdownPanel = document.createElement('div');
        this.dropdownPanel.className = 'driver-search-dropdown';
        this.dropdownPanel.style.display = 'none';
        
        // Create search input
        this.searchInput = document.createElement('input');
        this.searchInput.type = 'text';
        this.searchInput.className = 'driver-search-input';
        this.searchInput.placeholder = 'Type to search drivers...';
        
        // Create options container
        this.optionsContainer = document.createElement('div');
        this.optionsContainer.className = 'driver-search-options';
        
        // Assemble dropdown
        this.dropdownPanel.appendChild(this.searchInput);
        this.dropdownPanel.appendChild(this.optionsContainer);
        
        this.wrapper.appendChild(this.displayButton);
        this.wrapper.appendChild(this.dropdownPanel);
        
        // Insert after select element
        this.selectElement.parentNode.insertBefore(this.wrapper, this.selectElement.nextSibling);
        
        // Render initial options
        this.renderOptions(this.drivers);
    }
    
    bindEvents() {
        // Toggle dropdown
        this.displayButton.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleDropdown();
        });
        
        // Search input
        this.searchInput.addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });
        
        // Keyboard navigation
        this.searchInput.addEventListener('keydown', (e) => {
            this.handleKeyboard(e);
        });
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.wrapper.contains(e.target)) {
                this.closeDropdown();
            }
        });
        
        // Prevent form submission on enter in search
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
            }
        });
    }
    
    toggleDropdown() {
        if (this.isOpen) {
            this.closeDropdown();
        } else {
            this.openDropdown();
        }
    }
    
    openDropdown() {
        this.isOpen = true;
        this.dropdownPanel.style.display = 'block';
        this.displayButton.classList.add('active');
        this.searchInput.focus();
        this.searchInput.value = '';
        this.renderOptions(this.drivers);
        this.highlightedIndex = -1;
    }
    
    closeDropdown() {
        this.isOpen = false;
        this.dropdownPanel.style.display = 'none';
        this.displayButton.classList.remove('active');
        this.highlightedIndex = -1;
    }
    
    handleSearch(query) {
        const filtered = this.filterDrivers(query);
        this.renderOptions(filtered);
        this.highlightedIndex = -1;
    }
    
    filterDrivers(query) {
        if (!query.trim()) {
            return this.drivers;
        }
        
        const lowerQuery = query.toLowerCase();
        return this.drivers.filter(driver => {
            const fullName = `${driver.first_name} ${driver.last_name}`.toLowerCase();
            const driverId = (driver.driver_id || '').toLowerCase();
            return fullName.includes(lowerQuery) || driverId.includes(lowerQuery);
        });
    }
    
    renderOptions(drivers) {
        this.optionsContainer.innerHTML = '';
        
        if (drivers.length === 0) {
            const emptyState = document.createElement('div');
            emptyState.className = 'driver-search-empty';
            emptyState.innerHTML = `
                <i class="fas fa-user-slash"></i>
                <p>No drivers found</p>
            `;
            this.optionsContainer.appendChild(emptyState);
            return;
        }
        
        drivers.forEach((driver, index) => {
            const option = this.createOptionElement(driver, index);
            this.optionsContainer.appendChild(option);
        });
    }
    
    createOptionElement(driver, index) {
        const option = document.createElement('div');
        option.className = 'driver-search-option';
        option.dataset.index = index;
        option.dataset.driverId = driver.id;
        
        // Photo or placeholder
        let photoHtml = '';
        if (driver.photo_url && driver.photo_url !== 'null' && driver.photo_url !== '') {
            photoHtml = `<img src="${driver.photo_url}" alt="${driver.first_name} ${driver.last_name}" class="driver-option-photo" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                         <div class="driver-option-photo-placeholder" style="display:none;"><i class="fas fa-user"></i></div>`;
        } else {
            photoHtml = `<div class="driver-option-photo-placeholder"><i class="fas fa-user"></i></div>`;
        }
        
        // Highlight matching text
        const query = this.searchInput.value;
        const fullName = `${driver.first_name} ${driver.last_name}`;
        const highlightedName = this.highlightText(fullName, query);
        const highlightedId = this.highlightText(driver.driver_id || 'N/A', query);
        
        option.innerHTML = `
            ${photoHtml}
            <div class="driver-option-info">
                <div class="driver-option-name">${highlightedName}</div>
                <div class="driver-option-id">ID: ${highlightedId}</div>
            </div>
        `;
        
        // Click handler
        option.addEventListener('click', () => {
            this.selectDriver(driver);
        });
        
        // Hover handler
        option.addEventListener('mouseenter', () => {
            this.highlightOption(index);
        });
        
        return option;
    }
    
    highlightText(text, query) {
        if (!query.trim()) {
            return text;
        }
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    selectDriver(driver, closeDropdown = true) {
        this.selectedDriver = driver;
        
        // Update hidden select
        this.selectElement.value = driver.id;
        
        // Trigger change event for validation
        const event = new Event('change', { bubbles: true });
        this.selectElement.dispatchEvent(event);
        
        // Update display
        this.updateDisplay(driver);
        
        // Close dropdown
        if (closeDropdown) {
            this.closeDropdown();
        }
    }
    
    updateDisplay(driver) {
        let photoHtml = '';
        if (driver.photo_url && driver.photo_url !== 'null' && driver.photo_url !== '') {
            photoHtml = `<img src="${driver.photo_url}" alt="${driver.first_name} ${driver.last_name}" class="driver-display-photo" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                         <div class="driver-display-photo-placeholder" style="display:none;"><i class="fas fa-user"></i></div>`;
        } else {
            photoHtml = `<div class="driver-display-photo-placeholder"><i class="fas fa-user"></i></div>`;
        }
        
        this.displayButton.innerHTML = `
            <div class="driver-search-selected">
                ${photoHtml}
                <div class="driver-display-info">
                    <div class="driver-display-name">${driver.first_name} ${driver.last_name}</div>
                    <div class="driver-display-id">ID: ${driver.driver_id || 'N/A'}</div>
                </div>
            </div>
            <i class="fas fa-chevron-down driver-search-arrow"></i>
        `;
    }
    
    handleKeyboard(e) {
        const options = this.optionsContainer.querySelectorAll('.driver-search-option');
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.highlightedIndex = Math.min(this.highlightedIndex + 1, options.length - 1);
                this.updateHighlight();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.highlightedIndex = Math.max(this.highlightedIndex - 1, 0);
                this.updateHighlight();
                break;
                
            case 'Enter':
                e.preventDefault();
                if (this.highlightedIndex >= 0 && options[this.highlightedIndex]) {
                    const driverId = options[this.highlightedIndex].dataset.driverId;
                    const driver = this.drivers.find(d => d.id == driverId);
                    if (driver) {
                        this.selectDriver(driver);
                    }
                }
                break;
                
            case 'Escape':
                e.preventDefault();
                this.closeDropdown();
                break;
        }
    }
    
    highlightOption(index) {
        this.highlightedIndex = index;
        this.updateHighlight();
    }
    
    updateHighlight() {
        const options = this.optionsContainer.querySelectorAll('.driver-search-option');
        options.forEach((option, index) => {
            if (index === this.highlightedIndex) {
                option.classList.add('highlighted');
                option.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            } else {
                option.classList.remove('highlighted');
            }
        });
    }
}

// Initialize driver search dropdown
window.initDriverSearchDropdown = function(selectId, drivers) {
    const selectElement = document.getElementById(selectId);
    if (selectElement && drivers) {
        return new DriverSearchDropdown(selectElement, drivers);
    }
};
