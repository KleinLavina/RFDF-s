# TV Display Board Header Fix

## Issue
The table header fields on `/terminal/tv-display/` were not visible - the text appeared very faint (dark blue on dark blue background) and columns were not properly aligned.

## Root Cause
1. CSS file had old dark theme styling with dark background colors
2. HTML template class names didn't match CSS selectors (e.g., `board-header` vs `.departure-board__header`)
3. Grid column definitions were mismatched between header and rows
4. Header text color was not explicitly set to white

## Solution Applied

### 1. Updated Color Scheme (White Background)
```css
:root {
  --tv-bg: #ffffff;              /* White background */
  --tv-surface: #f8fafc;         /* Light gray surface */
  --tv-border: #e2e8f0;          /* Light border */
  --tv-text-primary: #112666;    /* Dark blue text */
  --tv-text-secondary: #64748b;  /* Gray text */
  --tv-accent: #2563eb;          /* Blue accent */
}
```

### 2. Fixed Board Header Styling
```css
.board-header {
  display: grid;
  grid-template-columns: 2fr 1.5fr 2.5fr 1.5fr 1.5fr;
  background: linear-gradient(135deg, #112666 0%, #1e3a8a 100%);
  color: #ffffff;  /* Explicit white text */
  font-weight: 800;
  font-size: 1rem;
  letter-spacing: 1px;
}

.board-header > div {
  color: #ffffff;  /* Ensure all child divs have white text */
}

.board-header i {
  color: #60a5fa;  /* Light blue icons */
}
```

### 3. Matched Grid Columns
Both header and rows now use the same grid structure:
```css
grid-template-columns: 2fr 1.5fr 2.5fr 1.5fr 1.5fr;
/* Departure Time | Route | Destination | Vehicle | Status */
```

### 4. Enhanced Typography for TV Viewing
- **Departure Time**: 3rem, monospace font, dark blue
- **Route**: 2rem, bold, blue accent color
- **Destination**: 1.75rem with icon, dark blue
- **Vehicle**: 1.5rem in styled box with gradient background
- **Status**: 1.125rem badges with gradient backgrounds and icons

### 5. Updated Header Design
- Gradient blue background (#112666 to #1e3a8a)
- White text throughout
- Light blue icons (#60a5fa)
- Proper spacing and padding
- Box shadow for depth

## Files Modified
- `static/styles/terminal/tv_display.css` - Complete redesign with white background
- `templates/terminal/tv_display.html` - Version bump to v=6.0
- `staticfiles/` - Collected static files

## Testing Checklist
- [ ] Header text is clearly visible (white on dark blue gradient)
- [ ] All column headers are aligned with data rows
- [ ] Grid columns maintain proper spacing
- [ ] Icons are visible and properly colored
- [ ] Typography is large enough for TV viewing
- [ ] Auto-refresh works every 15 seconds
- [ ] Status badges display with proper colors and icons
- [ ] Hover effects work on departure rows
- [ ] Empty state displays when no departures

## Version
CSS/JS version bumped to **v=6.0** to force cache refresh

## Deployment
Run `python manage.py collectstatic --noinput` to update static files on server.
