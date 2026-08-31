# African Fashion Web Application – Project Plan

## 1. Project Overview

This project is a full-stack inventory web application for African fashion outfits, built with Flask and PostgreSQL. It was designed to demonstrate practical understanding of relational database schema design, CRUD operations, Flask routing, and frontend integration.

The subject matter — African fashion — was chosen deliberately so the data has natural structure: outfits belong to categories, categories have many outfits, and stock levels vary. This makes the relational model meaningful rather than artificial.

---

## 2. Technology Decisions

### Why Flask?

Flask is a micro-framework that forces explicit decisions about routing, templates, and database integration. This makes it easier to demonstrate understanding because every component is wired together by hand rather than being hidden by convention. Django would have been faster to scaffold but harder to explain.

### Why PostgreSQL?

PostgreSQL supports check constraints, views, and relational integrity enforcement that SQLite does not. The `category_summary` reporting view (used in the `/category-summary` route) requires a SQL `VIEW`, which PostgreSQL supports in production. PostgreSQL is also the standard database offered by Render.com, so the local and hosted environments stay consistent.

### Why Flask-SQLAlchemy?

Raw `psycopg2` queries would require manual SQL strings and expose the app to SQL injection if user input were ever interpolated directly. Flask-SQLAlchemy provides:
- Parameterised queries by default (prevents injection)
- Python-class-based model definitions that double as documentation
- Relationship helpers (`relationship`, `backref`) that make joins readable

### Why SQLite for testing?

PostgreSQL requires a running server. SQLite runs entirely in memory, so tests can spin up a fresh database, run, and tear it down in milliseconds without any infrastructure. The `DATABASE_URL` environment variable controls which database is used, so the same code runs against both without modification.

### Why a `User` model with hashed passwords?

The inventory is writable — adding, editing, and deleting outfits. Without authentication, anyone could modify the data. Passwords are stored as bcrypt hashes via `werkzeug.security.generate_password_hash`; the plaintext password is never saved to the database.

---

## 3. Database Schema Design

### Design Decisions

**Why a separate `Category` table instead of a text field on `Outfit`?**

Storing `category` as a plain string on each outfit would cause duplication and inconsistency — e.g. "Women", "women", and "WOMEN" would be treated as three different categories. A dedicated `Category` table with a unique constraint on `name` enforces consistency and allows the gallery filter to list categories accurately. The `get_or_create_category` helper normalises names to title case before inserting, so "women" and "Women" resolve to the same record.

**Why enforce a `UNIQUE` constraint on `image_url`?**

Each outfit photo should represent a specific item. Allowing two outfits to share the same image would make the gallery misleading. The uniqueness constraint is enforced at the database level (not just in Python), so it holds even if data is inserted outside the application.

**Why a `category_summary` SQL VIEW?**

The `/category-summary` route needs per-category totals (item count, total stock). This could be computed in Python, but a SQL `VIEW` pushes the aggregation into the database where it runs efficiently with a single query. It also demonstrates use of raw SQL alongside the ORM.

### Tables

**User**

| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary key |
| username | String(80) | Unique, required |
| password_hash | String(200) | bcrypt hash — plaintext never stored |

**Category**

| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary key |
| name | String(50) | Unique, title-cased on insert |

**Outfit**

| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary key |
| name | String(100) | Required |
| description | Text | Optional |
| image_url | String(200) | Unique — one image per outfit |
| quantity | Integer | Check: >= 0 |
| price | Float | Check: >= 0 |
| category_id | Integer | Foreign key → `categories.id` |

### Relationship

`Category` → `Outfit` is a one-to-many relationship. One category (e.g. "Women") can have many outfits. The foreign key `category_id` on the `Outfit` table references `categories.id`. SQLAlchemy's `relationship()` with `back_populates` lets both sides navigate the relationship:

```python
# From a category object, access all its outfits:
category.outfits  # list of Outfit instances

# From an outfit, access its category:
outfit.category.name  # e.g. "Women"
```

---

## 4. Route Design

Routes were divided into functional groups:

| Group | Routes | Design rationale |
|-------|--------|-----------------|
| Public pages | `/`, `/about`, `/contact` | No login required — information only |
| Auth | `/login`, `/register`, `/logout` | Login required before any write operation |
| Inventory CRUD | `/gallery`, `/add`, `/edit/<id>`, `/delete/<id>` | Standard resource pattern |
| Stock management | `/dispatch/<id>` | Separate from edit — only decrements quantity |
| Category management | `/categories`, `/categories/<id>/edit`, `/categories/<id>/delete` | Keeps outfit forms clean; categories managed separately |
| Reporting | `/high-stock`, `/category-summary` | Read-only aggregate views |
| Image management | `/images/upload`, `/images/<filename>/rename`, `/images/<filename>/delete` | Keeps image lifecycle separate from outfit lifecycle |
| API | `/api/add-outfit` | JSON endpoint for programmatic access |

