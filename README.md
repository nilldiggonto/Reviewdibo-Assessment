# ReviewDibo - Product Review Platform (Assessment)

A full-stack product review platform built with **Next.js** (frontend) and **FastAPI** (backend), using **PostgreSQL** as the database.

## Live Demo

| | URL |
|--|-----|
| **Frontend** | [https://reviewdibo-assessment-frontend.vercel.app](https://reviewdibo-assessment-frontend.vercel.app) |
| **Backend API** | [https://reviewdibo-assessment-api.onrender.com](https://reviewdibo-assessment-api.onrender.com) |
| **API Docs (Swagger)** | [https://reviewdibo-assessment-api.onrender.com/docs](https://reviewdibo-assessment-api.onrender.com/docs) |
| **GitHub Repo** | [https://github.com/nilldiggonto/Reviewdibo-Assessment](https://github.com/nilldiggonto/Reviewdibo-Assessment) |

> **Note:** The backend is hosted on Render's free tier. If the API is unresponsive, see [Troubleshooting](#troubleshooting) below.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.12, SQLAlchemy (async) |
| Database | PostgreSQL with asyncpg driver |
| Package Manager | uv (Python), npm (Node) |
| Deployment | Vercel (frontend), Render (backend + database) |

---

## Project Structure

```
reviewDibo/
├── backend/                        # FastAPI backend
│   ├── app/
│   │   ├── core/                   # Configuration & database setup
│   │   │   ├── config.py           # Pydantic settings (reads .env)
│   │   │   └── database.py         # Async SQLAlchemy engine & session
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── base.py             # DeclarativeBase
│   │   │   ├── user.py             # User model
│   │   │   ├── product.py          # Product model
│   │   │   └── review.py           # Review model (FK → product, user)
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   │   ├── user.py             # UserCreate, UserOut
│   │   │   ├── product.py          # ProductListOut, ProductDetailOut, PaginatedResponse
│   │   │   └── review.py           # ReviewCreate, ReviewUpdate, ReviewOut
│   │   ├── repositories/           # Data access layer (DB queries)
│   │   │   ├── user_repository.py
│   │   │   ├── product_repository.py
│   │   │   └── review_repository.py
│   │   ├── services/               # Business logic layer
│   │   │   ├── user_service.py
│   │   │   ├── product_service.py
│   │   │   └── review_service.py
│   │   ├── routers/                # API endpoint definitions
│   │   │   ├── users.py            # /api/users
│   │   │   ├── products.py         # /api/products (paginated)
│   │   │   └── reviews.py          # /api/reviews
│   │   ├── tests/                  # Unit & integration tests
│   │   │   ├── conftest.py         # Async test fixtures (test DB, client)
│   │   │   ├── test_health.py
│   │   │   ├── test_products.py
│   │   │   ├── test_reviews.py
│   │   │   └── test_users.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   └── seed.py                 # Database seed script (30 products)
│   ├── Dockerfile                  # Docker build for Render deployment
│   ├── start.sh                    # Entrypoint: seed DB + start server
│   ├── .env.example                # Environment template
│   └── pyproject.toml              # Python project config (uv)
│
├── frontend/                       # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx              # Root layout with header/footer
│   │   ├── page.tsx                # Home page (paginated product grid)
│   │   ├── globals.css             # Global styles (Tailwind)
│   │   └── products/
│   │       └── [id]/
│   │           └── page.tsx        # Product detail page + reviews
│   ├── components/
│   │   ├── ProductCard.tsx         # Product card for home grid
│   │   ├── ReviewCard.tsx          # Single review display
│   │   ├── ReviewForm.tsx          # Review submission form
│   │   └── StarRating.tsx          # Star rating (display + interactive)
│   ├── lib/
│   │   ├── api.ts                  # API client functions (fetch)
│   │   └── types.ts                # TypeScript interfaces
│   ├── Dockerfile                  # Docker build (optional, for self-hosting)
│   ├── .env.example                # Frontend env template
│   └── .nvmrc                      # Node version (24)
│
├── .nvmrc                          # Node version (root)
├── .python-version                 # Python version (3.12)
└── .gitignore
```

---

## Architecture

### Backend Layers

The backend follows a **layered architecture** pattern:

```
Request → Router → Service → Repository → Database
```

| Layer | Folder | Responsibility |
|-------|--------|---------------|
| **Routers** | `app/routers/` | HTTP endpoints, request/response handling |
| **Services** | `app/services/` | Business logic, validation, error handling |
| **Repositories** | `app/repositories/` | Database queries (only layer that touches DB) |
| **Models** | `app/models/` | SQLAlchemy ORM table definitions |
| **Schemas** | `app/schemas/` | Pydantic models for validation & serialization |
| **Core** | `app/core/` | Config (reads `.env`), async DB engine/session |

Dependencies are injected via FastAPI's `Depends()` — each request gets its own service/repository chain wired to a fresh DB session.

### Database Schema

```
users                products              reviews
─────────────        ─────────────         ─────────────
id (PK)              id (PK)               id (PK)
name                 title                 product_id (FK → products)
email (unique)       description           user_id (FK → users)
created_at           image_url             rating (1-5)
                     created_at            comment
                                           created_at
```

Tables are auto-created on application startup via `Base.metadata.create_all`.

### API Endpoints

| Method | Path | Description | Query Params |
|--------|------|-------------|-------------|
| GET | `/api/health` | Health check | — |
| GET | `/api/products` | List products (paginated) | `page` (default 1), `page_size` (default 9, max 100) |
| GET | `/api/products/{id}` | Product detail with all reviews | — |
| POST | `/api/reviews` | Create a review | — |
| PUT | `/api/reviews/{id}` | Update a review | — |
| DELETE | `/api/reviews/{id}` | Delete a review | — |
| POST | `/api/users` | Create a user | — |
| GET | `/api/users` | List all users | — |

Full interactive docs available at [`/docs`](https://reviewdibo-assessment-api.onrender.com/docs) (Swagger UI).

### Frontend Pages

| Route | Description |
|-------|-------------|
| `/` | Paginated product grid with cards showing image, title, average rating, and review count |
| `/products/[id]` | Product detail with full description, all reviews, and a review submission form |

---

## Local Setup Instructions

> Tested on **Ubuntu 24.04 LTS**. Should work on any Debian-based Linux. macOS users may need to adjust PostgreSQL commands.

### Step 1: Install Prerequisites

**Python 3.12**

```bash
# Check if you already have it
python3.12 --version

# If not, install via pyenv (recommended)
curl https://pyenv.run | bash
# Restart your terminal, then:
pyenv install 3.12
pyenv global 3.12
```

**Node.js 24**

```bash
# Check if you already have it
node --version

# If not, install via nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
# Restart your terminal, then:
nvm install 24
nvm use 24
```

**uv (Python package manager)**

```bash
# Check if you already have it
uv --version

# If not, install it
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart your terminal or run: source ~/.bashrc
```

**PostgreSQL**

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# If not installed:
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/nilldiggonto/Reviewdibo-Assessment.git
cd Reviewdibo-Assessment
```

### Step 3: Set Up the Database

```bash
# Create the main database (used by the app)
sudo -u postgres psql -c "CREATE DATABASE reviewdibo;"

# Create the test database (used by pytest)
sudo -u postgres psql -c "CREATE DATABASE reviewdibo_test;"

# Set a password for the postgres user (the .env.example uses "postgres")
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

You can verify by connecting:
```bash
sudo -u postgres psql -c "\l" | grep reviewdibo
# Should show both "reviewdibo" and "reviewdibo_test"
```

### Step 4: Set Up the Backend

```bash
cd backend

# Copy the environment template
cp .env.example .env

# If your PostgreSQL username/password differ from "postgres"/"postgres",
# edit .env and update the DATABASE_URL accordingly.

# Install all Python dependencies
uv sync

# Seed the database with sample data
# This populates 30 products, 10 users, and 112 reviews so you have
# data to browse immediately. It's safe to run multiple times —
# it skips if data already exists.
uv run python -m app.seed
```

You should see:
```
Seeded 10 users, 30 products, and 112 reviews.
```

**Start the backend server:**

```bash
# Development mode (auto-reloads on code changes)
uv run fastapi dev --port 8000
```

Verify it's working — open these in your browser:
- **Health check:** http://localhost:8000/api/health → should return `{"status":"ok"}`
- **Products API:** http://localhost:8000/api/products → should return paginated product list
- **Swagger Docs:** http://localhost:8000/docs → interactive API documentation

### Step 5: Set Up the Frontend

Open a **new terminal** (keep the backend running in the first one):

```bash
cd frontend

# Copy the environment template
cp .env.example .env.local

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

Open http://localhost:3000 in your browser. You should see:
- A grid of product cards with images, ratings, and review counts
- Pagination controls at the bottom (30 products, 9 per page = 4 pages)
- Clicking a product card opens its detail page with reviews and a review form

### Step 6: Run the Tests

Open a **new terminal**:

```bash
cd backend

# Run all 15 tests against the reviewdibo_test database
uv run pytest app/tests/ -v
```

You should see:
```
app/tests/test_health.py::test_health_check PASSED
app/tests/test_products.py::test_get_products_empty PASSED
app/tests/test_products.py::test_get_products_with_data PASSED
app/tests/test_products.py::test_get_products_pagination PASSED
app/tests/test_products.py::test_get_product_detail PASSED
app/tests/test_products.py::test_get_product_not_found PASSED
app/tests/test_reviews.py::test_create_review PASSED
app/tests/test_reviews.py::test_create_review_invalid_rating PASSED
app/tests/test_reviews.py::test_create_review_product_not_found PASSED
app/tests/test_reviews.py::test_update_review PASSED
app/tests/test_reviews.py::test_delete_review PASSED
app/tests/test_reviews.py::test_delete_review_not_found PASSED
app/tests/test_users.py::test_create_user PASSED
app/tests/test_users.py::test_create_user_duplicate_email PASSED
app/tests/test_users.py::test_list_users PASSED

15 passed
```

**What the tests cover:**
- `test_health.py` — API health check endpoint
- `test_products.py` — Product listing, pagination, detail view, and 404 handling
- `test_reviews.py` — Create, update, delete reviews, rating validation (1-5), and foreign key checks
- `test_users.py` — User creation, duplicate email prevention, and listing

A **pre-commit hook** is configured — tests run automatically before every `git commit`. If any test fails, the commit is blocked.

### Step 7: About the Seed Script

The seed script (`backend/app/seed.py`) populates the database with realistic sample data:

| Data | Count | Details |
|------|-------|---------|
| Users | 10 | Names like "John Doe", "Jane Smith", etc. |
| Products | 30 | Tech products with descriptions and Unsplash images |
| Reviews | 112 | Random 1-6 reviews per product, ratings 2-5 |

It's **idempotent** — running it again won't create duplicates. If you want to reset and re-seed:

```bash
cd backend
sudo -u postgres psql -c "DROP DATABASE reviewdibo;"
sudo -u postgres psql -c "CREATE DATABASE reviewdibo;"
uv run python -m app.seed
```

---

## Environment Variables

### Backend (`backend/.env`)

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/reviewdibo
```

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string using the `asyncpg` driver | `postgresql+asyncpg://user:pass@host:5432/dbname` |

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL (no trailing slash) | `http://localhost:8000` |

---

## Deployment

### Backend (Render)

The backend is deployed as a **Docker Web Service** on Render.

- **Runtime:** Docker (uses `backend/Dockerfile`)
- **Root Directory:** `backend`
- **Start Command:** `start.sh` (seeds DB on first run, then starts FastAPI)
- **Environment Variable:** `DATABASE_URL` set to Render's internal PostgreSQL URL with `postgresql+asyncpg://` prefix and `?ssl=require`

### Frontend (Vercel)

The frontend is deployed on **Vercel** with zero configuration.

- **Framework:** Next.js (auto-detected)
- **Root Directory:** `frontend`
- **Environment Variable:** `NEXT_PUBLIC_API_URL` set to the Render backend URL

---

## Troubleshooting

### API calls fail or frontend shows "Failed to load products"

**Render free tier cold starts:** Render spins down free-tier services after 15 minutes of inactivity. The first request after idle triggers a cold start that takes **30-60 seconds**. Simply wait and refresh the page.

To verify the backend is up, visit the health endpoint directly:
[https://reviewdibo-assessment-api.onrender.com/api/health](https://reviewdibo-assessment-api.onrender.com/api/health)

### CORS errors in browser console

The backend allows all origins (`allow_origins=["*"]`). If you see CORS errors, make sure `NEXT_PUBLIC_API_URL` does not have a trailing slash.

### Database connection issues (local)

- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Verify the `reviewdibo` database exists: `sudo -u postgres psql -l | grep reviewdibo`
- Check that your `.env` `DATABASE_URL` matches your local PostgreSQL credentials
- Make sure to use the `postgresql+asyncpg://` prefix (not `postgresql://`)

### Tests fail locally

- Ensure the test database exists: `sudo -u postgres psql -c "CREATE DATABASE reviewdibo_test;"`
- Run tests from the `backend/` directory: `cd backend && uv run pytest app/tests/ -v`
