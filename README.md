# FishDex Backend API

Backend developed with **Django y Django REST Framework**, focused on designing clear, maintainable, and well-structured APIs. The project follows an API-first architecture, domain-based separation, JWT authentication, OpenAPI documentation, and a fully dockerized environment.

FishDex models a game system where each user controls a *Fisher* (pescador), explores zones, catches fish, manages inventory, buys tools, and maintains their own FishDex.

---

## Architecture

Decoupled API-based architecture:

```
[ Frontend (Vue) ]  ->  [ Django + DRF API ]  ->  [ PostgreSQL ]
                            |
                            +-> OpenAPI / Swagger
```

Applied principles:

* Backend independent from the client
* Explicit API contract (OpenAPI)
* Stateless authentication with JWT
* Functional domain separation
* Business logic outside the views

---

## Domain and Data Model

The domain revolves around the Fisher’s progression and interactions:

* Each **User** has a single **Fisher**
* The Fisher gains levels, experience, and coins
* Fish are caught individually
* Each catch has its own attributes (weight, memory, date)
* The FishDex summarizes captured species

### Core Models

**User**
Email-based authentication.

**Fisher**
Player profile.

* user (OneToOne)
* nickname
* level, experience, coins
* current_zone

**Fish**
Global species catalog.

* name, description
* habitat (RIVER | LAKE | SEA | OCEAN)
* rarity (COMMON | RARE | LEGENDARY)
* base_weight, base_price

**InventoryItem**
Individual catch.

* fisher, fish
* weight
* memory
* is_sold
* caught_at

**Item**
Store items.

* name
* type (ROD | BAIT)
* price
* effect

**Zone**
World zones.

* name
* min_level

---

## App Organization

Apps represent domains and use cases, not screens or generic CRUD.

* **accounts**: authentication and tokens
* **fishers**: player profile and progression
* **fish**: species catalog
* **inventory**: individual catches
* **dex**: aggregated summary by species
* **store**: buying and selling
* **zones**: zone management
* **capture**: spawning and capture logic

---

## Main Endpoints

**Auth**

* POST `/api/auth/register/`
* POST `/api/auth/login/`
* POST `/api/auth/logout/`
* POST `/api/auth/refresh/`

**Fisher**

* GET `/api/fisher/me/`
* PATCH `/api/fisher/nickname/`

**Inventory and Gameplay**

* GET `/api/inventory/`
* POST `/api/capture/`
* POST `/api/inventory/{id}/sell/`
* GET `/api/dex/`

**Store and Zones**

* GET `/api/store/items/`
* POST `/api/store/buy/`
* GET `/api/zones/`
* POST `/api/zones/change/`

---

## API and Documentation

* REST API built with Django REST Framework
* OpenAPI documentation generated with **drf-spectacular**
* Swagger UI for exploration and manual testing

---

## Testing

Automated testing with **pytest**:

* models
* serializers
* endpoints
* domain logic

Enables safe refactoring and regression control.

---

## Docker and Environment

Fully dockerized project.

Services:

* backend (Django + Gunicorn)
* database (PostgreSQL)

Includes **Dev Container** configuration for consistent development.

---

## Tech Stack

* Python
* Django 5.0.6
* Django REST Framework 3.15.2
* SimpleJWT
* drf-spectacular
* PostgreSQL
* Docker / Docker Compose
* pytest, flake8, black

---

## Project Status

Project under active development. The functional and architectural foundation is defined and operational. Current work focuses on completing features, refining domain logic, and consolidating the endpoint set while maintaining clarity, consistency, and maintainability.
