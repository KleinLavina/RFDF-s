# List Pages - Real-Time Filtering & Sorting Enhancement

## Overview
Enhanced both `/vehicles/registered/` and `/vehicles/registered-drivers/` pages with real-time filtering and sorting controls that apply automatically without manual submission.

## Features Implemented

### 1. Sorting Options (Both Pages)

#### Vehicle List (`/vehicles/registered/`)
- **Newest First** (default) - Recently registered vehicles first
- **Oldest First** - Oldest registered vehicles first
- **Name (A → Z)** - Alphabetical by vehicle name
- **Name (Z → A)** - Reverse alphabetical by vehicle name
- **Near Expiry** - Vehicles expiring soon or expired (within 30 days)
- **Already Expired** - Only expired vehicles first
- **Longest Time Remaining** - Vehicles with most time before expiry
- **Shortest Time Remaining** - Vehicles with least time before expiry

#### Driver List (`/vehicles/registered-drivers/`)
- **Name (A → Z)** (default) - Alphabetical by first name, then last name
- **Name (Z → A)** - Reverse alphabetical
- **Newest First** - Recently registered drivers first
- **Oldest First** - Oldest registered drivers first
- **Near Expiry** - Licenses expiring soon or expired (within 30 days)
- **Already Expired** - Only expired licenses first
- **Longest Time Remaining** - Licenses with most time before expiry
- **Shortest Time Remaining** - Licenses with least time before expiry

### 2. Real-Time Behavior
- **Auto-Apply**: All filters and sorting apply immediately on change
- **No Submit Button**: Changes take effect without manual submission
- **Combined Filters**: Search query + sorting work together
- **URL Persistence**: Filter state saved in URL for bookmarking/sharing
- **Debounced Search**: 300ms delay prevents excessive requests while typing

### 3. UI Components

#### Filter Controls
- Dropdown select for sorting options
- Icon indicators for visual clarity
- Consistent styling with RDFS color palette
- Hover effects for better UX

#### Loading States
- Loading indicator during fetch operations
- Smooth transitions between states
- Non-blocking UI updates

## Technical Implementation

### Frontend (JavaScript)

#### Vehicle List (`vehicle-list-search.js`)
```javascript
- Added sortSelect element handling
- Combined search + sort parameters in URL
- Restored sort state from URL on page load
- Real-time fetch on sort change
```

#### Driver List (`driver-list-search.js`)
```javascript
- Added sortSelect element handling
- Combined search + sort parameters in URL
- Restored sort state from URL on page load
- Real-time fetch on sort change
```

### Backend (Python)

#### Vehicle View (`registered_vehicles`)
```python
- Added sort_by parameter handling
- Implemented 8 sorting algorithms:
  * newest/oldest: By date_registered
  * name-asc/desc: By vehicle_name
  * expiry-near: Prioritizes expired + near expiry (≤30 days)
  * expiry-expired: Only expired first
  * expiry-longest: Most days remaining first
  * expiry-shortest: Least days remaining first
- Custom sorting on annotated expiry data
- Handles null expiry dates gracefully
```

#### Driver View (`registered_drivers`)
```python
- Added sort_by parameter handling
- Implemented 8 sorting algorithms:
  * name-asc/desc: By first_name + last_name
  * newest/oldest: By driver ID
  * expiry-near: Prioritizes expired + near expiry (≤30 days)
  * expiry-expired: Only expired first
  * expiry-longest: Most days remaining first
  * expiry-shortest: Least days remaining first
- Custom sorting on annotated expiry data
- Handles null expiry dates gracefully
```

### Styling (CSS)

#### Filter Controls Styles
```css
- .filter-controls: Flex container for filter groups
- .filter-group: Individual filter with label + select
- .filter-select: Custom styled dropdown with:
  * RDFS color scheme
  * Custom arrow icon
  * Hover and focus states
  * Consistent sizing (min-width: 200px)
```

## Sorting Logic Details

### Expiry-Based Sorting Priority

#### Near Expiry Sort
1. **Priority 0**: Expired or expiring ≤30 days (sorted by days remaining)
2. **Priority 1**: Not near expiry (>30 days)
3. **Priority 2**: No expiry date

#### Expired Sort
1. **Priority 0**: Already expired (sorted by how long expired)
2. **Priority 1**: Not expired
3. **Priority 2**: No expiry date

#### Longest/Shortest Time Remaining
- Sorts by days_remaining value
- Null expiry dates always last (-999999 or 999999 sentinel)
- Negative days (expired) included in calculation

## Files Modified

### Templates
- `templates/vehicles/registered_vehicles.html`
  - Added filter controls section
  - Added sortBy dropdown
  - Updated search hint text

- `templates/vehicles/registered_drivers.html`
  - Added filter controls section
  - Added sortBy dropdown
  - Updated search hint text

### JavaScript
- `static/js/vehicles/vehicle-list-search.js`
  - Added sort handling
  - Combined search + sort in URL
  - Restored sort state from URL

- `static/js/vehicles/driver-list-search.js`
  - Added sort handling
  - Combined search + sort in URL
  - Restored sort state from URL

### CSS
- `static/styles/vehicles/vehicle-list.css`
  - Added .filter-controls styles
  - Added .filter-group styles
  - Added .filter-select styles

- `static/styles/vehicles/driver-list.css`
  - Added .filter-controls styles
  - Added .filter-group styles
  - Added .filter-select styles

### Backend
- `vehicles/views.py`
  - Updated `registered_vehicles()` view
  - Updated `registered_drivers()` view
  - Added sorting logic for all 8 options

## User Experience

### Workflow
1. User opens vehicle or driver list page
2. User can immediately search using text input
3. User can select sorting option from dropdown
4. Results update automatically (no button click needed)
5. URL updates to reflect current filters
6. User can bookmark/share filtered view
7. Returning to page restores previous sort selection

### Performance
- Debounced search (300ms) reduces server load
- Loading indicator provides feedback
- AJAX requests prevent full page reloads
- Efficient queryset filtering before sorting

## Testing Checklist

### Vehicle List
- [x] Search by vehicle name
- [x] Search by plate number
- [x] Search by VIN
- [x] Search by driver name
- [x] Sort by newest first
- [x] Sort by oldest first
- [x] Sort by name A→Z
- [x] Sort by name Z→A
- [x] Sort by near expiry
- [x] Sort by expired only
- [x] Sort by longest time remaining
- [x] Sort by shortest time remaining
- [x] Combined search + sort
- [x] URL persistence
- [x] Loading indicator

### Driver List
- [x] Search by driver name
- [x] Search by license number
- [x] Search by contact info
- [x] Sort by name A→Z (default)
- [x] Sort by name Z→A
- [x] Sort by newest first
- [x] Sort by oldest first
- [x] Sort by near expiry
- [x] Sort by expired only
- [x] Sort by longest time remaining
- [x] Sort by shortest time remaining
- [x] Combined search + sort
- [x] URL persistence
- [x] Loading indicator

## Edge Cases Handled

1. **Null Expiry Dates**: Always sorted last regardless of sort direction
2. **Expired Items**: Included in expiry-based sorts with negative days
3. **Empty Results**: Proper empty state display
4. **URL State**: Sort parameter preserved in URL
5. **Default Values**: Sensible defaults (newest for vehicles, name-asc for drivers)
6. **Multiple Filters**: Search + sort work together seamlessly

## Future Enhancements (Optional)

- Add filter by vehicle type (jeepney/van/bus)
- Add filter by expiry status (expired/near/valid)
- Add date range filter for registration date
- Add export filtered results to CSV
- Add saved filter presets
- Add filter reset button
