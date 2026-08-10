# African Fashion Web Application – Project Plan

## 1. Project Overview

This project involves building a full-stack web application using Flask and PostgreSQL. The application will showcase African clothing styles and allow users to view, add, and manage outfit data.

The goal is to demonstrate understanding of:

* Database schema design
* CRUD operations
* Flask integration with PostgreSQL
* Frontend development using HTML, CSS, and JavaScript

---

## 2. Project Idea

The application, titled **"African Fashion Showcase"**, will:

* Display a collection of African clothing styles (e.g., Ankara, Dashiki, Kente)
* Allow users to add new outfits
* Store outfit data in a PostgreSQL database
* Provide an interactive and visually appealing interface

---

## 3. Target Users

* Students and users interested in African fashion
* Lecturers assessing full-stack development skills

---

## 4. Core Features

### 4.1 Outfit Management (CRUD)

* Create: Add new outfits via a form
* Read: View all outfits in a gallery
* Update: Edit existing outfit details and category
* Delete: Remove outfits

### 4.2 Pages

* Home page
* Gallery page (view outfits)
* Add Outfit page
* Edit Outfit page
* About page
* Contact page

### 4.3 Database Integration

* PostgreSQL database to store outfit and category data
* Flask-SQLAlchemy for ORM
* Relationship between outfits and categories
* Persistent storage of:

  * Outfit name
  * Category
  * Description
  * Image URL
  * Quantity
  * Price

---

## 5. Database Design

### Tables

**Category**

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | Integer | Primary key |
| name | String | Category name |

**Outfit**

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | Integer | Primary key |
| name | String | Outfit name |
| description | Text | Outfit description |
| image_url | String | Image URL or path |
| quantity | Integer | Stock quantity |
| price | Float | Outfit price |
| category_id | Integer | Foreign key to `categories.id` |

### Relationship

* One Category → Many Outfits
* Implemented using SQLAlchemy `relationship`
* Supports category reuse and accurate joins

---

## 6. Technologies Used

### Backend

* Flask (Python web framework)
* Flask-SQLAlchemy (ORM)
* PostgreSQL (database)

### Frontend

* HTML5 (structure)
* CSS3 (styling)
* JavaScript (interactivity)

### Tools

* Git & GitHub (version control)
* Render.com (deployment)

---

## 7. Project Structure (Planned)

african-fashion-app/
│
├── app.py
├── models.py
├── templates/
├── static/
│   ├── css/
│   └── js/
├── README.md
├── Planning.md
└── requirements.txt

---

## 8. Development Plan

### Phase 1: Setup

* Create project directory
* Initialize Git repository
* Set up virtual environment
* Install Flask and dependencies
* Prepare `requirements.txt`

### Phase 2: Basic Flask App

* Create `app.py`
* Set up routes for home, gallery, add, delete, and high-stock
* Create base template and navigation

### Phase 3: Frontend Development

* Build HTML pages
* Apply CSS styling
* Add JavaScript interactivity and form validation

### Phase 4: Database Integration

* Configure PostgreSQL / SQLite testing database
* Create models with `Category` and `Outfit`
* Implement CRUD operations and category relationships

### Phase 5: Testing

* Add `pytest` support and a simple test file
* Test `/`, `/add`, `/edit/<id>`, and `/gallery`
* Verify category relations and database write operations

### Phase 6: Deployment

* Push project to GitHub
* Deploy using Render.com
* Add `DATABASE_URL` environment variable
* Verify website after deployment

---

## 9. Development Evidence

* Committed category relationship and model improvements
* Committed edit/update route and gallery fixes
* Added `README.md` deployment and testing documentation
* Added `pytest` support and local test file
* Verified syntax with `python -m py_compile`
* Pushed changes to GitHub remote

---

---

## 9. Version Control Strategy

The project will be developed incrementally with meaningful Git commits:

* Initial project setup
* Add base Flask app
* Add templates
* Add CSS styling
* Add database models
* Implement CRUD features

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

