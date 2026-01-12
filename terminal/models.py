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

    # 🟢 NEW: Seat capacity limits (editable by admin)
    jeepney_max_seats = models.PositiveIntegerField(default=25)
    van_max_seats = models.PositiveIntegerField(default=15)
    bus_max_seats = models.PositiveIntegerField(default=60)

    theme_preference = models.CharField(
        max_length=10,
        choices=[('light', 'Light Mode'), ('dark', 'Dark Mode')],
        default='light'
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


@receiver(post_save, sender=Vehicle)
def create_terminal_fee_balance(sender, instance, created, **kwargs):
    if created:
        TerminalFeeBalance.objects.create(vehicle=instance)
    else:
        TerminalFeeBalance.objects.get_or_create(vehicle=instance)
