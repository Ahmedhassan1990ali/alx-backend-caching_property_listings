# ALX Backend Caching - Property Listings

A Django project with Dockerized PostgreSQL and Redis for property listings with caching capabilities.

## Features

- Django 4.2.7
- PostgreSQL database (Dockerized)
- Redis cache backend (Dockerized)
- Property listing management
- API endpoints with caching

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd alx-backend-caching_property_listings
   ```

2. **Run setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Docker Services

- **PostgreSQL**: `localhost:5432`
  - Database: `property_listings_db`
  - User: `alx_user`
  - Password: `alx_password`

- **Redis**: `localhost:6379`

## API Endpoints

- `GET /api/properties/` - Get all properties (cached)
- `GET /api/clear-cache/` - Clear Redis cache

## Admin Interface

- URL: `/admin/`
- Default superuser: `admin` / `adminpassword`

## Project Structure

```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── settings.py          # Django settings with DB and cache config
│   ├── urls.py             # Main URL configuration
│   └── ...
├── properties/
│   ├── models.py           # Property model
│   ├── views.py           # API views with caching
│   ├── urls.py           # App URL routes
│   └── ...
├── docker-compose.yml     # Docker services configuration
├── requirements.txt       # Python dependencies
└── README.md
```

## Usage

1. Access the admin panel at `http://localhost:8000/admin/` to add properties
2. Test the API endpoint at `http://localhost:8000/api/properties/`
3. The first request will hit the database, subsequent requests will be served from Redis cache
