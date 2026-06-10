# Asset Price Alert API

Backend API for tracking asset prices and creating threshold-based alerts.

This project demonstrates a production-style Python backend with authentication, PostgreSQL persistence, Alembic migrations, Redis-backed background jobs, price history tracking and alert generation.

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Redis
* RQ
* Docker Compose
* Pytest
* JWT authentication
* bcrypt password hashing

## Features

* User registration and login
* JWT-based authentication
* Protected API endpoints
* Tracked asset management
* Manual price checks
* Price history persistence
* Threshold-based alert generation
* Alert listing and detail endpoints
* Redis-backed background jobs with RQ
* Separate worker process for background price checks
* PostgreSQL database migrations with Alembic
* Docker Compose setup for PostgreSQL and Redis
* Automated tests with Pytest

## Project Structure

```text
asset-price-alert-api/
├── app/
│   ├── alerts/
│   │   └── router.py
│   ├── assets/
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   └── service.py
│   ├── jobs/
│   │   └── price_checks.py
│   ├── pricing/
│   │   ├── provider.py
│   │   └── service.py
│   ├── users/
│   │   └── models.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── queue.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
├── run_api.py
├── worker.py
└── README.md
```

## Environment Variables

Create a `.env` file based on `.env.example`.

```env
APP_ENV=development

DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/asset_price_alert
REDIS_URL=redis://localhost:6379/0

JWT_SECRET_KEY=change-this-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Run Locally

Start PostgreSQL and Redis:

```bash
docker compose up -d
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Apply database migrations:

```bash
python -m alembic -c alembic.ini upgrade head
```

Run the API:

```bash
python run_api.py
```

Run the background worker in a second terminal:

```bash
python worker.py
```

API documentation:

```text
http://127.0.0.1:8010/docs
```

## API Endpoints

### System

```text
GET /health
GET /db-health
GET /redis-health
GET /db-tables
```

### Authentication

```text
POST /auth/register
POST /auth/login
GET /auth/me
```

### Tracked Assets

```text
POST /tracked-assets
GET /tracked-assets
GET /tracked-assets/{asset_id}
DELETE /tracked-assets/{asset_id}
POST /tracked-assets/{asset_id}/check-now
POST /tracked-assets/{asset_id}/enqueue-check
GET /tracked-assets/{asset_id}/price-history
```

### Alerts

```text
GET /alerts
GET /alerts/{alert_id}
```

## Example Flow

Register a user:

```json
{
  "email": "test@example.com",
  "password": "strongpassword",
  "full_name": "Test User"
}
```

Login and copy the returned access token:

```json
{
  "email": "test@example.com",
  "password": "strongpassword"
}
```

Authorize requests with:

```text
Bearer <access_token>
```

Create a tracked asset:

```json
{
  "symbol": "BTC",
  "name": "Bitcoin",
  "target_price": 70000,
  "condition": "below",
  "currency": "USD"
}
```

Run a manual price check:

```text
POST /tracked-assets/{asset_id}/check-now
```

Or enqueue a background price check:

```text
POST /tracked-assets/{asset_id}/enqueue-check
```

The worker processes the queued job, saves a price check and creates an alert if the threshold condition is met.

## Mock Price Provider

The project currently uses a mock price provider for stable local development and deterministic tests.

Example mock prices:

```text
BTC  -> 68000.00 USD
ETH  -> 3500.00 USD
SOL  -> 150.00 USD
AAPL -> 195.00 USD
TSLA -> 250.00 USD
```

Example alert condition:

```text
BTC current price: 68000.00
Target price:      70000.00
Condition:         below

Result: alert triggered
```

## Background Jobs

The project uses Redis and RQ for background processing.

The API endpoint:

```text
POST /tracked-assets/{asset_id}/enqueue-check
```

adds a job to the `price-checks` queue.

The worker:

```bash
python worker.py
```

processes the job and runs the price check outside the HTTP request-response cycle.

On Windows, the project uses RQ `SimpleWorker` for local development because the default RQ worker uses process forking, which is not available on Windows.

## Tests

Run tests:

```bash
python -m pytest
```

The test suite covers:

* health check endpoint
* user registration
* user login
* current user endpoint
* tracked asset creation
* tracked asset listing
* manual price checks
* price history
* alert generation
* alert listing
* enqueue price check endpoint

## Development Notes

This project is designed as a portfolio backend project. It focuses on practical backend concepts:

* API design
* authentication
* relational database modeling
* migrations
* background jobs
* queue-based processing
* service-layer structure
* testable business logic
* Docker-based local infrastructure

## Future Improvements

* Add GitHub Actions CI
* Add real external price provider integration
* Add scheduled recurring price checks
* Add notification delivery via email or Telegram
* Add pagination for tracked assets and alerts
* Add rate limiting
* Add Dockerfile for the API and worker
* Add production deployment configuration
