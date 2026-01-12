from django.db import migrations, models


def _format_route_display(route):
    if not route:
        return "Unassigned route"

    origin = getattr(route, "origin", "")
    destination = getattr(route, "destination", "")
    if origin and destination:
        return f"{origin} → {destination}"

    name = getattr(route, "name", "")
    if name:
        return name

    return str(route)


def _backfill_terminal_activity(apps, schema_editor):
    TerminalActivity = apps.get_model("terminal", "TerminalActivity")
    QueueHistory = apps.get_model("vehicles", "QueueHistory")

    for queue in QueueHistory.objects.all():
        route = (
            _format_route_display(queue.vehicle.route)
            if queue.vehicle and queue.vehicle.route
            else "Unassigned route"
        )
        TerminalActivity.objects.update_or_create(
            queue_history=queue,
            defaults={
                "vehicle_id": queue.vehicle_id,
                "driver_id": queue.driver_id,
                "route_name": route,
                "event_type": queue.action,
                "fee_charged": queue.fee_charged,
                "wallet_balance_snapshot": queue.wallet_balance_snapshot,
                "timestamp": queue.timestamp,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("terminal", "0013_entrylog_boarding_started"),
        ("vehicles", "0016_queuehistory_fee"),
    ]

    operations = [
        migrations.CreateModel(
            name="TerminalActivity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("route_name", models.CharField(default="Unassigned route", max_length=200)),
                ("event_type", models.CharField(choices=[("enter", "Entry"), ("exit", "Exit")], max_length=10)),
                ("fee_charged", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("wallet_balance_snapshot", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("timestamp", models.DateTimeField()),
                ("entry_log", models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name="terminal_activities", to="terminal.entrylog")),
                ("driver", models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name="terminal_activities", to="vehicles.driver")),
                ("queue_history", models.OneToOneField(on_delete=models.CASCADE, related_name="terminal_activity", to="vehicles.queuehistory")),
                ("vehicle", models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name="terminal_activities", to="vehicles.vehicle")),
            ],
        ),
        migrations.RunPython(_backfill_terminal_activity, migrations.RunPython.noop),
    ]
