# African Fashion Web Application

An interactive web-based application for managing African traditional clothing inventory.  
Built using **Flask**, **PostgreSQL**, **HTML**, **CSS**, **JavaScript**, and **JSON**.

---

## Auth  
**Hlengiwe Ncube
**04 April 2026**

---
## Project Links 
| Resource                        | Link                                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------- |
| **GitHub Repository**           | [https://github.com/HlengiweNcube/flask_db_project] (https://github.com/HlengiweNcube/flask_db_project) |

## Purpose  
This project fulfills the Database & Web Development assignment requirements, demonstrating:  
- Integration of Flask with PostgreSQL  
- Use of advanced SQL concepts  
- Implementation of CRUD operations  
- Data validation across multiple layers  
- Interactive frontend using JavaScript and JSON  

---

## Project Links  

| Resource                        | Link |
|--------------------------------|------|
| **GitHub Repository**          | Add your GitHub link here |
| **Live Website (Optional)**    | Not deployed |

---

## Project Concept  

The **African Fashion Web Application** is designed to manage and showcase traditional African outfits.  
It allows users to add, update, delete, and view clothing items while tracking stock levels and prices.  

The system demonstrates full-stack development by combining backend logic, database management, and frontend interactivity.

---

## Key Features  

- **Gallery:** Displays all outfits with images, category, price, and stock  
- **Add Outfit:** Users can add new clothing items  
- **Update Logic:** If an outfit already exists, quantity is updated instead of duplicating  
- **Delete Function:** Removes outfits from the system  
- **Dispatch Feature:** Reduces stock safely with validation  
- **Search:** Find outfits by name  
- **Filter:** View by category (Men, Women, Teens, Children)  
- **Sort:** Alphabetical sorting (A–Z / Z–A)  
- **High Stock:** Displays items above average stock (Subquery)  
- **Image Slider:** Interactive homepage slider using JavaScript  

---

## Database Features  

### 1. Aggregate Functions  
- Total items  
- Total stock  
- Average stock (formatted to 2 decimal places)  
- Minimum and maximum stock  

---

### 2. Subquery  
Displays outfits with stock greater than the average:

```sql
SELECT * FROM outfits
WHERE quantity > (SELECT AVG(quantity) FROM outfits);
3. Join
Combines Outfit and Category tables:

db.session.query(Outfit.name, Category.name).join(
    Category, Outfit.category == Category.name
)
4. View
A PostgreSQL view was created to summarise outfits per category:

CREATE VIEW category_summary AS
SELECT category, COUNT(*) AS total_items
FROM outfits
WHERE quantity > 0
GROUP BY category;
5. Trigger
Prevents negative stock values:

CREATE OR REPLACE FUNCTION prevent_negative_quantity()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantity < 0 THEN
        RAISE EXCEPTION 'Quantity cannot be negative';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_quantity
BEFORE INSERT OR UPDATE ON outfits
FOR EACH ROW
EXECUTE FUNCTION prevent_negative_quantity();
Validation
Frontend Validation
Required fields

Minimum values for quantity and price

Backend Validation (Flask)
Prevents empty inputs

Prevents negative values

JSON Validation
Data submitted using fetch()

Validated before insertion into database

JavaScript Features
Image slider with next/previous functionality

Category filtering

JSON form submission using fetch()

Dynamic interaction without page reload

Design & Accessibility Highlights
Clean layout using CSS

Structured templates using Jinja2

Responsive design for different screen sizes

Clear navigation and user-friendly interface

Technical Implementation
Flask (Python):

Routing and backend logic

Database interaction via SQLAlchemy

PostgreSQL:

Data storage

Advanced SQL features (JOIN, VIEW, TRIGGER, SUBQUERY)

HTML & CSS:

Page structure and styling

JavaScript:

DOM manipulation

Slider functionality

JSON form handling

Project Structure
flask_db_project/
│
├── app.py
├── models.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── gallery.html
│   ├── add_outfit.html
│   ├── about.html
│   └── contact.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md
How to Run the Project
Activate virtual environment

Run the Flask application:

python app.py
Open in browser:

http://127.0.0.1:5000/
Key Learning Outcomes
Integration of Flask with PostgreSQL

Use of advanced SQL queries and database features

Implementation of validation at multiple levels

Use of JavaScript and JSON for dynamic interaction

Full-stack web application development

Author
Hlengiwe Ncube  


## Image Sources & Copyright
**Wikimedia Commons (Public Domain)**  
**www.alamy.com**  
**www.gettyimages.ie**  

https://github.com/HlengiweNcube/flask_db_project


