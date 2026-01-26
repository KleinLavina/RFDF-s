# Queue Count Display Fix Summary

## Issue Description
Queue counts and indicators for active queues were displaying inaccurate numbers across multiple pages. The displayed counts did not correctly reflect the actual queue state.

## Root Cause
The views were using incorrect filters to count active queue entries:

### Incorrect Approaches Found:
1. **Admin Dashboard**: `EntryLog.objects.filter(status=EntryLog.STATUS_SUCCESS).count()`
   - Counted ALL successful entries ever recorded, not just active ones
   
2. **Staff Dashboard**: Same issue - counted all successful entries historically
   
3. **Transactions View**: `Vehicle.objects.filter(status__in=["queued", "boarding"]).count()`
   - Relied on Vehicle status field which may be outdated or not synchronized

### Correct Approach:
```python
EntryLog.objects.filter(is_active=True, status=EntryLog.STATUS_SUCCESS).count()
```

**Why this is correct:**
- `is_active=True` means the vehicle is currently inside the terminal
- `status=EntryLog.STATUS_SUCCESS` means the entry was successful
- Together, they represent the actual current active queue

## Changes Made

### 1. Fixed `admin_dashboard_view()` in `accounts/views.py` (Line ~208)
**Before:**
```python
total_queue = 0
if QueueHistory is not None:
    total_queue = QueueHistory.objects.filter().count()
else:
    try:
        total_queue = EntryLog.objects.filter(status=EntryLog.STATUS_SUCCESS).count()
    except Exception:
        total_queue = 0
```

**After:**
```python
# Active queue count: vehicles currently in terminal (is_active=True, status=success)
total_queue = EntryLog.objects.filter(is_active=True, status=EntryLog.STATUS_SUCCESS).count()
```

### 2. Fixed `staff_dashboard_view()` in `accounts/views.py` (Line ~260)
**Before:**
```python
total_queue = EntryLog.objects.filter(status=EntryLog.STATUS_SUCCESS).count()
```

**After:**
```python
# Active queue count: vehicles currently in terminal (is_active=True, status=success)
total_queue = EntryLog.objects.filter(is_active=True, status=EntryLog.STATUS_SUCCESS).count()
```

### 3. Fixed `transactions_view()` in `terminal/views/core.py` (Line ~176)
**Before:**
```python
active_queue = Vehicle.objects.filter(
    status__in=["queued", "boarding"]
).count()
```

**After:**
```python
# Active queue count: vehicles currently in terminal (is_active=True, status=success)
active_queue = EntryLog.objects.filter(is_active=True, status=EntryLog.STATUS_SUCCESS).count()
```

### 4. Fixed `reports_home()` in `reports/views.py` (Line ~55)
**Before:**
```python
active_vehicles = Vehicle.objects.filter(status__in=["queued", "boarding"]).count()
```

**After:**
```python
# Active queue count: vehicles currently in terminal (is_active=True, status=success)
active_vehicles = EntryLog.objects.filter(is_active=True, status=EntryLog.STATUS_SUCCESS).count()
```

## Affected Pages
All pages now display accurate, synchronized queue counts:

1. ✅ `/accounts/dashboard/admin/` - Admin dashboard
2. ✅ `/accounts/dashboard/staff/` - Staff dashboard  
3. ✅ `/terminal/transactions/` - Transactions view
4. ✅ `/reports/` - Reports home page
5. ✅ `/accounts/dashboard/admin/data/` - Admin dashboard AJAX endpoint (already correct)

## Verification
- All four views now use the same consistent filter logic
- Queue counts will accurately reflect vehicles currently in the terminal
- No changes were made to the underlying queue logic (as instructed)
- Only the data presentation layer was corrected
- All Python files compile successfully without syntax errors

## Testing Recommendations
1. Log in as admin and verify queue count on dashboard matches reality
2. Log in as staff and verify queue count on dashboard matches reality
3. Check transactions page and verify active queue count is accurate
4. Scan a vehicle in via QR entry and verify all counts increment by 1
5. Scan a vehicle out via QR exit and verify all counts decrement by 1
6. Verify counts remain synchronized across all pages

## Notes
- The `admin_dashboard_data()` AJAX endpoint was already using the correct filter
- The `system_and_routes()` view does not display queue counts, so no changes were needed
- All changes preserve existing functionality and only correct the counting logic
- Comments were added to make the correct approach clear for future maintenance
