from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Van',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration', models.CharField(max_length=20, unique=True)),
                ('model', models.CharField(max_length=100)),
                ('capacity_kg', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('available', 'Available'), ('on_route', 'On Route'), ('maintenance', 'Maintenance'), ('inactive', 'Inactive')], default='available', max_length=20)),
                ('last_service_date', models.DateField(blank=True, null=True)),
                ('mileage_km', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vans', to='tracking.driver')),
            ],
            options={'ordering': ['registration']},
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('speed_kmh', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('van', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='tracking.van')),
            ],
            options={'ordering': ['-timestamp'], 'get_latest_by': 'timestamp'},
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20)),
                ('scheduled_departure', models.DateTimeField()),
                ('actual_departure', models.DateTimeField(blank=True, null=True)),
                ('actual_arrival', models.DateTimeField(blank=True, null=True)),
                ('distance_km', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trips', to='tracking.driver')),
                ('van', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='tracking.van')),
            ],
            options={'ordering': ['-scheduled_departure']},
        ),
    ]
