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

### 4. Run the application locally

```powershell
python app.py
```

Open your browser at `http://127.0.0.1:5000` and verify the site functions:

* Add an outfit via `/add`
* Edit an outfit via `/edit/<id>`
* View the gallery at `/gallery`
* Dispatch stock via the gallery form
* Confirm categories appear and are reusable

### 5. Run tests

```powershell
pytest
```

This validates the homepage, outfit creation, and outfit editing flows.

---

## Render Deployment

### 1. Create a new Web Service

* Go to Render.com and create a new Web Service
* Connect the GitHub repository: `HlengiweNcube/flask_db_project`

### 2. Set build and start commands

* Build command:

```bash
pip install -r requirements.txt
```

* Start command:

```bash
gunicorn app:app
```

### 3. Add environment variables

* `DATABASE_URL` — your PostgreSQL connection string

Example:

```bash
postgresql://postgres:<password>@<host>:5432/<database>
```

### 4. Deploy and verify

After deployment, verify the app is accessible and fully functional:

* Visit the deployed Render URL
* Test the gallery and add/edit routes
* Confirm the `DATABASE_URL` variable is configured

---

## Post-deployment Verification

* Confirm the live app matches local behavior
* Verify category filters and gallery search work
* Confirm editing and deletion work without errors
* Check that stock reporting and high-stock view load correctly

---

## Notes on Security

* Do not commit the actual `DATABASE_URL` or any database credentials to GitHub
* Use environment variables instead of hard-coded connection strings
* Keep the `requirements.txt` dependency list up to date
