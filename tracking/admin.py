from django.contrib import admin
from .models import Van, Driver, Location, Trip


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_number', 'phone', 'email', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'license_number', 'email']


@admin.register(Van)
class VanAdmin(admin.ModelAdmin):
    list_display = ['registration', 'model', 'status', 'driver', 'mileage_km', 'last_service_date']
    list_filter = ['status']
    search_fields = ['registration', 'model']
    list_select_related = ['driver']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['van', 'latitude', 'longitude', 'address', 'speed_kmh', 'timestamp']
    list_filter = ['van']
    readonly_fields = ['timestamp']


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['van', 'driver', 'origin', 'destination', 'status', 'scheduled_departure']
    list_filter = ['status']
    search_fields = ['origin', 'destination']
