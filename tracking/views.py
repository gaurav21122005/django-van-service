from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import json

from .models import Van, Driver, Location, Trip
from .forms import VanForm, DriverForm, TripForm, LocationUpdateForm


def dashboard(request):
    vans = Van.objects.select_related('driver').all()
    total_vans = vans.count()
    on_route = vans.filter(status='on_route').count()
    available = vans.filter(status='available').count()
    maintenance = vans.filter(status='maintenance').count()
    recent_trips = Trip.objects.select_related('van', 'driver').order_by('-created_at')[:5]
    recent_locations = Location.objects.select_related('van').order_by('-timestamp')[:10]

    context = {
        'vans': vans,
        'total_vans': total_vans,
        'on_route': on_route,
        'available': available,
        'maintenance': maintenance,
        'recent_trips': recent_trips,
        'recent_locations': recent_locations,
    }
    return render(request, 'tracking/dashboard.html', context)


# --- Van Views ---

def van_list(request):
    vans = Van.objects.select_related('driver').all()
    return render(request, 'tracking/van_list.html', {'vans': vans})


def van_detail(request, pk):
    van = get_object_or_404(Van, pk=pk)
    locations = van.locations.order_by('-timestamp')[:20]
    trips = van.trips.select_related('driver').order_by('-scheduled_departure')[:10]
    return render(request, 'tracking/van_detail.html', {
        'van': van, 'locations': locations, 'trips': trips
    })


def van_create(request):
    if request.method == 'POST':
        form = VanForm(request.POST)
        if form.is_valid():
            van = form.save()
            messages.success(request, f'Van {van.registration} added successfully.')
            return redirect('van_detail', pk=van.pk)
    else:
        form = VanForm()
    return render(request, 'tracking/van_form.html', {'form': form, 'title': 'Add Van'})


def van_edit(request, pk):
    van = get_object_or_404(Van, pk=pk)
    if request.method == 'POST':
        form = VanForm(request.POST, instance=van)
        if form.is_valid():
            form.save()
            messages.success(request, 'Van updated successfully.')
            return redirect('van_detail', pk=van.pk)
    else:
        form = VanForm(instance=van)
    return render(request, 'tracking/van_form.html', {'form': form, 'title': 'Edit Van', 'van': van})


def van_delete(request, pk):
    van = get_object_or_404(Van, pk=pk)
    if request.method == 'POST':
        reg = van.registration
        van.delete()
        messages.success(request, f'Van {reg} deleted.')
        return redirect('van_list')
    return render(request, 'tracking/confirm_delete.html', {'object': van, 'type': 'Van'})


# --- Driver Views ---

def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'tracking/driver_list.html', {'drivers': drivers})


def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    trips = driver.trips.select_related('van').order_by('-scheduled_departure')[:10]
    return render(request, 'tracking/driver_detail.html', {'driver': driver, 'trips': trips})


def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            driver = form.save()
            messages.success(request, f'Driver {driver.name} added.')
            return redirect('driver_detail', pk=driver.pk)
    else:
        form = DriverForm()
    return render(request, 'tracking/driver_form.html', {'form': form, 'title': 'Add Driver'})


def driver_edit(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver updated.')
            return redirect('driver_detail', pk=driver.pk)
    else:
        form = DriverForm(instance=driver)
    return render(request, 'tracking/driver_form.html', {'form': form, 'title': 'Edit Driver', 'driver': driver})


def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        name = driver.name
        driver.delete()
        messages.success(request, f'Driver {name} deleted.')
        return redirect('driver_list')
    return render(request, 'tracking/confirm_delete.html', {'object': driver, 'type': 'Driver'})


# --- Trip Views ---

def trip_list(request):
    trips = Trip.objects.select_related('van', 'driver').all()
    return render(request, 'tracking/trip_list.html', {'trips': trips})


def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save()
            messages.success(request, 'Trip scheduled.')
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'tracking/trip_form.html', {'form': form, 'title': 'Schedule Trip'})


def trip_edit(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip updated.')
            return redirect('trip_list')
    else:
        form = TripForm(instance=trip)
    return render(request, 'tracking/trip_form.html', {'form': form, 'title': 'Edit Trip', 'trip': trip})


def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Trip deleted.')
        return redirect('trip_list')
    return render(request, 'tracking/confirm_delete.html', {'object': trip, 'type': 'Trip'})


# --- Location / API ---

@require_POST
def update_location(request, van_pk):
    van = get_object_or_404(Van, pk=van_pk)
    try:
        data = json.loads(request.body)
        Location.objects.create(
            van=van,
            latitude=data['latitude'],
            longitude=data['longitude'],
            address=data.get('address', ''),
            speed_kmh=data.get('speed_kmh', 0),
        )
        van.status = 'on_route'
        van.save()
        return JsonResponse({'status': 'ok', 'van': van.registration})
    except (KeyError, ValueError) as e:
        return JsonResponse({'status': 'error', 'detail': str(e)}, status=400)


def api_vans(request):
    vans = Van.objects.select_related('driver').all()
    data = []
    for van in vans:
        latest = van.locations.order_by('-timestamp').first()
        data.append({
            'id': van.pk,
            'registration': van.registration,
            'model': van.model,
            'status': van.status,
            'driver': van.driver.name if van.driver else None,
            'last_lat': float(latest.latitude) if latest else None,
            'last_lng': float(latest.longitude) if latest else None,
            'last_seen': latest.timestamp.isoformat() if latest else None,
        })
    return JsonResponse({'vans': data})
