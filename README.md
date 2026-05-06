# African Fashion Web Application

An interactive web-based application for managing African traditional clothing inventory.
Built using Flask, PostgreSQL, HTML, CSS, JavaScript, and JSON.

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

This project demonstrates:

* Integration of Flask with PostgreSQL
* Implementation of full CRUD functionality
* Use of relational database design
* Frontend interaction using JavaScript and JSON
* Deployment using Render

---

## 🧠 Design Decisions

* **Flask** was chosen for simplicity and flexibility
* **PostgreSQL** was used to demonstrate relational database concepts
* **SQLAlchemy ORM** simplifies database interaction
* **JavaScript + JSON** enables dynamic form submission without page reload
* **Render** was used for deployment to make the app accessible online

---

## 🗄️ Database Design

### Tables:

**Category**

* id (Primary Key)
* name

**Outfit**

* id (Primary Key)
* name
* price
* quantity
* category_id (Foreign Key)

### Relationship:

* One Category → Many Outfits
* Implemented using SQLAlchemy relationship and foreign key

---

## ⚙️ Features

* Add outfits
* View outfits (Gallery)
* Update outfits (stock and details)
* Delete outfits
* Search outfits
* Filter by category
* Sort alphabetically
* Stock management (dispatch feature)

---

## 🧮 Advanced SQL Features

* Aggregate functions (AVG, MIN, MAX)
* Subqueries (above-average stock)
* JOIN between Outfit and Category
* PostgreSQL VIEW (`category_summary`)
* TRIGGER to prevent negative stock

---

## 🔄 CRUD Implementation

* **Create:** Add new outfit via form
* **Read:** Display outfits in gallery
* **Update:** Modify outfit details and stock
* **Delete:** Remove outfit from database

---

## 🧪 Testing

* Manual testing of all routes
* Tested add, update, delete operations
* Verified database updates
* Tested deployed version on Render

---

## ☁️ Deployment (Render)

The application is deployed using Render.

### Steps:

1. Create a PostgreSQL database on Render
2. Copy the database connection URL
3. Add it as an environment variable:

   * Key: `DATABASE_URL`
4. Set build command:

   ```
   pip install -r requirements.txt
   ```
5. Set start command:

   ```
   gunicorn app:app
   ```

---

## 💻 Running Locally

1. Create virtual environment:

   ```
   python -m venv venv
   ```
2. Activate environment
3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
4. Set DATABASE_URL
5. Run:

   ```
   python app.py
   ```

---

## 📁 Project Structure

* app.py → Flask routes and logic
* models.py → Database models
* templates/ → HTML templates
* static/ → CSS, JS, images

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
