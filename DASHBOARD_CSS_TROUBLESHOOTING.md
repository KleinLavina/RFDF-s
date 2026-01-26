# Dashboard CSS Not Loading - Troubleshooting Guide

## Issue
CSS files for admin and staff dashboards are not loading.

## Files Verified ✅
- ✅ `static/styles/accounts/admin-dashboard.css` exists
- ✅ `static/styles/accounts/staff-dashboard.css` exists
- ✅ `staticfiles/styles/accounts/admin-dashboard.css` exists (collected)
- ✅ `staticfiles/styles/accounts/staff-dashboard.css` exists (collected)
- ✅ `templates/base.html` has `{% block extra_css %}` added
- ✅ Templates use correct `{% static %}` tags
- ✅ `collectstatic` ran successfully (54 files copied)

## Steps to Fix

### 1. Restart Django Development Server
```bash
# Stop the current server (Ctrl+C if running)
# Then restart:
python manage.py runserver
```

### 2. Clear Browser Cache
**Chrome/Edge:**
- Press `Ctrl + Shift + Delete`
- Select "Cached images and files"
- Click "Clear data"

**Or use Hard Refresh:**
- Press `Ctrl + F5` (Windows)
- Or `Ctrl + Shift + R`

### 3. Verify Static Files Settings
Check `rdfs/settings.py`:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 4. Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for 404 errors for CSS files
4. Check Network tab for failed requests

### 5. Verify URL in Browser
Try accessing CSS directly:
- `http://127.0.0.1:8000/static/styles/accounts/admin-dashboard.css`
- `http://127.0.0.1:8000/static/styles/accounts/staff-dashboard.css`

If you get 404, the issue is with static file serving.

### 6. Check DEBUG Mode
In `.env` file:
```
DEBUG=True
```

### 7. Re-run collectstatic
```bash
python manage.py collectstatic --clear --noinput
```

### 8. Check File Permissions
```bash
# Windows PowerShell
Get-Acl static/styles/accounts/admin-dashboard.css | Format-List
```

## Quick Test

### Test 1: View Page Source
1. Go to admin dashboard
2. Right-click → "View Page Source"
3. Search for "admin-dashboard.css"
4. Should see: `<link rel="stylesheet" href="/static/styles/accounts/admin-dashboard.css?v=1.0">`

### Test 2: Check Link
1. Click the CSS link in page source
2. Should see CSS code, not 404 error

### Test 3: Inspect Element
1. Right-click any element on dashboard
2. Click "Inspect"
3. Check "Styles" panel
4. Should see styles from `.admin-dashboard`, `.stat-card`, etc.

## Common Issues & Solutions

### Issue: 404 Not Found
**Solution:** Run `python manage.py collectstatic --noinput`

### Issue: Old Styles Showing
**Solution:** Hard refresh browser (Ctrl + F5)

### Issue: CSS Not Applied
**Solution:** Check browser console for syntax errors

### Issue: Blank Page
**Solution:** Check template syntax errors in Django logs

### Issue: Mixed Content (HTTPS)
**Solution:** Ensure STATIC_URL uses correct protocol

## Verification Commands

```bash
# Check if files exist
Test-Path static/styles/accounts/admin-dashboard.css
Test-Path static/styles/accounts/staff-dashboard.css

# Check if collected
Test-Path staticfiles/styles/accounts/admin-dashboard.css
Test-Path staticfiles/styles/accounts/staff-dashboard.css

# List all dashboard CSS files
Get-ChildItem -Path static/styles/accounts/ -Filter "*dashboard*"

# Check file size (should be ~12KB and ~10KB)
(Get-Item static/styles/accounts/admin-dashboard.css).Length
(Get-Item static/styles/accounts/staff-dashboard.css).Length
```

## Expected Results

### Admin Dashboard
- Modern gradient stat cards with icons
- Large revenue cards with glassmorphism
- Interactive profit chart
- 3 action cards with hover effects
- Smooth animations

### Staff Dashboard
- Horizontal stat cards with large icons
- 6 action cards in grid layout
- Gradient backgrounds
- Ripple effects on hover

## If Still Not Working

### Check Django Logs
Look for errors when accessing the page:
```
[timestamp] "GET /static/styles/accounts/admin-dashboard.css HTTP/1.1" 404
```

### Verify Template Inheritance
Ensure templates extend base.html correctly:
```django
{% extends "base.html" %}
{% load static %}
{% block extra_css %}
<link rel="stylesheet" href="{% static 'styles/accounts/admin-dashboard.css' %}?v=1.0">
{% endblock %}
```

### Check STATICFILES_FINDERS
In `settings.py`:
```python
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
```

## Manual Fix (Last Resort)

If nothing works, add CSS inline temporarily:

1. Copy content from `static/styles/accounts/admin-dashboard.css`
2. Paste in `<style>` tag in template head
3. This confirms CSS code works
4. Then debug static file serving

## Contact Points

If issue persists:
1. Check Django version compatibility
2. Verify whitenoise configuration (if using)
3. Check web server configuration (nginx/apache)
4. Review ALLOWED_HOSTS setting

## Success Indicators

✅ No 404 errors in browser console  
✅ CSS file loads when accessed directly  
✅ Styles appear in DevTools inspector  
✅ Dashboard looks modern with gradients  
✅ Hover effects work on cards  
✅ Animations play on page load  

---

**Last Updated:** January 26, 2026  
**Status:** Troubleshooting Active
