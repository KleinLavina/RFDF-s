# System & Routes Page Unification

## Overview
Successfully merged `/terminal/system-settings/` and `/terminal/manage-routes/` into a single unified page at `/terminal/system-and-routes/`.

## Changes Made

### 1. Created Unified Template
**File:** `templates/terminal/system_and_routes.html`
- Tab-based navigation with two sections: "System Settings" and "Route Management"
- Modern card-based layout with improved visual hierarchy
- Integrated both forms and functionality from original pages
- Includes confirmation modal for settings updates
- Includes edit modal for route management
- Chart.js integration for route analytics

### 2. Created Modern CSS
**File:** `static/styles/terminal/01.css`
- RDFS color palette (#112666 blue, #2563eb accent)
- Compact design with reduced padding and spacing
- Responsive grid layouts for forms and stats
- Tab navigation with smooth transitions
- Modern card shadows and rounded corners
- Mobile-responsive breakpoints

### 3. Created Unified View Function
**File:** `terminal/views/core.py`
- New function: `system_and_routes(request)`
- Combines logic from both `system_settings` and `manage_routes`
- Handles both settings form submission and route CRUD operations
- Single POST handler that routes based on action parameter
- Preserves all existing validation and error messages
- Returns combined context with form, routes, and analytics data

### 4. Updated URL Configuration
**File:** `terminal/urls.py`
- Added new route: `path('system-and-routes/', views.system_and_routes, name='system_and_routes')`
- Original routes remain intact for backward compatibility

### 5. Updated Admin Sidebar
**File:** `templates/includes/sidebar_admin.html`
- Replaced two separate links (System Settings, Routes) with single "System & Routes" link
- Points to new unified page: `{% url 'terminal:system_and_routes' %}`
- Uses gear icon for visual consistency

## Features

### System Settings Tab
- Terminal fee configuration
- Minimum deposit amount
- Entry cooldown and stay duration
- Queue display settings (countdown, refresh interval)
- Seat capacity limits (Jeepney, Van, Bus)
- Theme preference
- Confirmation modal before saving

### Route Management Tab
- Stats dashboard (Active Routes, Total Trips, Total Fees, Top Route)
- Route activity chart (Chart.js bar chart)
- Add new route form
- Routes table with edit/delete actions
- Edit route modal
- Duplicate route prevention
- Success/error toast notifications

## User Experience Improvements
1. **Single Page Access**: No need to navigate between two separate pages
2. **Tab Navigation**: Quick switching between settings and routes
3. **Visual Consistency**: Unified design language across both sections
4. **Compact Layout**: More information visible without scrolling
5. **Modern UI**: Card-based design with proper spacing and shadows
6. **Responsive**: Works on desktop and mobile devices

## Backward Compatibility
- Original `/terminal/system-settings/` and `/terminal/manage-routes/` URLs still work
- All existing functionality preserved
- No database changes required
- No breaking changes to existing code

## Testing Checklist
- [ ] Access unified page at `/terminal/system-and-routes/`
- [ ] Switch between tabs (Settings ↔ Routes)
- [ ] Update system settings and verify save
- [ ] Add new route and verify creation
- [ ] Edit existing route and verify update
- [ ] Delete route and verify removal
- [ ] Check chart renders correctly
- [ ] Verify stats display accurate data
- [ ] Test on mobile/tablet devices
- [ ] Verify toast notifications appear
- [ ] Check sidebar link works correctly

## Next Steps (Optional)
1. Consider deprecating old separate pages after testing
2. Update any documentation referencing old URLs
3. Add user training materials for new unified interface
4. Monitor user feedback and iterate on design
