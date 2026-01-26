# Quick Start: System & Routes Page

## Accessing the Page

### From Admin Dashboard
1. Log in as Admin
2. Click on "System & Routes" card in the Quick Actions section

### From Sidebar
1. Navigate to Settings section in sidebar
2. Click "System & Routes"

### Direct URL
```
http://127.0.0.1:8000/terminal/system-and-routes/
```

---

## Using System Settings Tab

### Updating Settings
1. Click "System Settings" tab (default view)
2. Modify any of the following:
   - **Terminal Entry Fee** - Fee charged per vehicle entry
   - **Minimum Deposit** - Required minimum wallet balance
   - **Entry Cooldown** - Time between consecutive entries
   - **Stay Duration** - Max time before departure
   - **Countdown Duration** - Timer duration for displays
   - **Auto-Refresh Interval** - Display refresh rate
   - **Seat Capacity Limits** - Max seats per vehicle type
   - **System Theme** - Light/Dark mode preference

3. Click "Save Settings" button
4. Confirm in the modal popup
5. Success message will appear

### Current Fee Banner
- Shows current terminal fee at the top
- Displays last update timestamp

---

## Using Route Management Tab

### Viewing Route Analytics
1. Click "Route Management" tab
2. View stats dashboard:
   - Active Routes count
   - Total Trips count
   - Total Fees collected
   - Top Route by trips

3. View route activity chart
   - Bar chart showing trips per route
   - Hover for exact numbers

### Adding a New Route
1. Scroll to "Add New Route" section
2. Fill in:
   - **Origin** - Starting location (required)
   - **Destination** - End location (required)
   - **Base Fare** - Fare amount (optional)
   - **Active** - Check to activate immediately

3. Click "Add Route" button
4. Success message will appear

### Editing a Route
1. Find route in "Existing Routes" table
2. Click edit icon (pencil) button
3. Modal will open with current values
4. Modify fields as needed
5. Click "Save Changes"
6. Success message will appear

### Deleting a Route
1. Find route in "Existing Routes" table
2. Click delete icon (trash) button
3. Confirm deletion in browser prompt
4. Success message will appear

### Route Table Columns
- **#** - Row number
- **Origin** - Starting location
- **Destination** - End location
- **Fare** - Base fare amount
- **Status** - Active (green) or Inactive (gray)
- **Actions** - Edit and Delete buttons

---

## Tips & Best Practices

### Settings
- Always use the confirmation modal before saving settings
- Changes apply immediately to all future entries
- Test settings in development before production
- Document any major changes for your team

### Routes
- Use clear, consistent naming for origins/destinations
- Set realistic base fares based on distance
- Deactivate routes instead of deleting (preserves history)
- Review route analytics regularly to optimize operations

### Navigation
- Use tabs to quickly switch between sections
- Both sections are on the same page (no reload needed)
- Sidebar link always returns to last active tab
- Dashboard card opens to Settings tab by default

---

## Troubleshooting

### Settings Not Saving
- Check for validation errors below form fields
- Ensure all required fields are filled
- Verify you have admin permissions
- Check browser console for JavaScript errors

### Route Not Adding
- Verify both origin and destination are filled
- Check if route already exists (duplicates prevented)
- Ensure you have admin permissions
- Look for error message at top of page

### Chart Not Displaying
- Ensure Chart.js is loaded (check browser console)
- Verify there is route data to display
- Try refreshing the page
- Check if JavaScript is enabled

### Tab Not Switching
- Check browser console for JavaScript errors
- Ensure Bootstrap JS is loaded
- Try hard refresh (Ctrl+F5)
- Clear browser cache if needed

---

## Keyboard Shortcuts (Future Enhancement)

Currently not implemented, but planned:
- `Alt+1` - Switch to Settings tab
- `Alt+2` - Switch to Routes tab
- `Ctrl+S` - Save settings (when in Settings tab)
- `Ctrl+N` - Focus on new route form (when in Routes tab)

---

## Mobile Usage

### Responsive Features
- Tabs scroll horizontally on small screens
- Forms stack vertically on mobile
- Stats cards stack in single column
- Table scrolls horizontally if needed
- Touch-friendly button sizes

### Mobile Tips
- Use landscape mode for better table viewing
- Pinch to zoom on chart for details
- Swipe tabs for quick navigation
- Use browser back button to return to dashboard

---

## Support

For issues or questions:
1. Check this guide first
2. Review SYSTEM_AND_ROUTES_MERGE.md for technical details
3. Contact your system administrator
4. Check application logs for errors

---

## Version History

**v1.0** (Current)
- Initial unified page release
- Tab-based navigation
- Settings form with confirmation
- Route CRUD operations
- Analytics dashboard
- Chart.js integration
- Mobile responsive design
