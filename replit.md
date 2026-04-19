# Benkiz Bakers

Kenyan bakery website with a Django backend and a modern React frontend.

## Architecture

### Backend — Django (port 8000)
- Framework: Django 6 + Django REST Framework
- Database: SQLite (`db.sqlite3`)
- Static files: WhiteNoise
- Media files: `/media/` directory
- Key app: `main` (models, views, Django templates)
- API app: `benkizapi` (REST endpoints)

### Frontend — React + Vite (port 5000)
- Framework: React 19 + Vite 8
- Routing: React Router DOM v7
- HTTP: Axios
- Icons: Font Awesome 6 Free (`@fortawesome/fontawesome-free`)
- Theming: CSS variables — 3 built-in themes (light, dark, warm)
- Source: `frontend/src/`

## Workflows

| Workflow | Command | Port | Type |
|---|---|---|---|
| Start application | `cd frontend && npm run dev -- --port 5000` | 5000 | webview |
| Django Backend | `python manage.py runserver 0.0.0.0:8000` | 8000 | console |

## Directory Structure

```
/
├── BenkizBakers/          # Django project settings
├── main/                  # Main Django app (models, views, templates)
├── benkizapi/             # REST API app
│   ├── views.py           # All API endpoints
│   ├── urls.py            # URL routing
│   └── serializers.py     # DRF serializers
├── frontend/              # React Vite app
│   ├── src/
│   │   ├── App.jsx        # Root component + routing
│   │   ├── index.css      # Full theme system (CSS variables)
│   │   ├── api/client.js  # Axios client + all endpoint helpers
│   │   ├── context/       # Auth, Cart, Wishlist, Theme contexts
│   │   ├── components/    # Navbar, Footer, ProductCard
│   │   └── pages/         # All pages
│   └── vite.config.js     # Proxies /api, /media, /static → port 8000
├── static/                # Django static files
├── media/                 # User-uploaded media
└── db.sqlite3             # SQLite database
```

## Pages

| Route | Component | Auth Required |
|---|---|---|
| `/` | Home | No |
| `/shop` | Shop | No |
| `/shop/:id` | ProductDetails | No |
| `/gallery` | Gallery | No |
| `/contact` | Contact | No |
| `/classes` | Classes | No |
| `/search` | Search | No |
| `/auth` | Auth (Login + Register) | No |
| `/cart` | Cart | Yes |
| `/checkout` | Checkout | Yes |
| `/profile` | Profile | Yes |
| `/wishlist` | Wishlist | Yes |
| `/payment/waiting/:ref` | PaymentWaiting | Yes |

## API Endpoints

All API endpoints are under `/api/`:

- `GET /api/auth/csrf/` — Get CSRF token
- `POST /api/auth/login/` — Login
- `POST /api/auth/logout/` — Logout
- `POST /api/auth/register/` — Register
- `GET /api/auth/me/` — Current user + profile
- `GET /api/items/` — List items (params: search, category, limit)
- `GET /api/items/:id/` — Item detail
- `GET /api/items/featured/` — Featured items
- `GET /api/categories/` — Category list
- `GET /api/cart/` — Get cart
- `POST /api/cart/add/` — Add to cart
- `PATCH /api/cart/items/:id/` — Update cart item
- `DELETE /api/cart/items/:id/` — Remove cart item
- `GET /api/wishlist/` — Get wishlist
- `POST /api/wishlist/add/` — Add to wishlist
- `DELETE /api/wishlist/remove/:item_id/` — Remove from wishlist
- `GET /api/lessons/` — List classes
- `POST /api/lessons/:id/enroll/` — Enroll in class
- `DELETE /api/lessons/:id/unenroll/` — Unenroll
- `GET /api/course-basket/` — Get course basket
- `GET/PATCH /api/profile/` — Get/update profile
- `GET /api/testimonials/` — Get testimonials
- `GET /api/team/` — Get team members
- `GET /api/locations/` — Get locations
- `POST /api/contact/` — Send contact message
- `POST /api/checkout/` — Process order + M-Pesa payment
- `GET /api/payment-status/:ref/` — Check payment status
- `GET /api/hero-banners/` — Get hero banners

## Theming

Themes are controlled via the `data-theme` attribute on `<html>`:
- `light` (default) — warm gold primary
- `dark` — dark background, gold accents
- `warm` — red primary, warm cream background

Users can cycle themes using the gear icon in the navbar. Theme persists in `localStorage`.

## Payment

M-Pesa via Kreative Labs API. Requires `API_KEY_KREATIVE_LABS` environment variable.
Business phone: 0795404843
WhatsApp: 254707091550

## Environment Secrets

- `SECRET_KEY` — Django secret key (required)
- `API_KEY_KREATIVE_LABS` — M-Pesa payment API key (optional; payment disabled without it)
