# VanService — Django Van Tracking System

A full van fleet tracking web application built with Django and SQLite.

## Features

- **Dashboard** — fleet overview with live status, recent trips, and location pings
- **Vans** — register, edit, and delete vans; view location history and trip history per van
- **Drivers** — manage drivers and their assigned vans
- **Trips** — schedule and track trips with origin, destination, status, and distance
- **Location API** — REST endpoint to receive GPS pings from vans
- **Django Admin** — full admin panel for all models

## Quick Start

### 1. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply migrations (creates db.sqlite3)

```bash
python manage.py migrate
```

### 4. Create a superuser (for /admin access)

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 — the dashboard loads immediately.

---

## Project Structure

```
vanservice/
├── manage.py
├── requirements.txt
├── db.sqlite3               # created after migrate
├── vanservice/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tracking/                # main app
    ├── models.py            # Van, Driver, Location, Trip
    ├── views.py             # CRUD + JSON API views
    ├── forms.py             # ModelForms
    ├── admin.py             # Admin registrations
    ├── urls.py              # URL routing
    ├── migrations/
    └── templates/tracking/
        ├── base.html
        ├── dashboard.html
        ├── van_list.html
        ├── van_detail.html
        ├── van_form.html
        ├── driver_list.html
        ├── driver_detail.html
        ├── driver_form.html
        ├── trip_list.html
        ├── trip_form.html
        └── confirm_delete.html
```

---

## Models

| Model | Key fields |
|-------|-----------|
| `Van` | registration, model, capacity_kg, status, driver (FK), mileage_km |
| `Driver` | name, license_number, phone, email, is_active |
| `Location` | van (FK), latitude, longitude, address, speed_kmh, timestamp |
| `Trip` | van (FK), driver (FK), origin, destination, status, scheduled_departure, distance_km |

---

## API Endpoints

### GET `/api/vans/`
Returns JSON list of all vans with their latest location.

```json
{
  "vans": [
    {
      "id": 1,
      "registration": "MH12AB1234",
      "model": "Tata Ace",
      "status": "on_route",
      "driver": "Ravi Kumar",
      "last_lat": 12.9716,
      "last_lng": 77.5946,
      "last_seen": "2026-04-13T10:30:00Z"
    }
  ]
}
```

### POST `/api/vans/<id>/location/`
Push a GPS ping for a van. Automatically sets van status to `on_route`.

**Request body:**
```json
{
  "latitude": 12.9716,
  "longitude": 77.5946,
  "address": "Bengaluru, Karnataka",
  "speed_kmh": 45.5
}
```

**Response:**
```json
{"status": "ok", "van": "MH12AB1234"}
```

---

## Van Status Values

| Value | Meaning |
|-------|---------|
| `available` | Ready to be assigned |
| `on_route` | Currently on a trip |
| `maintenance` | Under service/repair |
| `inactive` | Not in use |

## Trip Status Values

| Value | Meaning |
|-------|---------|
| `scheduled` | Planned, not started |
| `in_progress` | Currently running |
| `completed` | Finished |
| `cancelled` | Cancelled |

---

## Notes

- The SQLite database file (`db.sqlite3`) is created locally after running `migrate`.
- For production, change `SECRET_KEY` in `settings.py` and set `DEBUG = False`.
- To switch to PostgreSQL, update the `DATABASES` block in `settings.py`.
