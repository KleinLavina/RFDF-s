from django.contrib import admin
from .models import TerminalFeeBalance, EntryLog, SystemSettings, TerminalActivity

admin.site.register(SystemSettings)


@admin.register(TerminalFeeBalance)
class TerminalFeeBalanceAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "balance")
    search_fields = ("vehicle__plate_number",)
    ordering = ("vehicle",)


@admin.register(EntryLog)
class EntryLogAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "staff", "status", "fee_charged", "created_at")
    list_filter = ("status", "staff")
    search_fields = ("vehicle__plate_number", "staff__username")
    ordering = ("-created_at",)


@admin.register(TerminalActivity)
class TerminalActivityAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle",
        "driver",
        "event_type",
        "fee_charged",
        "timestamp",
    )
    list_filter = ("event_type",)
    search_fields = ("vehicle__license_plate", "driver__last_name")
    ordering = ("-timestamp",)
