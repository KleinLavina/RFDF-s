# Vehicle Registration Validation & Searchable Driver Dropdown - Implementation Plan

## Overview
Implement unified validation for vehicle registration form and add a searchable driver dropdown, following the same pattern used for driver registration.

## ✅ Completed
1. **Created `vehicles/vehicle_validation_rules.py`** - Single source of truth for all vehicle validation rules

## 🔄 Implementation Steps

### Step 1: Update Django Form (`vehicles/forms.py`)
- Import validation rules from `vehicle_validation_rules.py`
- Update `VehicleRegistrationForm.__init__()` to apply validation rules
- Set required flags, placeholders, patterns, min/max lengths from single source
- Update error messages to match validation rules

### Step 2: Update View (`vehicles/views.py`)
- Import `get_vehicle_frontend_validation_config()` from vehicle_validation_rules
- Update `register_vehicle()` view to pass validation config to template
- Add driver data with photos for searchable dropdown
- Serialize config as JSON and add to context

### Step 3: Create JavaScript Validation Module
- Create `static/js/vehicle-validation.js`
- Implement `VehicleFormValidator` class for real-time validation
- Validate on blur and input events
- Check: required, min/max length, patterns, VIN format, year range
- Show/clear Bootstrap validation classes
- Prevent form submission if errors exist

### Step 4: Create Searchable Driver Dropdown
- Create `static/js/driver-search-dropdown.js`
- Implement custom searchable dropdown (no Select2 dependency)
- Features:
  - Search/filter drivers by name as user types
  - Display driver photo, name, and ID
  - Keyboard navigation (arrow keys, enter, escape)
  - Click outside to close
  - Highlight matching text
  - Show "No drivers found" message
  - Accessible (ARIA labels, roles)

### Step 5: Update Template (`templates/vehicles/register_vehicle.html`)
- Add validation config as JSON script tag
- Load validation JavaScript module
- Load driver search dropdown module
- Update all form fields to include proper `invalid-feedback` divs
- Add driver data attributes for search functionality
- Replace Select2 with custom searchable dropdown
- Use native HTML5 date input for registration expiry
- Improve form layout and styling
- Add proper ARIA labels

### Step 6: Create Enhanced CSS
- Create `static/styles/vehicles/vehicle-registration.css`
- Style form inputs, sections, buttons
- Style searchable driver dropdown
- Add validation state styling
- Ensure responsive design
- Match RDFS color palette

## Features to Implement

### Unified Validation
- ✅ Single source of truth in `vehicle_validation_rules.py`
- ✅ Backend validation uses same rules
- ✅ Frontend validation uses same rules
- ✅ Consistent error messages
- ✅ Real-time validation feedback

### Searchable Driver Dropdown
- 🔄 Custom dropdown (no external dependencies)
- 🔄 Search/filter as user types
- 🔄 Display driver photo + name + ID
- 🔄 Keyboard navigation
- 🔄 Accessible (ARIA)
- 🔄 Mobile-friendly
- 🔄 Highlight matching text

### Form Enhancements
- 🔄 Better placeholders with examples
- 🔄 Contextual help text with icons
- 🔄 Native HTML5 date input
- 🔄 Improved layout and spacing
- 🔄 Better accessibility
- 🔄 Enhanced visual feedback

## Validation Rules Summary

### Required Fields
- vehicle_type
- ownership_type
- assigned_driver
- cr_number (5-50 digits)
- or_number (5-50 digits)
- vin_number (exactly 17 chars, no I/O/Q)
- year_model (1886 to current_year + 1)
- registration_number (5-50 chars, alphanumeric + hyphens)
- registration_expiry (future date)
- license_plate (2-12 chars, alphanumeric + spaces/hyphens)

### Optional Fields
- vehicle_name (max 100 chars)
- route
- seat_capacity (1-100)

## Driver Search Dropdown Specifications

### UI Components
```
┌─────────────────────────────────────┐
│ 🔍 Search driver...                 │ ← Input field
├─────────────────────────────────────┤
│ ┌─────┐                             │
│ │ 👤  │ Juan Dela Cruz              │ ← Driver option
│ └─────┘ ID: DRV-001                 │
├─────────────────────────────────────┤
│ ┌─────┐                             │
│ │ 👤  │ Maria Santos                │
│ └─────┘ ID: DRV-002                 │
├─────────────────────────────────────┤
│ No drivers found                    │ ← Empty state
└─────────────────────────────────────┘
```

### Features
- Real-time search filtering
- Case-insensitive matching
- Match on first name, last name, or driver ID
- Highlight matching text
- Show driver photo (or placeholder icon)
- Display driver name and ID
- Keyboard navigation:
  - Arrow Up/Down: Navigate options
  - Enter: Select highlighted option
  - Escape: Close dropdown
- Click outside to close
- Mobile-friendly touch interactions

### Data Structure
```javascript
{
  id: "123",
  name: "Juan Dela Cruz",
  driver_id: "DRV-001",
  photo_url: "/media/drivers/photos/juan.jpg"
}
```

## Testing Checklist

### Validation
- [ ] All required fields show error when empty
- [ ] Min/max length validation works
- [ ] Pattern validation works (CR, OR, VIN, plate)
- [ ] VIN validation (17 chars, no I/O/Q)
- [ ] Year validation (1886 to current+1)
- [ ] Registration expiry validation (future date)
- [ ] Backend errors map to correct fields
- [ ] Toast messages still work
- [ ] Form submission prevented if invalid
- [ ] Real-time validation provides feedback

### Driver Dropdown
- [ ] Dropdown opens on click
- [ ] Search filters drivers correctly
- [ ] Case-insensitive search works
- [ ] Driver photos display correctly
- [ ] Placeholder icon shows when no photo
- [ ] Keyboard navigation works
- [ ] Enter selects highlighted option
- [ ] Escape closes dropdown
- [ ] Click outside closes dropdown
- [ ] Selected driver displays correctly
- [ ] "No drivers found" shows when appropriate
- [ ] Mobile touch interactions work

### Accessibility
- [ ] All inputs have labels
- [ ] Error messages are announced
- [ ] Keyboard navigation works
- [ ] ARIA labels present
- [ ] Focus management correct
- [ ] Screen reader friendly

### Responsive
- [ ] Form works on desktop
- [ ] Form works on tablet
- [ ] Form works on mobile
- [ ] Dropdown works on touch devices
- [ ] Date picker works on mobile

## Implementation Priority

1. **High Priority** (Core functionality)
   - Update form with validation rules
   - Create validation JavaScript
   - Update template with validation
   - Create searchable driver dropdown

2. **Medium Priority** (UX improvements)
   - Enhanced CSS styling
   - Better placeholders
   - Improved help text
   - Native date input

3. **Low Priority** (Polish)
   - Animations and transitions
   - Advanced keyboard shortcuts
   - Additional accessibility features

## Notes

- Keep existing toast notification system
- Reuse all existing error messages
- Don't break existing functionality
- Progressive enhancement (works without JS)
- Maintain accessibility standards
- Follow RDFS color palette
- No external dependencies (no Select2, no Flatpickr)
