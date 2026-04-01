# FishDex Backend API

FishDex Backend is a Django and Django REST Framework application that exposes a JWT-secured API for player progression, fish catalog access, inventory management, capture flows, and store operations. The codebase follows a domain-oriented structure with clear separation between API, application services, and persistence concerns.

FishDex models a fishing game loop in which each user owns a `Fisher`, moves between zones, spawns fish based on the current habitat, attempts captures using rods and bait, stores catches, and sells them to earn coins.

The application is deployed to production on Render directly from GitHub. The public frontend is available at [fishdex-frontend.onrender.com](https://fishdex-frontend.onrender.com).

## Architecture Overview

```text
[ Frontend ] -> [ Django + DRF API ] -> [ PostgreSQL ]
                    |
                    +-> OpenAPI / Swagger / ReDoc
```

Architectural characteristics present in the current implementation:

- Client-agnostic backend.
- Stateless authentication with JWT via `SimpleJWT`.
- OpenAPI schema generation with `drf-spectacular`.
- Domain-based application boundaries.
- Business logic implemented outside views.
- Layered organization inside each domain:
  - `api/`: views and serializers.
  - `domain/`: application services and domain rules.
  - `infrastructure/`: repositories and database access.

## Implemented Domains

The active Django apps in the project are:

- `accounts`: registration, login flow integration, and refresh-token logout.
- `fishers`: player profile, nickname updates, coin balance, and zone changes.
- `fish`: global fish catalog.
- `inventory`: captured fish and purchased items owned by the player.
- `store`: rod and bait listing plus purchasing logic.
- `capture`: fish spawning and capture resolution.
- `core`: shared exceptions, global exception handling, and supporting utilities.

Important note: the previous README referenced `dex` and `zones` as standalone modules. In the current codebase, those modules do not exist as separate apps. Zone management is currently handled under `fishers`, and there is no dedicated `dex` app implemented at this stage.

## Actual Data Model

### `Fisher`

Player profile associated one-to-one with Django's user model.

- `user`
- `nickname`
- `level`
- `experience`
- `coins`
- `current_zone`

### `Fish`

Global catalog of fish species available in the game.

- `name`
- `fish_id`
- `description`
- `habitat`: `RIVER | LAKE | SEA | OCEAN`
- `rarity`: `COMMON | RARE | LEGENDARY`
- `base_weight`
- `base_price`

### `FisherFish`

Individual captured fish stored in the player's inventory.

- `fisher`
- `fish`
- `caught_at`
- `description`
- `weight`
- `length`

### `ItemStore`

Store catalog item.

- `name`
- `code`
- `type`: `ROD | BAIT`
- `quantity`
- `price`
- `effect`

### `FisherItem`

Player-owned store item entry.

- `fisher`
- `item`
- `is_equipped`
- `acquired_at`
- `quantity`

## Gameplay Flow Supported by the API

1. A user registers through `accounts`.
2. Registration automatically creates the associated `Fisher`.
3. The player retrieves profile data and coin balance.
4. The player purchases rods and bait from the store.
5. The player can switch zones if enough coins are available.
6. `capture/spawned-fish/` generates a fish based on the current zone and rarity weights.
7. `capture/capture/` resolves the capture attempt using equipment effect values versus fish weight.
8. On success, a `FisherFish` record is created in the inventory.
9. The player can list catches, annotate them, and sell them for coins.

## API Endpoints

Default local base URL: `http://localhost:8000`

Except for `register`, `login`, `refresh`, and the root healthcheck, all endpoints require:

```http
Authorization: Bearer <access_token>
```

### Healthcheck

- `GET /`
  - Response:
  ```json
  {
    "status": "ok"
  }
  ```

### Authentication

- `POST /api/auth/register/`
  - Request body:
  ```json
  {
    "email": "player@example.com",
    "password": "secret123"
  }
  ```
  - Creates both the Django user and the associated `Fisher` profile.

- `POST /api/auth/login/`
  - Standard `TokenObtainPairView` endpoint.
  - Returns `access` and `refresh` tokens.

- `POST /api/auth/refresh/`
  - Request body:
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```
  - Rotates the refresh token and returns a new access token.

- `POST /api/auth/logout/`
  - Request body:
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```
  - Blacklists the provided refresh token.

### Fisher

- `GET /api/fishers/me/`
  - Returns:
    - `nickname`
    - `level`
    - `coins`
    - `current_zone`

- `PATCH /api/fishers/nickname/`
  - Request body:
  ```json
  {
    "nickname": "angler_01"
  }
  ```
  - Accepts only letters, numbers, and underscores.

- `PATCH /api/fishers/change-zone/`
  - Request body:
  ```json
  {
    "new_zone": "LAKE"
  }
  ```
  - Zones currently supported by the service logic:
    - `RIVER`
    - `LAKE`
    - `OCEAN`
  - Zone change costs currently implemented:
    - `RIVER`: 100 coins
    - `LAKE`: 200 coins
    - `OCEAN`: 500 coins

### Fish Catalog

- `GET /api/fish/get-list-fishes/`
  - Returns the complete fish catalog.

- `GET /api/fish/get-fish-details/?fish_id=1`
  - Returns the details of a single fish species.

### Inventory

- `GET /api/inventory/items/`
  - Returns the player's store-item inventory:
    - `item_code`
    - `item_name`
    - `quantity`

- `GET /api/inventory/fishes/`
  - Returns the player's captured-fish inventory:
    - `pk`
    - `fish_id`
    - `fish_name`
    - `price`
    - `weight`
    - `caught_at`
    - `rarity`

- `POST /api/inventory/fish-sell/`
  - Request body:
  ```json
  {
    "pk": 10,
    "fish_id": 3,
    "total_weight": "1.25"
  }
  ```
  - Sale value is computed from fish base price and weight.
  - In the current implementation, the sale removes the entire captured-fish record and credits coins to the `Fisher`.

- `PATCH /api/inventory/fisher-fish-description/`
  - Request body:
  ```json
  {
    "pk": 10,
    "description": "Caught at sunset near the reeds"
  }
  ```
  - Updates the description associated with a captured fish entry.

### Capture

- `GET /api/capture/spawned-fish/`
  - Spawns a fish according to the player's current zone.
  - Current rarity weights:
    - `COMMON`: 70
    - `RARE`: 25
    - `LEGENDARY`: 5

- `POST /api/capture/capture/`
  - Request body:
  ```json
  {
    "used_rod": "ROD_BASIC",
    "used_bait": "BAIT_BASIC",
    "fish_id": 1,
    "fish_weight": 1.45,
    "fish_length": 35.0
  }
  ```
  - `used_bait` may also be an empty string (`""`).
  - In the current logic, both bait and rod quantity are decremented even when the capture attempt fails.

### Store

- `GET /api/store/get-rod-store-list/`
  - Returns the available rods in the store.

- `GET /api/store/get-bait-store-list/`
  - Returns the available bait in the store.

- `PUT /api/store/buy-item/`
  - Request body:
  ```json
  {
    "item_code": "ROD_BASIC",
    "quantity": 1
  }
  ```
  - Deducts coins and creates or increments the corresponding `FisherItem`.

## API Documentation

`drf-spectacular` documentation endpoints:

- `GET /api/schema/`
- `GET /api/docs/`
- `GET /api/redocs/`

## Authentication and Security

- JWT-based authentication.
- Access token lifetime: 15 minutes.
- Refresh token lifetime: 6 days.
- Refresh token rotation enabled.
- Refresh token blacklist enabled on logout.

## Environment and Execution

### Requirements

- Python 3.11
- Docker and Docker Compose
- PostgreSQL 16 when running outside Docker

### Run with Docker

```bash
docker compose -f docker-compose.dev.yml up --build
```

Defined services:

- `fishdex-backend`
- `fishdex-postgres-db`

The API is exposed at `http://localhost:8000`.

### Configuration

The project uses `DJANGO_ENV` to load the corresponding `.env.<environment>` file automatically.

Examples:

- `DJANGO_ENV=development` -> `.env.development`
- `DJANGO_ENV=production` -> `.env.production`

In development, if PostgreSQL credentials are not available, the project can fall back to SQLite. In production, it is configured to support `DATABASE_URL` and Render deployment.

### Container Startup Flow

`entrypoint.sh` performs the following steps:

1. `migrate`
2. `create_superuser_if_not_exists`
3. `collectstatic` in production
4. Start with `runserver` in development or `gunicorn` in production

## Testing

The repository includes test coverage for:

- API endpoints
- application services
- repositories
- serializers

Test suites are present under:

- `accounts/tests`
- `fishers/tests`
- `fish/tests`
- `inventory/tests`
- `capture/tests`

I could not execute the test suite in the current workspace session because `pytest` is not installed in this environment.

## Tech Stack

- Python 3.11
- Django 5.0.6
- Django REST Framework 3.15.2
- SimpleJWT
- drf-spectacular
- PostgreSQL
- Docker
- Gunicorn
- WhiteNoise
- pytest / pytest-django / pytest-cov
- factory_boy

## Current Status

The backend already provides a functional base for authentication, player profile management, fish spawning, capture resolution, inventory handling, and store operations. At the same time, the codebase is still evolving: several endpoints remain strongly use-case-oriented in their naming, and this README is intentionally aligned with the current implementation rather than with an aspirational future structure.
