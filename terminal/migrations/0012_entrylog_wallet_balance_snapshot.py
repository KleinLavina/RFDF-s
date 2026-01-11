from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0011_alter_terminalfeebalance_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrylog',
            name='wallet_balance_snapshot',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Wallet balance snapshot at the time the entry log was created.',
                max_digits=12,
                null=True,
            ),
        ),
    ]
