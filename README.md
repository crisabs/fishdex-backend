# FishDex Backend API

Backend desarrollado con **Django y Django REST Framework**, orientado al diseño de APIs claras, mantenibles y bien estructuradas. El proyecto aplica una arquitectura API-first, separación por dominios, autenticación JWT, documentación OpenAPI y entorno dockerizado.

FishDex modela un sistema de juego donde cada usuario controla un *Fisher* (pescador), explora zonas, captura peces, gestiona inventario, compra herramientas y mantiene su propia FishDex.

---

## Arquitectura

Arquitectura desacoplada basada en API:

```
[ Frontend (Vue) ]  ->  [ Django + DRF API ]  ->  [ PostgreSQL ]
                            |
                            +-> OpenAPI / Swagger
```

Principios aplicados:

* Backend independiente del cliente
* Contrato de API explícito (OpenAPI)
* Autenticación stateless con JWT
* Separación por dominios funcionales
* Lógica de negocio fuera de las views

---

## Dominio y modelo de datos

El dominio gira en torno a la progresión del Fisher y sus interacciones:

* Cada **User** tiene un único **Fisher**
* El Fisher acumula nivel, experiencia y monedas
* Los peces se capturan de forma individual
* Cada captura tiene atributos propios (peso, memoria, fecha)
* La FishDex resume especies capturadas

### Modelos principales

**User**
Autenticación por email.

**Fisher**
Perfil del jugador.

* user (OneToOne)
* nickname
* level, experience, coins
* current_zone

**Fish**
Catálogo global de especies.

* name, description
* habitat (RIVER | LAKE | SEA | OCEAN)
* rarity (COMMON | RARE | LEGENDARY)
* base_weight, base_price

**InventoryItem**
Captura individual.

* fisher, fish
* weight
* memory
* is_sold
* caught_at

**Item**
Objetos de tienda.

* name
* type (ROD | BAIT)
* price
* effect

**Zone**
Zonas del mundo.

* name
* min_level

---

## Organización por apps

Las apps representan dominios y casos de uso, no pantallas ni CRUD genéricos.

* **accounts**: autenticación y tokens
* **fishers**: perfil y progresión del jugador
* **fish**: catálogo de especies
* **inventory**: capturas individuales
* **dex**: resumen agregado por especie
* **store**: compra y venta
* **zones**: gestión de zonas
* **capture**: lógica de aparición y captura

---

## Endpoints principales

**Auth**

* POST `/api/auth/register/`
* POST `/api/auth/login/`
* POST `/api/auth/logout/`
* POST `/api/auth/refresh/`

**Fisher**

* GET `/api/fisher/me/`
* PATCH `/api/fisher/nickname/`

**Inventario y juego**

* GET `/api/inventory/`
* POST `/api/capture/`
* POST `/api/inventory/{id}/sell/`
* GET `/api/dex/`

**Store y zonas**

* GET `/api/store/items/`
* POST `/api/store/buy/`
* GET `/api/zones/`
* POST `/api/zones/change/`

---

## API y documentación

* API REST con Django REST Framework
* Documentación OpenAPI generada con **drf-spectacular**
* Swagger UI para exploración y pruebas manuales

---

## Testing

Testing automatizado con **pytest**:

* modelos
* serializers
* endpoints
* lógica de dominio

Permite refactorización segura y control de regresiones.

---

## Docker y entorno

Proyecto completamente dockerizado.

Servicios:

* backend (Django + Gunicorn)
* database (PostgreSQL)

Incluye configuración de **Dev Container** para desarrollo consistente.

---

## Stack tecnológico

* Python
* Django 5.0.6
* Django REST Framework 3.15.2
* SimpleJWT
* drf-spectacular
* PostgreSQL
* Docker / Docker Compose
* pytest, flake8, black

---

## Estado del proyecto

Proyecto en desarrollo activo. La base funcional y arquitectónica está definida y operativa, y el trabajo actual se centra en completar funcionalidades, refinar la lógica de dominio y consolidar el conjunto de endpoints manteniendo claridad, coherencia y mantenibilidad.
