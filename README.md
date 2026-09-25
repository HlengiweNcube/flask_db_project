# African Fashion Web Application

An interactive inventory application for African fashion outfits.
Built with Flask, SQLAlchemy, PostgreSQL, HTML, CSS, and JavaScript.

---

## Author

Hlengiwe Ncube
04 April 2026

---

## 🌐 Project Links

| Resource          | Link                                              |
| ----------------- | ------------------------------------------------- |
| GitHub Repository | https://github.com/HlengiweNcube/flask_db_project |
| Live Web App      | https://flask-db-project.onrender.com             |

> **Note:** The app runs on Render's free tier. If the page takes 20–30 seconds to load on first visit, the service is waking up from idle — refresh once and it will load normally.

---

## 🎯 Purpose

This project documents and demonstrates:

* Flask application structure and routing
* Relational database schema design
* CRUD operations for Outfit inventory
* Category relationship using SQLAlchemy foreign keys
* Frontend integration with HTML, CSS, and JavaScript
* Deployment setup for Render

---

## 🗄️ Database Design

### Tables

**User**

* `id` — Primary key
* `username` — Required and unique login name
* `email` — Required and unique email address used for password recovery
* `password_hash` — Securely hashed password; the plain password is never stored

**Category**

* `id` — Primary key
* `name` — Category title (unique)

**Outfit**

* `id` — Primary key
* `name` — Outfit name
* `description` — Text description
* `image_url` — Image filename resolved by the `/media/<filename>` route
* `quantity` — Stock quantity
* `price` — Price in Euros
* `category_id` — Integer foreign key to `categories.id`

### Relationship

* One Category → Many Outfits
* Implemented using SQLAlchemy `relationship` and `ForeignKey`
* Categories are reused instead of storing duplicate category text on each outfit

**UploadedImage**

* `id` — Primary key
* `filename` — Required and unique uploaded filename
* `mimetype` — Stored MIME type used when serving the image
* `data` — Binary image bytes stored in the database

Bundled sample images are read from `static/images/`. Uploaded images are
stored in `uploaded_images` and served through `/media/<filename>`, so they
survive Render redeploys.

### Database View: `category_summary`

The application also creates a SQL view named `category_summary`. It joins
`categories` to `outfits` and calculates the number of outfits and total stock
for each category:

```sql
CREATE VIEW category_summary AS
SELECT c.id AS category_id,
       c.name AS category_name,
       COUNT(o.id) AS total_items,
       COALESCE(SUM(o.quantity), 0) AS total_stock
FROM categories c
LEFT JOIN outfits o ON o.category_id = c.id
GROUP BY c.id, c.name;
```

`ensure_category_summary_view()` recreates the view when the application starts,
so a new SQLite or PostgreSQL database has the reporting structure before any
request uses it. The `/category-summary` route reads this view and renders the
results in `category_summary.html`. The behavior is covered by
`test_category_summary_view_aggregates_outfits` in `test_app.py`.

---

## 🚀 Application Features

* Full CRUD for outfits:
  * Create new outfits
  * Read and filter outfits in the gallery
  * Update outfit details and category
  * Delete outfits
* Stock dispatch feature to subtract inventory quantity
* Search and category filter
* Sort gallery results alphabetically
* Highlight items whose stock is above the overall inventory average
* Login protection for inventory management
* Dedicated category management page with duplicate-name protection
* Image management page for uploading, renaming, and removing unused images

---

## 📦 Routes

* `/` — Home page
* `/gallery` — Outfit gallery with search, sort, and category filter
* `/add` — Add new outfit form
* `/edit/<id>` — Edit existing outfit
* `/delete/<id>` — Delete outfit record
* `/dispatch/<id>` — Dispatch stock quantity from an outfit
* `/high-stock` — Show outfits with stock above the overall inventory average; the displayed average is the threshold used for filtering
* `/category-summary` — Display category totals from the SQL reporting view
* `/about` — Information page
* `/contact` — Contact page
* `/api/add-outfit` — JSON POST endpoint for outfit creation
* `/login` — Authenticate an inventory user
* `/register` — Create an account with a username, email address, and password
* `/forgot-password` — Request an expiring password reset link by email
* `/reset-password/<token>` — Set a new password using a valid reset link
* `/logout` — End the current session
* `/categories` — View and add reusable categories

The home, gallery, About, and Contact pages are public. Adding, editing,
dispatching, deleting, and using the API require authentication.
Authenticated users can manage categories and images from **Manage Categories
and Images**. Images currently used by outfits cannot be deleted, and renaming
an image updates its outfit references automatically.
An image filename can only be assigned to one outfit. The add and edit routes
check for an existing assignment and reject reuse, preventing accidental image
duplication in the gallery. This is enforced by application validation rather
than a database-level `UNIQUE` constraint.
Outfit names may be reused for different garments, including garments in
different categories. Each submission creates its own outfit record. Image
filenames remain unique to one outfit so each record has its own picture.

**Uploaded images are stored in the database, not on disk.** Render's free web
service has no persistent disk, so files saved to the filesystem are wiped on
every redeploy. The `UploadedImage` model stores the image bytes and MIME type
in PostgreSQL, and the `/media/<filename>` route serves either an uploaded
database image or one of the bundled sample images in `static/images/`
(which ship with the Git repo and are always available). Bundled sample
images are read-only in the UI — only uploaded images can be renamed or
deleted.

---

## 💡 Design and Implementation Notes

* The app uses `Flask-SQLAlchemy` for ORM mapping and `SQLAlchemy` for query construction
* Categories are created or reused automatically when adding/editing outfits
* Authenticated users can also add categories directly from `/categories`
* The gallery uses join queries to connect `Outfit` and `Category`
* Template pages use dynamic category selection and a clean edit workflow
* Add and Edit forms provide dropdowns for categories and available images
* Server-side validation ensures required fields and non-negative inventory values
* The JSON API uses the same validation helper as the HTML form
* Flask-Login protects inventory-changing routes and stores only password hashes

Password reset email delivery uses SMTP. Configure `SMTP_HOST`, `SMTP_PORT`,
`SMTP_USERNAME`, `SMTP_PASSWORD`, and `SMTP_FROM` in the deployment environment.
Reset links expire after one hour, and the reset request page uses the same
message whether or not an account exists for the submitted address.

---

## 🧪 Local Testing

### 1. Install dependencies

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure the database

For PostgreSQL:

```powershell
$env:DATABASE_URL = "postgresql://postgres:password@localhost:5432/african_fashion"
```

For local SQLite testing:

```powershell
$env:DATABASE_URL = "sqlite:///local_test.db"
```

### 3. Run the application

Create the tables before the first run:

```powershell
python -m flask --app app init-db
```

Optionally load sample outfits so all routes have data to display immediately:

```powershell
python -m flask --app app seed-db
```

This inserts 8 sample outfits across four categories (Traditional, Women, Children, Accessories). The command is safe to re-run — it skips any outfit whose image is already assigned.

Open `/register` to create a local user, then use `/login` before testing the
inventory management pages.

Then start the development server:

```powershell
python app.py
```

### 4. Test the app

Run the automated tests:

```powershell
python -m pytest -q
```

The suite uses an isolated in-memory SQLite database and covers the homepage,
authentication, category reuse, create/update/delete, dispatch, image
management, password reset, reporting, and invalid API input. The browser can
then be used to verify the `/gallery`, `/add`, `/edit/<id>`, `/delete/<id>`,
and `/high-stock` flows.

---

## ☁️ Deployment Instructions

This app is designed for deployers such as Render.com.

For full deployment and environment setup details, see `deployment.md`.

### Render setup

1. Create a new Web Service in Render
2. Connect the GitHub repository
3. Set the build command:

```bash
pip install -r requirements.txt
```

4. Set the start command:

```bash
gunicorn app:app
```

5. Add environment variables:

* `DATABASE_URL` — PostgreSQL connection string
* `SECRET_KEY` — random secret used to sign sessions and reset tokens
* `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM` —
  optional SMTP settings for password reset email

6. Deploy and verify the app on the provided Render URL

The production database URL is read only from the `DATABASE_URL` environment
variable. No password or connection string is stored in the repository. Run
`python -m flask --app app init-db` once against a new database before using
the hosted forms.

---

## ✅ Hosted App Verification

The live app is available at **https://flask-db-project.onrender.com**. The
GitHub repository is
**https://github.com/HlengiweNcube/flask_db_project**. After each deployment,
run the verification table below against the live URL and record the date in
the submission evidence.

The following routes were tested and confirmed working:

| Route | Result |
|-------|--------|
| `/` | Home page loads with navigation |
| `/register` | Account creation form accepts username, email, and password |
| `/login` | Login form authenticates correctly |
| `/gallery` | Outfit cards display with search and category filter |
| `/gallery?search=zulu` | Search filters results correctly |
| `/add` | Add form shows category and image dropdowns; outfit saves |
| `/edit/<id>` | Edit form pre-fills existing values; update persists |
| `/delete/<id>` (POST) | Outfit is removed and gallery reloads |
| `/dispatch/<id>` (POST) | Stock quantity is decremented correctly |
| `/high-stock` | Shows outfits above average stock |
| `/category-summary` | Displays per-category totals from SQL view |
| `/categories` | Category management page lists and creates categories |
| `/categories/<id>/edit` (POST) | Category name is updated |
| `/categories/<id>/delete` (POST) | Unused category is removed |
| `/images` (POST) | Uploaded image is stored in the database |
| `/images/<filename>/rename` (POST) | Uploaded image is renamed and outfit references update |
| `/images/<filename>/delete` (POST) | Unused uploaded image is removed |
| `/media/<filename>` | Uploaded or bundled image is served |
| `/api/add-outfit` (POST) | JSON request creates an outfit |
| `/forgot-password` | Password reset request returns a safe response |
| `/reset-password/<token>` | Valid token allows a new password |
| `/logout` (POST) | Current session ends |
| `/about` | About page loads |
| `/contact` | Contact page loads |

The PostgreSQL database on Render is connected via the `DATABASE_URL`
environment variable set in the Render dashboard; no credentials are stored in
the repository. Compare the hosted page at desktop and mobile widths with the
local page after deployment. The cellphone verification record is documented
in `MOBILE_TEST_EVIDENCE.md`.

---

## 📁 Project Structure

* `app.py` — Flask routes and application logic
* `models.py` — SQLAlchemy database models
* `templates/` — HTML templates, including authentication and password recovery
* `static/css/` — Stylesheets
* `static/js/` — JavaScript code
* `static/images/` — Bundled sample outfit images
* `requirements.txt` — Python dependencies
* `render.yaml` — Render web service and PostgreSQL configuration
* `deployment.md` — Deployment and setup guide
* `planning.md` — Design decisions and development history
* `ASSIGNMENT_CHECKLIST.md` — Assignment requirements checklist
* `SUBMISSION_GUIDE.md` — Submission and verification guide
* `MOBILE_TEST_EVIDENCE.md` — Manual cellphone testing record
* `test_app.py` — Automated pytest coverage

---

## 📚 Improvements Made

* Added a relational schema with `User`, `Category`, `Outfit`, and
  `UploadedImage` tables
* Added a foreign-key relationship between `Category` and `Outfit` using
  Flask-SQLAlchemy relationships
* Implemented complete outfit CRUD operations, including the edit/update route
* Added category creation, reuse, editing, and protected deletion
* Added the `category_summary` SQL view and reporting route
* Added search, category filtering, alphabetical sorting, stock dispatch, and
  high-stock reporting
* Added database-backed image upload, rename, delete, and media serving for
  persistent Render storage
* Added username/email registration, login protection, and password recovery
* Added a repeatable `seed-db` command for manual route demonstrations
* Added server-side validation, password hashing, secure filenames, and
  environment-based configuration
* Added responsive CSS, JavaScript enhancements, and high-contrast keyboard
  focus indicators
* Added README documentation, route explanations, deployment instructions, and
  design-decision notes
* Added SQLite test setup with 29 automated pytest tests
* Added cellphone verification evidence and hosted-app verification guidance

---

## 📚 Learning Outcomes

* Configure Flask-SQLAlchemy for both PostgreSQL production use and isolated
  SQLite testing
* Design a relational schema with four tables, unique constraints, check
  constraints, a foreign key, and a one-to-many relationship
* Create and query a database view for category-level reporting
* Implement complete CRUD logic with separate routes for create, read, update,
  delete, and stock dispatch operations
* Use Flask route protection, password hashing, email registration, and secure
  password recovery tokens
* Validate form and JSON input on the server and handle invalid data safely
* Integrate Jinja templates, responsive CSS, and optional JavaScript
  enhancements using template inheritance and Flask static-file helpers
* Store uploaded image bytes in the database so media persists across Render
  redeployments
* Organize configuration with environment variables instead of committed
  credentials
* Use pytest fixtures and an in-memory database to test routes and database
  behavior repeatably
* Deploy a Flask application with Gunicorn, Render, PostgreSQL, and automatic
  GitHub deployment
* Document design decisions, testing evidence, deployment steps, and mobile
  verification for reproducible assessment

---

## References

### Image Sources

* Wikimedia Commons (Public Domain) — https://commons.wikimedia.org
* Alamy — https://www.alamy.com
* Getty Images — https://www.gettyimages.com

Images are used for educational, non-commercial coursework purposes only.

### Documentation and Technical References

* Flask documentation — https://flask.palletsprojects.com
* Flask-SQLAlchemy documentation — https://flask-sqlalchemy.palletsprojects.com
* SQLAlchemy documentation — https://docs.sqlalchemy.org
* Flask-Login documentation — https://flask-login.readthedocs.io
* Werkzeug documentation (password hashing, `secure_filename`) — https://werkzeug.palletsprojects.com
* PostgreSQL documentation — https://www.postgresql.org/docs
* Render documentation (deployment, Blueprints, environment variables) — https://render.com/docs
* MDN Web Docs (HTML, CSS, JavaScript reference) — https://developer.mozilla.org
* pytest documentation — https://docs.pytest.org

---

## Author

Hlengiwe Ncube
