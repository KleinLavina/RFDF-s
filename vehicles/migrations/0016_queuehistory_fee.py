from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0015_alter_driver_driver_photo_alter_vehicle_qr_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="queuehistory",
            name="fee_charged",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
