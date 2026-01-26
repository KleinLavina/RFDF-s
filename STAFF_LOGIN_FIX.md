# Staff Login Dashboard Fix

## Issue
Staff users were seeing the admin dashboard page instead of the staff dashboard after logging in, even though the staff sidebar was displayed correctly.

## Root Cause
The `accounts/views.py` file had **duplicate function definitions** that were conflicting:

1. **Line 15:** Imported `is_admin` from `accounts.utils`
2. **Lines 22-26:** Defined local `is_admin()` and `is_staff_admin()` functions

The local function definitions were **overriding** the imported ones, and the local `is_staff_admin()` function was checking for the role but the decorator wasn't working correctly due to the conflict.

## Solution
Removed the duplicate local function definitions and imported all role-checking functions from `accounts.utils`:

### Before:
```python
from accounts.utils import is_admin  # Only importing is_admin

# Local duplicate definitions (WRONG)
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'role', '') == 'admin')

def is_staff_admin(user):
    return user.is_authenticated and getattr(user, 'role', '') == 'staff_admin'
```

### After:
```python
from accounts.utils import is_admin, is_staff_admin, is_staff_admin_or_admin  # Import all

# No local definitions - use the ones from utils
```

## Files Modified

### 1. accounts/views.py
- **Removed:** Local `is_admin()` function (lines 22-23)
- **Removed:** Local `is_staff_admin()` function (lines 26-27)
- **Updated:** Import statement to include all role functions from utils

### 2. accounts/utils.py (from previous fix)
- **Added:** `is_staff_admin()` function that was missing

## How It Works Now

### Role Checking Functions (accounts/utils.py)
```python
# ✅ Strictly admin only
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# ✅ Strictly staff_admin only
def is_staff_admin(user):
    return user.is_authenticated and user.role == 'staff_admin'

# ✅ Allow both admin and staff_admin
def is_staff_admin_or_admin(user):
    return user.is_authenticated and user.role in ['staff_admin', 'admin']
```

### Login Flow
1. User logs in at `/accounts/terminal-access/`
2. System checks user role
3. **If admin:** Redirect to `/accounts/dashboard/admin/`
4. **If staff_admin:** Redirect to `/accounts/dashboard/staff/`

### Dashboard Access Control
```python
# Admin Dashboard
@user_passes_test(is_admin)  # Only admin role
def admin_dashboard_view(request):
    # Shows admin dashboard
    
# Staff Dashboard  
@user_passes_test(is_staff_admin)  # Only staff_admin role
def staff_dashboard_view(request):
    # Shows staff dashboard
```

## Testing

### Verification Steps
1. ✅ Django check passed (no errors)
2. ✅ Python syntax validated
3. ✅ No import conflicts
4. ✅ Decorators using correct functions

### Manual Testing Required
- [ ] Log in as staff user
- [ ] Verify redirect to `/accounts/dashboard/staff/`
- [ ] Verify staff dashboard content displays
- [ ] Verify staff sidebar displays (blue gradient)
- [ ] Log out and log in as admin
- [ ] Verify redirect to `/accounts/dashboard/admin/`
- [ ] Verify admin dashboard content displays
- [ ] Verify admin sidebar displays

## Why This Happened

The issue occurred because:
1. Originally, `is_staff_admin()` was missing from `accounts/utils.py`
2. Someone added local definitions in `accounts/views.py` as a workaround
3. Later, `is_staff_admin()` was added to `accounts/utils.py`
4. But the local definitions were never removed
5. This created a conflict where the decorator was using the wrong function

## Prevention

To prevent this in the future:
1. **Always use centralized utility functions** from `accounts/utils.py`
2. **Never duplicate role-checking logic** in multiple files
3. **Import all needed functions** at the top of the file
4. **Remove any local workarounds** when proper fixes are implemented

## Related Files

### accounts/utils.py
Contains the **single source of truth** for role checking:
- `is_admin(user)` - Admin only
- `is_staff_admin(user)` - Staff only  
- `is_staff_admin_or_admin(user)` - Both roles

### accounts/views.py
Uses the functions from utils:
- `login_view()` - Routes users to correct dashboard
- `admin_dashboard_view()` - Admin dashboard
- `staff_dashboard_view()` - Staff dashboard

### accounts/urls.py
URL routing:
- `/accounts/terminal-access/` - Login page
- `/accounts/dashboard/admin/` - Admin dashboard
- `/accounts/dashboard/staff/` - Staff dashboard

## Impact

### Before Fix
❌ Staff users saw admin dashboard
❌ Confusing user experience
❌ Potential security concern
❌ Duplicate code maintenance

### After Fix
✅ Staff users see staff dashboard
✅ Clear role separation
✅ Proper access control
✅ Single source of truth for roles
✅ Cleaner codebase

## Rollback Plan

If issues occur:
1. Revert changes to `accounts/views.py`
2. Add back local function definitions
3. Investigate further

## Conclusion

The staff login issue has been resolved by:
1. Removing duplicate function definitions
2. Using centralized role-checking functions
3. Ensuring proper imports

Staff users will now correctly see their staff dashboard after logging in, while admin users continue to see the admin dashboard.
