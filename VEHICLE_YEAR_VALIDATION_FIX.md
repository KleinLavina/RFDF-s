# Vehicle Year Validation Fix

**Date:** January 26, 2026  
**Issue:** Year 2020 incorrectly rejected as "Invalid year. Year cannot be in the future."  
**Status:** ✅ Fixed

---

## Problem

When registering a vehicle, entering year 2020 (or any past year) was incorrectly rejected with the error message:
> ❌ Invalid year. Year cannot be in the future.

This was confusing because 2020 is clearly in the past (current year is 2026).

---

## Root Cause

The `get_vehicle_frontend_validation_config()` function in `vehicles/vehicle_validation_rules.py` was passing `maxValue: None` to the frontend JavaScript validator.

When `maxValue` is `None` (null in JavaScript), the validation logic was treating it as 0 or undefined, causing all years to fail the check.

### Code Flow:
1. **Backend validation** (forms.py) - ✅ Worked correctly
   - Checked: `year > current_year + 1` (2027)
   - 2020 would pass this check

2. **Frontend validation** (JavaScript) - ❌ Failed
   - Received: `maxValue: null`
   - JavaScript treated null as invalid
   - All years were rejected

---

## Solution

Updated `get_vehicle_frontend_validation_config()` to dynamically set `max_value` for the `year_model` field:

### Before:
```python
def get_vehicle_frontend_validation_config():
    config = {}
    for field_name, rules in VEHICLE_VALIDATION_RULES.items():
        config[field_name] = {
            'maxValue': rules.get('max_value'),  # Returns None for year_model
            # ...
        }
    return config
```

### After:
```python
def get_vehicle_frontend_validation_config():
    from django.utils import timezone
    current_year = timezone.now().year
    
    config = {}
    for field_name, rules in VEHICLE_VALIDATION_RULES.items():
        # Set max_value for year_model dynamically
        max_value = rules.get('max_value')
        if field_name == 'year_model' and max_value is None:
            max_value = current_year + 1  # 2027 for year 2026
        
        config[field_name] = {
            'maxValue': max_value,
            # ...
        }
    return config
```

---

## Valid Year Range

After the fix:
- **Minimum Year:** 1886 (first automobile)
- **Maximum Year:** 2027 (current year + 1)
- **Current Year:** 2026

### Examples:
- ✅ 1886 - Valid (first car year)
- ✅ 1990 - Valid
- ✅ 2020 - Valid (FIXED)
- ✅ 2025 - Valid
- ✅ 2026 - Valid (current year)
- ✅ 2027 - Valid (next year models)
- ❌ 2028 - Invalid (too far in future)
- ❌ 1885 - Invalid (before cars existed)

---

## Files Modified

**`vehicles/vehicle_validation_rules.py`**
- Updated `get_vehicle_frontend_validation_config()` function
- Added dynamic year calculation
- Ensures frontend and backend validation match

---

## Validation Logic

### Backend (Django Forms)
```python
def clean_year_model(self):
    year = int(self.cleaned_data.get('year_model'))
    current_year = timezone.now().year
    
    if year < 1886:
        raise ValidationError("❌ Invalid year. Vehicles didn't exist before 1886.")
    
    if year > current_year + 1:
        raise ValidationError(f"❌ Invalid year. Year cannot be more than {current_year + 1}.")
    
    return year
```

### Frontend (JavaScript)
```javascript
if (fieldName === 'year_model' && value) {
    const year = parseInt(value);
    const currentYear = new Date().getFullYear();
    
    if (year < 1886) {
        return this.showError(input, rules.errors.min_value);
    }
    
    if (year > currentYear + 1) {
        return this.showError(input, rules.errors.max_value);
    }
}
```

Both now use the same logic: `year > currentYear + 1`

---

## Testing

### Test Cases
- [x] Enter 2020 → Should be accepted ✅
- [x] Enter 2026 → Should be accepted ✅
- [x] Enter 2027 → Should be accepted ✅
- [x] Enter 2028 → Should be rejected ❌
- [x] Enter 1886 → Should be accepted ✅
- [x] Enter 1885 → Should be rejected ❌
- [x] Enter 1990 → Should be accepted ✅
- [x] Enter 2025 → Should be accepted ✅

### Validation Points
- [x] Frontend validation works
- [x] Backend validation works
- [x] Error messages are clear
- [x] Both validations match

---

## Why Allow Next Year (current_year + 1)?

Allowing `current_year + 1` (2027) is intentional because:

1. **Pre-orders** - Dealers often sell next year's models in advance
2. **Manufacturing** - Cars are manufactured before the model year
3. **Industry Standard** - Common practice in automotive registration
4. **Flexibility** - Prevents issues at year boundaries (Dec 31 → Jan 1)

Example: In December 2026, dealers are already selling 2027 models.

---

## Impact

### Before Fix
- ❌ Could not register vehicles from 2020-2026
- ❌ Confusing error message
- ❌ Frontend/backend mismatch
- ❌ Poor user experience

### After Fix
- ✅ Can register vehicles from 1886-2027
- ✅ Clear, accurate error messages
- ✅ Frontend/backend in sync
- ✅ Smooth registration process

---

## Related Validation

The year validation is part of the unified validation system:
- **Source of Truth:** `vehicles/vehicle_validation_rules.py`
- **Backend Validation:** `vehicles/forms.py` (clean_year_model)
- **Frontend Validation:** `static/js/vehicle-validation.js`
- **Real-time Feedback:** Validates on blur and input

---

## Future Considerations

### Auto-update Each Year
The validation automatically updates each year:
- 2026: Allows 1886-2027
- 2027: Will allow 1886-2028
- 2028: Will allow 1886-2029

No code changes needed annually!

### Optional Enhancements
- Add warning for very old vehicles (< 1980)
- Add info tooltip explaining year range
- Add year dropdown instead of text input
- Add "classic car" flag for pre-1980 vehicles

---

## Deployment Notes

1. File updated: `vehicles/vehicle_validation_rules.py`
2. No database changes required
3. No migration needed
4. Change takes effect immediately
5. Clear browser cache recommended

---

**Status:** ✅ Complete  
**Breaking Changes:** None  
**User Impact:** Positive - Can now register vehicles correctly
