# Quick Start: Deposit Management

## Accessing the Page

### From Dashboard
**Staff Dashboard:**
1. Log in as Staff or Admin
2. Click "Deposit Management" card in Quick Actions

**Admin Dashboard:**
1. Log in as Admin
2. Navigate via sidebar: Transactions → Deposits

### From Sidebar
1. Expand "Transactions" section
2. Click "Deposits"

### Direct URL
```
http://127.0.0.1:8000/terminal/deposits/
```

---

## Using Driver Wallets Tab

### Viewing Wallet Information
1. Click "Driver Wallets" tab (default view)
2. View stats at the top:
   - Total Wallets
   - Total Balance
   - Low Balance Count
   - Total Deposits

### Searching for a Driver
1. Type in the "Live Search" field
2. Results update automatically as you type
3. Search works for:
   - Driver name
   - License number
   - License plate

### Sorting Wallets
1. Use the "Sort By" dropdown
2. Options:
   - **Newest Deposits** - Most recent activity first
   - **Largest Balance** - Highest balance first
   - **Smallest Balance** - Lowest balance first
   - **Driver A → Z** - Alphabetical ascending
   - **Driver Z → A** - Alphabetical descending
3. Results update instantly

### Understanding Balance Badges
- **Green (High)** - Balance ≥ ₱500
- **Blue (Medium)** - Balance ≥ ₱200
- **Yellow (Low)** - Balance ≥ minimum required
- **Red (Critical)** - Balance < minimum required

### Adding a Deposit (Method 1: Quick Action)
1. Find the driver in the table
2. Click the **+** button in the Actions column
3. Modal opens with driver pre-selected
4. Enter deposit amount
5. Click "Confirm Deposit"
6. Success message appears

### Adding a Deposit (Method 2: Main Button)
1. Click "Add Deposit" button (top right)
2. Start typing driver name, license, or plate
3. Select driver from dropdown suggestions
4. System shows current balance
5. Enter deposit amount
6. Click "Confirm Deposit"
7. Success message appears

---

## Using Deposit History Tab

### Viewing History
1. Click "Deposit History" tab
2. View stats:
   - Total Records
   - Total Amount Deposited

### Filtering History
1. Enter search term in "Search" field
2. Select sort option from "Sort By" dropdown
3. Click "Apply Filters" button
4. Results update with filtered data

### Sort Options
- **Newest First** - Most recent deposits
- **Largest Amount** - Highest amounts first
- **Smallest Amount** - Lowest amounts first
- **Driver A → Z** - Alphabetical ascending
- **Driver Z → A** - Alphabetical descending

### Understanding Status Badges
- **Green (Completed/Success)** - Deposit successful
- **Yellow (Pending)** - Processing
- **Red (Failed)** - Deposit failed

### Reading Reference Numbers
- Each deposit has a unique reference code
- Format: Monospace font for easy reading
- Use for tracking and support

---

## Modal: Add Deposit

### Step-by-Step Guide

**Step 1: Open Modal**
- Click "Add Deposit" button, OR
- Click **+** button next to a driver

**Step 2: Select Driver**
- Type in search field
- Suggestions appear as you type
- Click on desired driver
- Current balance displays automatically

**Step 3: Enter Amount**
- Click in "Deposit Amount" field
- Enter amount (e.g., 500.00)
- Must be greater than zero
- Use decimal point for cents

**Step 4: Review**
- Check selected driver name
- Verify current balance shown
- Confirm amount is correct

**Step 5: Submit**
- Click "Confirm Deposit" button
- Wait for confirmation message
- Modal closes automatically

**Step 6: Verify**
- Check success message
- Wallet table updates automatically
- New balance reflects deposit

### Modal Features

**Autocomplete Search:**
- Type any part of name, license, or plate
- Up to 6 suggestions shown
- Click to select
- "No matching driver found" if none match

**Balance Display:**
- Shows current wallet balance
- Updates when driver selected
- Helps verify before depositing

**Form Validation:**
- Submit button disabled until valid
- Must select driver
- Must enter amount > 0
- Clear error messages

**Visual Feedback:**
- Selected driver highlighted with checkmark
- Loading spinner while fetching balance
- Disabled state for invalid forms

---

## Tips & Best Practices

