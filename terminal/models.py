from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

from vehicles.models import Vehicle, VehicleBalanceBase


class TerminalFeeBalance(VehicleBalanceBase):
    vehicle = models.OneToOneField(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='fee_balance'
    )

    def clean(self):
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative.")

    def __str__(self):
        plate = getattr(self.vehicle, 'plate_number', None) or getattr(self.vehicle, 'license_plate', None)
        return f"Balance for {plate or self.vehicle.pk}"


class EntryLog(models.Model):
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_INSUFFICIENT = 'insufficient'
    STATUS_INVALID = 'invalid'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_INSUFFICIENT, 'Insufficient Balance'),
        (STATUS_INVALID, 'Invalid QR'),
    ]

    vehicle = models.ForeignKey(
        'vehicles.Vehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entry_logs'
    )
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='terminal_actions'
    )
    fee_charged = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wallet_balance_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Wallet balance snapshot at the time the entry log was created.",
    )
    boarding_started_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_FAILED)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    departed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Entry Log"
        verbose_name_plural = "Entry Logs"

    def __str__(self):
        plate = getattr(self.vehicle, 'plate_number', None) or getattr(self.vehicle, 'license_plate', None)
        state = "Active" if self.is_active else "Exited"
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {plate or 'Unknown vehicle'} - {self.status} ({state})"


class TerminalActivity(models.Model):
    EVENT_ENTRY = 'enter'
    EVENT_EXIT = 'exit'

    EVENT_CHOICES = [
        (EVENT_ENTRY, 'Entry'),
        (EVENT_EXIT, 'Exit'),
    ]

    queue_history = models.OneToOneField(
        "vehicles.QueueHistory",
        on_delete=models.CASCADE,
        related_name="terminal_activity",
    )
    entry_log = models.ForeignKey(
        EntryLog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terminal_activities",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terminal_activities",
    )
    driver = models.ForeignKey(
        "vehicles.Driver",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terminal_activities",
    )
    route_name = models.CharField(max_length=200, default="Unassigned route")
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    fee_charged = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wallet_balance_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.get_event_type_display()} – {self.route_name} @ {self.timestamp:%Y-%m-%d %H:%M}"


class SystemSettings(models.Model):
    terminal_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    min_deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    entry_cooldown_minutes = models.PositiveIntegerField(default=5)
    departure_duration_minutes = models.PositiveIntegerField(default=30)

    # Countdown duration for boarding/departure preparation phase (in seconds)
    countdown_duration_seconds = models.PositiveIntegerField(
        default=30,
        help_text="Duration of countdown timer before state transitions (in seconds)"
    )

    # Seat capacity limits (editable by admin)
    jeepney_max_seats = models.PositiveIntegerField(default=25)
    van_max_seats = models.PositiveIntegerField(default=15)
    bus_max_seats = models.PositiveIntegerField(default=60)

    theme_preference = models.CharField(
        max_length=10,
        choices=[('light', 'Light Mode'), ('dark', 'Dark Mode')],
        default='light'
    )

    # Queue display refresh interval (in seconds)
    queue_refresh_interval_seconds = models.PositiveIntegerField(
        default=15,
        help_text="How often queue displays auto-refresh (in seconds)"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"System Settings (Fee: ₱{self.terminal_fee}, "
            f"Min Deposit: ₱{self.min_deposit_amount}, "
            f"Stay: {self.departure_duration_minutes} mins)"
        )

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class Transaction(models.Model):
    """
    Immutable snapshot of every terminal entry/exit transaction.
    Used for historical records, analytics, and CSV export.
    """
    # Core references
    vehicle = models.ForeignKey(
        'vehicles.Vehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    driver = models.ForeignKey(
        'vehicles.Driver',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    entry_log = models.ForeignKey(
        EntryLog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )

    # Snapshot data (immutable once created)
    vehicle_plate = models.CharField(max_length=50, default="—")
    driver_name = models.CharField(max_length=200, default="N/A")
    route_name = models.CharField(max_length=200, default="Unassigned")

    # Timestamps
    entry_timestamp = models.DateTimeField()
    exit_timestamp = models.DateTimeField(null=True, blank=True)

    # Financial snapshots
    fee_charged = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wallet_balance_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Date breakdown for analytics
    transaction_date = models.DateField()
    transaction_year = models.PositiveIntegerField()
    transaction_month = models.PositiveIntegerField()
    transaction_day = models.PositiveIntegerField()

    # System revenue tracking
    is_revenue_counted = models.BooleanField(
        default=True,
        help_text="Whether this transaction counts toward daily revenue"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entry_timestamp']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=['transaction_date']),
            models.Index(fields=['transaction_year', 'transaction_month']),
            models.Index(fields=['vehicle_plate']),
        ]

    def __str__(self):
        return f"[{self.entry_timestamp:%Y-%m-%d %H:%M}] {self.vehicle_plate} - ₱{self.fee_charged}"

    @classmethod
    def create_from_entry_log(cls, entry_log, exit_timestamp=None):
        """Create an immutable transaction snapshot from an entry log."""
        from django.utils import timezone

        vehicle = entry_log.vehicle
        driver = getattr(vehicle, 'assigned_driver', None) if vehicle else None
        route = getattr(vehicle, 'route', None) if vehicle else None

        entry_time = entry_log.created_at
        exit_time = exit_timestamp or entry_log.departed_at
        tx_date = timezone.localtime(entry_time).date()

        return cls.objects.create(
            vehicle=vehicle,
            driver=driver,
            entry_log=entry_log,
            vehicle_plate=getattr(vehicle, 'license_plate', '—') if vehicle else '—',
            driver_name=f"{driver.first_name} {driver.last_name}" if driver else "N/A",
            route_name=f"{route.origin} → {route.destination}" if route else "Unassigned",
            entry_timestamp=entry_time,
            exit_timestamp=exit_time,
            fee_charged=entry_log.fee_charged or 0,
            wallet_balance_snapshot=entry_log.wallet_balance_snapshot,
            transaction_date=tx_date,
            transaction_year=tx_date.year,
            transaction_month=tx_date.month,
            transaction_day=tx_date.day,
            is_revenue_counted=entry_log.status == EntryLog.STATUS_SUCCESS,
        )


@receiver(post_save, sender=Vehicle)
def create_terminal_fee_balance(sender, instance, created, **kwargs):
    if created:
        TerminalFeeBalance.objects.create(vehicle=instance)
    else:
        TerminalFeeBalance.objects.get_or_create(vehicle=instance)
