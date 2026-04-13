from django import forms
from .models import Van, Driver, Trip, Location


class VanForm(forms.ModelForm):
    class Meta:
        model = Van
        fields = ['registration', 'model', 'capacity_kg', 'status', 'driver', 'last_service_date', 'mileage_km']
        widgets = {
            'last_service_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'phone', 'email', 'is_active']


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['van', 'driver', 'origin', 'destination', 'status',
                  'scheduled_departure', 'actual_departure', 'actual_arrival',
                  'distance_km', 'notes']
        widgets = {
            'scheduled_departure': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'actual_departure': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'actual_arrival': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'address', 'speed_kmh']