`/dispatch/<id>` was kept separate from `/edit/<id>` intentionally: dispatching stock is a single-field operation that does not require loading the full edit form.

---

## 5. Frontend Design Decisions

### Progressive enhancement for JavaScript

All form submissions use standard HTML `<form method="POST">`. JavaScript only adds optional improvements (dispatch validation, delete confirmation, image dropdown behaviour). If JavaScript is disabled, every route still works. This is why `script.js` opens with:

```js
// Client-side enhancements stay optional: all important operations work without JavaScript.
```

### CSS layout

Flexbox was used for the gallery card grid because it handles variable numbers of cards cleanly without requiring a fixed column count. Cards wrap automatically at different screen widths, giving a responsive layout without a separate grid framework.

### Template inheritance

All pages extend `base.html`, which contains the `<head>`, navigation bar, and footer. This ensures consistent styling across pages and means CSS/JS links only need to be maintained in one place.

---

## 6. Development Phases

### Phase 1: Environment setup
- Created virtual environment (`venv/`) and `requirements.txt`
- Initialised Git repository with `.gitignore` (excluded `venv/`, `*.db`, `.env`)
- Chose to use environment variables for `DATABASE_URL` and `SECRET_KEY` from the start — no credentials ever committed to Git

### Phase 2: Database models
- Defined `Category` and `Outfit` models in `models.py` before writing routes
- Added the foreign key relationship first to ensure CRUD routes could use it from day one
- Added `User` model with password hashing for login protection

### Phase 3: Core routes
- Built routes in order: read (`/gallery`) → create (`/add`) → update (`/edit/<id>`) → delete (`/delete/<id>`)
- Added `get_or_create_category` helper to prevent duplicate categories during create/update

### Phase 4: Extended features
- Added `/dispatch/<id>` for stock management
- Added `/high-stock` reporting route
- Added `category_summary` SQL view and `/category-summary` route
- Added category management interface with duplicate-name protection
- Added image upload, rename, and delete management

### Phase 5: Authentication
- Added `User` model, `/register`, `/login`, `/logout` routes
- Protected all write routes with `@login_required`

### Phase 6: Testing
- Added `test_app.py` with pytest covering all major routes and database operations
- Used SQLite in-memory database for tests (no PostgreSQL required)
- 22 tests covering: auth, CRUD, validation, category management, API, and reporting

### Phase 7: Deployment
- Deployed to Render.com with PostgreSQL add-on
- Set `DATABASE_URL` and `SECRET_KEY` as environment variables in Render dashboard
- Verified all routes on the live URL after deploy

---

## 7. Testing Strategy

Tests use a `test_client` pytest fixture that:
1. Sets `DATABASE_URL` to `sqlite:///:memory:`
2. Creates all tables in memory
3. Registers a test user so protected routes can be accessed
4. Drops all tables after each test

This means tests are fully isolated — each test starts with a clean database. SQLite is used instead of PostgreSQL because it requires no server setup and runs in milliseconds.

Key test areas:
- Public pages return HTTP 200
- Protected routes redirect to login when unauthenticated
- Add/edit/delete operations persist correctly in the database
- Duplicate category names are rejected
- Duplicate image assignments are rejected
- The `category_summary` view aggregates correctly
- The API rejects invalid values

---

## 8. Security Considerations

- `SECRET_KEY` is read from an environment variable; a fallback string is used locally only
- `DATABASE_URL` is never hard-coded; it is always read from the environment
- Passwords are hashed with bcrypt via `werkzeug.security` — the plaintext is never stored or logged
- SQLAlchemy parameterised queries prevent SQL injection
- `secure_filename()` from Werkzeug sanitises uploaded filenames before saving to disk
- All write routes require login via `@login_required`

Each commit will represent a clear development step.

---

## 10. Future Enhancements

* User authentication system 
* Image upload functionality
* Search and filtering
* Improved UI/UX design

---

## 11. Success Criteria

The project will be considered successful if:

* The Flask app runs correctly
* PostgreSQL is fully integrated
* CRUD operations function properly
* The website is visually appealing
* The app is deployed and accessible online

---

