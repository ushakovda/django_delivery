# Generated by Django 4.1.3 on 2024-10-26 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParcelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('content_value_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_cost_rub', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('parcel_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='registration.parceltype')),
            ],
        ),
    ]