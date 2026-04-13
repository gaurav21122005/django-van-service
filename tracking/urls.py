from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Vans
    path('vans/', views.van_list, name='van_list'),
    path('vans/add/', views.van_create, name='van_create'),
    path('vans/<int:pk>/', views.van_detail, name='van_detail'),
    path('vans/<int:pk>/edit/', views.van_edit, name='van_edit'),
    path('vans/<int:pk>/delete/', views.van_delete, name='van_delete'),

    # Drivers
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.driver_create, name='driver_create'),
    path('drivers/<int:pk>/', views.driver_detail, name='driver_detail'),
    path('drivers/<int:pk>/edit/', views.driver_edit, name='driver_edit'),
    path('drivers/<int:pk>/delete/', views.driver_delete, name='driver_delete'),

    # Trips
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/add/', views.trip_create, name='trip_create'),
    path('trips/<int:pk>/edit/', views.trip_edit, name='trip_edit'),
    path('trips/<int:pk>/delete/', views.trip_delete, name='trip_delete'),

    # API
    path('api/vans/', views.api_vans, name='api_vans'),
    path('api/vans/<int:van_pk>/location/', views.update_location, name='update_location'),
]