### For Efficient Searching
- Use partial names (e.g., "Juan" finds "Juan Dela Cruz")
- Use plate numbers for quick lookup
- Live search is instant - no need to press Enter

### For Adding Deposits
- Use quick action buttons for known drivers
- Use main button for searching drivers
- Double-check amount before submitting
- Watch for success confirmation

### For Monitoring Balances
- Check "Low Balance" stat regularly
- Sort by "Smallest Balance" to find critical wallets
- Red badges indicate urgent attention needed
- Green badges indicate healthy balances

### For Reviewing History
- Use date sorting for recent activity
- Use amount sorting for large transactions
- Reference numbers help track specific deposits
- Status badges show transaction state

---

## Troubleshooting

### Search Not Working
- Check spelling
- Try partial names
- Use license plate instead
- Clear search and try again

### Modal Not Opening
- Check browser console for errors
- Ensure JavaScript is enabled
- Try refreshing page
- Clear browser cache

### Deposit Not Submitting
- Verify driver is selected
- Check amount is greater than zero
- Ensure amount has valid format
- Look for error messages

### Balance Not Displaying
- Check internet connection
- Verify driver has wallet
- Try selecting driver again
- Refresh page if needed

### Tab Not Switching
- Check browser console
- Ensure JavaScript is enabled
- Try hard refresh (Ctrl+F5)
- Clear browser cache

---

## Keyboard Shortcuts

### Navigation
- `Tab` - Move between fields
- `Enter` - Submit form (when valid)
- `Esc` - Close modal
- `Arrow Keys` - Navigate dropdown suggestions

### Search
- Start typing in search field
- No need to click first
- Results update automatically
- Clear with Backspace

---

## Mobile Usage

### Responsive Features
- Tabs scroll horizontally if needed
- Tables scroll horizontally
- Stats stack vertically
- Modal fills screen appropriately
- Touch-friendly button sizes

### Mobile Tips
- Use landscape for better table viewing
- Pinch to zoom if needed
- Swipe to scroll tables
- Tap to select from dropdowns
- Use native keyboard for amounts

---

## Common Workflows

### Daily Deposit Processing
1. Open Deposits page
2. Click "Add Deposit" button
3. Search for first driver
4. Enter amount
5. Submit
6. Repeat for next driver
7. Review history tab at end of day

### Checking Low Balances
1. Open Deposits page
2. Check "Low Balance" stat
3. Sort by "Smallest Balance"
4. Review red-badged wallets
5. Add deposits as needed
6. Verify balances updated

### Finding Specific Deposit
1. Switch to "Deposit History" tab
2. Enter driver name in search
3. Click "Apply Filters"
4. Locate deposit by reference number
5. Note status and amount

### Bulk Deposit Session
1. Prepare list of drivers and amounts
2. Open Deposits page
3. Use quick action buttons for speed
4. Work through list systematically
5. Verify each success message
6. Review history tab when complete

---

## Best Practices

### Data Entry
- Always verify driver before submitting
- Double-check amounts
- Use consistent decimal format
- Watch for success confirmations

### Monitoring
- Check low balances daily
- Review history regularly
- Track large deposits
- Monitor failed transactions

### Organization
- Process deposits at consistent times
- Keep reference numbers for records
- Note any unusual transactions
- Report issues promptly

---

## Support

### Getting Help
1. Check this guide first
2. Review error messages carefully
3. Try troubleshooting steps
4. Contact system administrator
5. Provide reference numbers for issues

### Reporting Issues
Include:
- What you were trying to do
- Steps you took
- Error message (if any)
- Reference number (if applicable)
- Browser and device info

---

## Quick Reference

### URLs
- Main Page: `/terminal/deposits/`
- Wallets Tab: `/terminal/deposits/?tab=wallets`
- History Tab: `/terminal/deposits/?tab=history`

### Minimum Balance
- Check info banner at top of page
- Red badges indicate below minimum
- System prevents entry if too low

### Color Codes
- **Green** - Good/High/Success
- **Blue** - Medium/Normal
- **Yellow** - Low/Warning/Pending
- **Red** - Critical/Error/Failed

### Quick Actions
- **+ Button** - Add deposit for that driver
- **Add Deposit** - Open modal to search
- **Tab Buttons** - Switch between views
- **Sort Dropdown** - Change order
- **Search Field** - Filter results
