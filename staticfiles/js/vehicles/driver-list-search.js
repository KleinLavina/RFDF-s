// =====================================================
// DRIVER LIST - AUTO-FILTERING SEARCH
// =====================================================

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('driverSearch');
  const clearBtn = document.getElementById('clearSearch');
  const tableBody = document.getElementById('driversTableBody');
  const resultsText = document.getElementById('resultsText');
  const loadingIndicator = document.getElementById('loadingIndicator');
  
  let searchTimeout;
  const DEBOUNCE_DELAY = 300; // ms

  // Show/hide clear button based on input
  function updateClearButton() {
    if (searchInput && clearBtn) {
      clearBtn.style.display = searchInput.value.trim() ? 'block' : 'none';
    }
  }

  // Clear search
  if (clearBtn) {
    clearBtn.addEventListener('click', function() {
      searchInput.value = '';
      updateClearButton();
      performSearch('');
    });
  }

  // Debounced search on input
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      updateClearButton();

      // Clear previous timeout
      clearTimeout(searchTimeout);

      // Show loading indicator
      if (loadingIndicator) {
        loadingIndicator.style.display = 'flex';
      }

      // Debounce the search
      searchTimeout = setTimeout(() => {
        performSearch(query);
      }, DEBOUNCE_DELAY);
    });

    // Initial state
    updateClearButton();
  }

  // Perform the actual search
  function performSearch(query) {
    const url = new URL(window.location.href);
    
    if (query) {
      url.searchParams.set('q', query);
    } else {
      url.searchParams.delete('q');
    }

    // Fetch filtered results
    fetch(url.toString(), {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.text())
    .then(html => {
      // Parse the response HTML
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      
      // Extract the table body
      const newTableBody = doc.getElementById('driversTableBody');
      if (newTableBody && tableBody) {
        tableBody.innerHTML = newTableBody.innerHTML;
      }

      // Update results counter
      const newResultsText = doc.getElementById('resultsText');
      if (newResultsText && resultsText) {
        resultsText.innerHTML = newResultsText.innerHTML;
      }

      // Update URL without reload
      window.history.replaceState({}, '', url.toString());

      // Hide loading indicator
      if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
      }
    })
    .catch(error => {
      console.error('Search error:', error);
      
      // Hide loading indicator
      if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
      }
    });
  }
});
