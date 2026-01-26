# Queue Count Best Practices

## ✅ Correct Way to Count Active Queue

When you need to count vehicles currently in the terminal queue, **always** use:

```python
from terminal.models import EntryLog

active_queue_count = EntryLog.objects.filter(
    is_active=True, 
    status=EntryLog.STATUS_SUCCESS
).count()
```

### Why This Works:
- `is_active=True` → Vehicle is currently inside the terminal
- `status=EntryLog.STATUS_SUCCESS` → Entry was successful (not failed/insufficient balance)
- Together they represent the **actual current active queue**

---

## ❌ Common Mistakes to Avoid

### 1. Counting All Successful Entries (Historical)
```python
# ❌ WRONG - Counts ALL entries ever, not just active ones
total = EntryLog.objects.filter(status=EntryLog.STATUS_SUCCESS).count()
```

### 2. Using Vehicle Status Field
```python
# ❌ WRONG - Vehicle status may be outdated or not synchronized
total = Vehicle.objects.filter(status__in=["queued", "boarding"]).count()
```

### 3. Using QueueHistory Without Filters
```python
# ❌ WRONG - Counts all history records, not current queue
total = QueueHistory.objects.filter().count()
```

---

## 📊 Common Use Cases

### Display Active Queue Count on Dashboard
```python
@login_required
def dashboard_view(request):
    active_queue = EntryLog.objects.filter(
        is_active=True, 
        status=EntryLog.STATUS_SUCCESS
    ).count()
    
    context = {'active_queue': active_queue}
    return render(request, 'dashboard.html', context)
```

### Get Active Queue Entries with Details
```python
from terminal.models import EntryLog

active_entries = EntryLog.objects.filter(
    is_active=True,
    status=EntryLog.STATUS_SUCCESS
).select_related('vehicle__assigned_driver').order_by('-created_at')

for entry in active_entries:
    print(f"{entry.vehicle.license_plate} - {entry.created_at}")
```

### Count Today's Total Entries (Not Active Queue)
```python
from django.utils import timezone

today = timezone.localtime().date()
today_entries = EntryLog.objects.filter(created_at__date=today).count()
```

### Count Successful Entries in Date Range
```python
from django.utils import timezone
from datetime import timedelta

start_date = timezone.now() - timedelta(days=7)
weekly_entries = EntryLog.objects.filter(
    status=EntryLog.STATUS_SUCCESS,
    created_at__gte=start_date
).count()
```

---

## 🔍 Understanding EntryLog Fields

### `is_active` (Boolean)
- `True` → Vehicle is currently inside the terminal
- `False` → Vehicle has departed (exited)
- Set to `False` when vehicle scans QR at exit

### `status` (CharField)
- `EntryLog.STATUS_SUCCESS` → Entry successful, fee charged
- `EntryLog.STATUS_INSUFFICIENT` → Insufficient wallet balance
- `EntryLog.STATUS_FAILED` → Entry failed for other reasons
- `EntryLog.STATUS_INVALID` → Invalid QR code

### `departed_at` (DateTimeField)
- `None` → Vehicle still in terminal
- `<timestamp>` → When vehicle departed
- Set when `is_active` becomes `False`

---

## 🎯 Quick Reference

| What You Need | Filter to Use |
|---------------|---------------|
| **Active queue count** | `is_active=True, status=STATUS_SUCCESS` |
| **Today's entries** | `created_at__date=today` |
| **Successful entries (any time)** | `status=STATUS_SUCCESS` |
| **Failed entries** | `status__in=[STATUS_FAILED, STATUS_INSUFFICIENT]` |
| **Departed vehicles** | `is_active=False` |
| **Revenue calculation** | `status=STATUS_SUCCESS` + `Sum('fee_charged')` |

---

## 📝 Code Review Checklist

When reviewing code that counts queue entries, verify:

- [ ] Uses `is_active=True` for current queue
- [ ] Uses `status=EntryLog.STATUS_SUCCESS` for successful entries
- [ ] Does NOT rely on `Vehicle.status` field for queue counts
- [ ] Does NOT count all historical entries when only active queue is needed
- [ ] Includes proper date filters when counting historical data
- [ ] Uses `.select_related()` when accessing related vehicle/driver data

---

## 🚨 Migration Note

If you're updating old code that uses incorrect filters:

1. Search for: `Vehicle.objects.filter(status__in=["queued", "boarding"])`
2. Replace with: `EntryLog.objects.filter(is_active=True, status=EntryLog.STATUS_SUCCESS)`

3. Search for: `EntryLog.objects.filter(status=EntryLog.STATUS_SUCCESS).count()`
4. Verify context - if counting active queue, add `is_active=True`

---

## 📚 Related Documentation

- See `QUEUE_COUNT_FIX_SUMMARY.md` for details on the 2026-01-26 fix
- See `terminal/models.py` for EntryLog model definition
- See `terminal/shared_queue.py` for queue maintenance logic (do not modify)

---

**Last Updated:** January 26, 2026  
**Applies To:** RDFS Terminal Management System
