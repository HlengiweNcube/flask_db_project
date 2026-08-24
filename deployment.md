# Deployment and Setup Guide

This document explains how to set up the project locally and deploy it to Render.com.
It includes the commands, environment variables, and verification steps used during development.

---

## Local Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure a local database

#### PostgreSQL

Create a local PostgreSQL database and set the `DATABASE_URL` environment variable:

```powershell
$env:DATABASE_URL = "postgresql://postgres:<password>@localhost:5432/african_fashion"
```

Replace `<password>` with your PostgreSQL password.

#### SQLite (quick local testing)

For testing without PostgreSQL, use SQLite:

```powershell
$env:DATABASE_URL = "sqlite:///local_test.db"
```

### 4. Initialize the database

Initialize the database tables:

```powershell
python -m flask --app app init-db
```

Or if using the custom alias:

```powershell
python -m flask init_db
```

### 5. Run the application locally

```powershell
python app.py
```

Open your browser at `http://127.0.0.1:5000` and verify the site functions:

* Add an outfit via `/add`
* Edit an outfit via `/edit/<id>`
* View the gallery at `/gallery`
* Dispatch stock via the gallery form
* Confirm categories appear and are reusable

### 6. Run tests

```powershell
pytest
```

This validates the homepage, outfit creation, and outfit editing flows.

---

## Render Deployment

The repository includes `render.yaml`, a Render Blueprint that defines the web
service, PostgreSQL database, build command, start command, and automatic
`DATABASE_URL` connection. Blueprint deployments use the `main` branch and
have `autoDeploy: true`, so a push to GitHub triggers a new Render deploy.

### 1. Create a new Web Service

* Go to Render.com and choose **New > Blueprint**
* Connect the GitHub repository: `HlengiweNcube/flask_db_project`
* Select the `main` branch and apply the `render.yaml` Blueprint

If the service already exists, open **Settings > Build & Deploy**, set the
branch to `main`, and set **Auto-Deploy** to **Yes**.

### 2. Set build and start commands

* Build command:

```bash
pip install -r requirements.txt
```

* Start command:

```bash
gunicorn app:app
```

These values are already supplied by `render.yaml`.

### 3. Add environment variables

* `DATABASE_URL` — your PostgreSQL connection string

When using the Blueprint, Render creates this variable from the managed
PostgreSQL database automatically. Do not replace it with a hard-coded value.

Example:

```bash
postgresql://postgres:<password>@<host>:5432/<database>
```

Do not paste this value into `app.py`, commit it to GitHub, or include it in
screenshots. Render supplies the value to the application at runtime.

### 4. Create the database tables

After the PostgreSQL database is available, open a Render shell (or run the
command from a trusted machine using the same `DATABASE_URL`) and run:

```bash
flask --app app init-db
```

This creates the `categories` and `outfits` tables from the SQLAlchemy models.
The `Outfit.category_id` column is a foreign key to `Category.id`, and each
outfit is connected through the `Category.outfits` relationship.

### 5. Deploy and verify

After deployment, verify the app is accessible and fully functional:

* Visit the deployed Render URL
* Test the gallery and add/edit routes
* Confirm the `DATABASE_URL` variable is configured

Record the deployed URL and test these workflows in the browser: open the
gallery, add an outfit, confirm its category appears in the category counts,
edit it, dispatch stock, and delete it. Also test `/gallery?search=shirt` and
`/high-stock`. Compare the hosted pages with the local version at desktop and
mobile widths and keep screenshots or a short test log as submission evidence.

---

## Post-deployment Verification

* Confirm the live app matches local behavior
* Verify category filters and gallery search work
* Confirm editing and deletion work without errors
* Check that stock reporting and high-stock view load correctly
* Confirm invalid negative quantities are rejected instead of creating rows

---

## Notes on Security

* Do not commit the actual `DATABASE_URL` or any database credentials to GitHub
* Use environment variables instead of hard-coded connection strings
* Keep the `requirements.txt` dependency list up to date
