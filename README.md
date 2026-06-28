# ReviewDibo - Product Review Platform

A full-stack product review platform built with **Next.js** (frontend) and **FastAPI** (backend), using **PostgreSQL** as the database.

---

## Project Structure

```
reviewDibo/
├── backend/                    # FastAPI backend (Python 3.12, uv)
│   ├── app/
│   │   ├── core/               # Configuration & database setup
│   │   │   ├── config.py       # Pydantic settings (reads .env)
│   │   │   └── database.py     # Async SQLAlchemy engine & session
│   │   ├── models/             # SQLAlchemy ORM models
│   │   │   ├── base.py         # DeclarativeBase
│   │   │   ├── user.py         # User model
│   │   │   ├── product.py      # Product model
│   │   │   └── review.py       # Review model (FK → product, user)
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   │   ├── user.py         # UserCreate, UserOut
│   │   │   ├── product.py      # ProductListOut, ProductDetailOut
│   │   │   └── review.py       # ReviewCreate, ReviewUpdate, ReviewOut
│   │   ├── repositories/       # Data access layer (DB queries)
│   │   │   ├── user_repository.py
│   │   │   ├── product_repository.py
│   │   │   └── review_repository.py
│   │   ├── services/           # Business logic layer
│   │   │   ├── user_service.py
│   │   │   ├── product_service.py
│   │   │   └── review_service.py
│   │   ├── routers/            # API endpoint definitions
│   │   │   ├── users.py        # /api/users
│   │   │   ├── products.py     # /api/products
│   │   │   └── reviews.py      # /api/reviews
│   │   ├── tests/              # Unit & integration tests
│   │   │   ├── conftest.py     # Async test fixtures (test DB, client)
│   │   │   ├── test_health.py
│   │   │   ├── test_products.py
│   │   │   ├── test_reviews.py
│   │   │   └── test_users.py
│   │   ├── main.py             # FastAPI app entry point
│   │   └── seed.py             # Database seed script
│   ├── .env                    # Environment variables (local)
│   ├── .env.example            # Environment template
│   └── pyproject.toml          # Python project config (uv)
│
├── frontend/                   # Next.js frontend (Node 24, TypeScript)
│   ├── app/
│   │   ├── layout.tsx          # Root layout with header/footer
│   │   ├── page.tsx            # Home page (product grid)
│   │   ├── globals.css         # Global styles (Tailwind)
│   │   └── products/
│   │       └── [id]/
│   │           └── page.tsx    # Product detail page + reviews
│   ├── components/
│   │   ├── ProductCard.tsx     # Product card for home grid
│   │   ├── ReviewCard.tsx      # Single review display
│   │   ├── ReviewForm.tsx      # Review submission form
│   │   └── StarRating.tsx      # Star rating (display + interactive)
│   ├── lib/
│   │   ├── api.ts              # API client functions (fetch)
│   │   └── types.ts            # TypeScript interfaces
│   ├── .env.local              # Frontend env vars
│   ├── .env.example            # Frontend env template
│   └── .nvmrc                  # Node version (24)
│
├── .nvmrc                      # Node version (root)
└── .python-version             # Python version (3.12)
```

---

## Architecture Overview

### Backend Layers

The backend follows a **layered architecture** pattern:

1. **Routers** (`app/routers/`) — Define API endpoints, handle HTTP request/response. Depend on services via FastAPI dependency injection.
2. **Services** (`app/services/`) — Business logic. Validate rules (e.g., product exists before review), raise HTTP exceptions. Depend on repositories.
3. **Repositories** (`app/repositories/`) — Data access. Execute SQLAlchemy queries, return models or dicts. Only layer that touches the DB.
4. **Models** (`app/models/`) — SQLAlchemy ORM models that map to PostgreSQL tables.
5. **Schemas** (`app/schemas/`) — Pydantic models for request validation and response serialization.
6. **Core** (`app/core/`) — Shared infrastructure: config (reads `.env`), async database engine/session.

### Database Schema

```
users              products            reviews
──────────         ──────────          ──────────
id (PK)            id (PK)             id (PK)
name               title               product_id (FK → products.id)
email (unique)     description         user_id (FK → users.id)
created_at         image_url           rating (1-5)
                   created_at          comment
                                       created_at
```

### API Endpoints

| Method | Path                  | Description                  |
|--------|-----------------------|------------------------------|
| GET    | `/api/health`         | Health check                 |
| GET    | `/api/products`       | List all products + avg rating |
| GET    | `/api/products/{id}`  | Product detail with reviews  |
| POST   | `/api/reviews`        | Create a new review          |
| PUT    | `/api/reviews/{id}`   | Update a review              |
| DELETE | `/api/reviews/{id}`   | Delete a review              |
| POST   | `/api/users`          | Create a user                |
| GET    | `/api/users`          | List all users               |

### Frontend Pages

| Route              | File                           | Description                                |
|--------------------|--------------------------------|--------------------------------------------|
| `/`                | `app/page.tsx`                 | Product grid with cards showing avg rating |
| `/products/[id]`   | `app/products/[id]/page.tsx`   | Product detail, review list, submit form   |

---

## Setup Instructions

### Prerequisites

- Python 3.12
- Node.js 24 (see `.nvmrc`)
- PostgreSQL 14+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### 1. Database Setup

```bash
# Create the main and test databases
sudo -u postgres psql -c "CREATE DATABASE reviewdibo;"
sudo -u postgres psql -c "CREATE DATABASE reviewdibo_test;"
```

### 2. Backend Setup

```bash
cd backend

# Copy environment variables
cp .env.example .env
# Edit .env if your PostgreSQL credentials differ

# Install dependencies
uv sync

# Tables are auto-created on first run, but you can seed sample data:
uv run python -m app.seed

# Start the backend server (development with auto-reload)
uv run fastapi dev --port 8000

# Or production mode
uv run fastapi run --port 8000
```

The API will be available at `http://localhost:8000`.  
Swagger docs: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Copy environment variables
cp .env.example .env.local

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### 4. Running Tests

```bash
cd backend

# Run all tests (uses reviewdibo_test database)
uv run pytest app/tests/ -v
```

---

## Key Design Decisions

- **Fully async**: The backend uses `asyncpg` + SQLAlchemy async for non-blocking DB queries.
- **Layered architecture**: Routers → Services → Repositories keeps concerns separated and testable.
- **Dependency injection**: FastAPI's `Depends()` wires up service instances per request.
- **Auto-migration**: Tables are created via `Base.metadata.create_all` on startup (no Alembic migrations needed for this scope).
- **Test isolation**: Each test gets a fresh database schema (create + drop per test) with its own async session.
- **User handling**: The review form uses get-or-create logic — if the email already exists, it reuses the existing user.

---

## Environment Variables

### Backend (`.env`)

| Variable       | Description                       | Default                                                  |
|----------------|-----------------------------------|----------------------------------------------------------|
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/reviewdibo` |

### Frontend (`.env.local`)

| Variable             | Description        | Default                  |
|----------------------|--------------------|--------------------------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |