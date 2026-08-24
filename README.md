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
* `password_hash` — Securely hashed password; the plain password is never stored

**Category**

* `id` — Primary key
* `name` — Category title (unique)

**Outfit**

* `id` — Primary key
* `name` — Outfit name
* `description` — Text description
* `image_url` — Filename selected from `static/images/`
* `quantity` — Stock quantity
* `price` — Price in Euros
* `category_id` — Integer foreign key to `categories.id`

### Relationship

* One Category → Many Outfits
* Implemented using SQLAlchemy `relationship` and `ForeignKey`
* Categories are reused instead of storing duplicate category text on each outfit

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
* Highlight above-average stock items
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
* `/high-stock` — Show outfits with stock above average
* `/about` — Information page
* `/contact` — Contact page
* `/api/add-outfit` — JSON POST endpoint for outfit creation
* `/login` — Authenticate an inventory user
* `/register` — Create an account
* `/logout` — End the current session
* `/categories` — View and add reusable categories

The home, gallery, About, and Contact pages are public. Adding, editing,
dispatching, deleting, and using the API require authentication.
Authenticated users can manage categories and images from **Manage Categories
and Images**. Images currently used by outfits cannot be deleted, and renaming
an image updates its outfit references automatically.

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

The suite uses an isolated in-memory SQLite database and covers the home page,
category reuse, create/update/delete, dispatch, and invalid API input. The
browser can then be used to verify the `/gallery`, `/add`, `/edit/<id>`,
`/delete/<id>`, and `/high-stock` flows.

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

6. Deploy and verify the app on the provided Render URL

The production database URL is read only from the `DATABASE_URL` environment
variable. No password or connection string is stored in the repository. Run
`python -m flask --app app init-db` once against a new database before using
the hosted forms.

---

## 📁 Project Structure

* `app.py` — Flask routes and application logic
* `models.py` — SQLAlchemy database models
* `templates/` — HTML templates
* `static/css/` — Stylesheets
* `static/js/` — JavaScript code
* `requirements.txt` — Python dependencies
* `deployment.md` — Deployment and setup guide
* `test_app.py` — Automated pytest coverage

---

## 📚 Improvements Made

* Added `Category` model usage and foreign key relationships
* Added edit/update route for outfits
* Improved gallery filters and category joins
* Added README documentation and deployment instructions
* Added local testing guidance and route documentation
* Added `deployment.md` for deployment evidence and setup
* Added automated `pytest` tests

---

## 📚 Learning Outcomes

* Flask + PostgreSQL integration
* Relational database design
* Full-stack web development
* Deployment and environment configuration

---

## Image Sources

Wikimedia Commons (Public Domain)
Alamy
Getty Images

---

## Author

Hlengiwe Ncube
