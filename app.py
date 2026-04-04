from flask import Flask, jsonify, render_template, request, redirect
from models import db, Outfit, Category
from sqlalchemy import func, text

import os

app = Flask(__name__)

uri = os.environ.get("DATABASE_URL")

if not uri:
    uri = "postgresql://postgres:Amanda%40123@localhost:5432/african_fashion"

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/gallery')
def gallery():
    category = request.args.get('category')
    sort = request.args.get('sort')
    search = request.args.get('search')

    query = Outfit.query.filter(Outfit.quantity > 0)

    if search:
        query = query.filter(Outfit.name.ilike(f"%{search}%"))

    if category:
        query = query.filter(Outfit.category == category)

    if sort == 'asc':
        query = query.order_by(Outfit.name.asc())
    elif sort == 'desc':
        query = query.order_by(Outfit.name.desc())

    outfits = query.all()

    category_counts = db.session.query(
        Outfit.category,
        func.count(Outfit.id)
    ).filter(Outfit.quantity > 0)\
     .group_by(Outfit.category).all()

    stats = db.session.query(
        func.count(Outfit.id),
        func.sum(Outfit.quantity),
        func.avg(Outfit.quantity),
        func.min(Outfit.quantity),
        func.max(Outfit.quantity)
    ).filter(Outfit.quantity > 0).first()

    # VIEW
    category_view = db.session.execute(
        text("SELECT * FROM category_summary")
    ).fetchall()

    # JOIN
    results = db.session.query(
    Outfit.name,
    Category.name
  ).join(Category, Outfit.category == Category.name)\
 .filter(Outfit.quantity > 0)\
 .all()
    
    return render_template(
        'gallery.html',
        outfits=outfits,
        category_counts=category_counts,
        stats=stats,
        results=results,
        category_view=category_view
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        image_url = request.form['image_url']
        quantity = int(request.form.get('quantity', 0))
        price = float(request.form.get('price', 0.0))

        existing = Outfit.query.filter_by(name=name, category=category).first()

        if existing:
            existing.quantity += quantity
            existing.price = price
        else:
            new = Outfit(
                name=name,
                category=category,
                description=description,
                image_url=image_url,
                quantity=quantity,
                price=price
            )
            db.session.add(new)

        db.session.commit()
        return redirect('/gallery')

    return render_template('add_outfit.html')


@app.route('/delete/<int:id>')
def delete(id):
    outfit = Outfit.query.get_or_404(id)
    db.session.delete(outfit)
    db.session.commit()
    return redirect('/gallery')


@app.route('/dispatch/<int:id>', methods=['POST'])
def dispatch(id):
    outfit = Outfit.query.get_or_404(id)
    amount = request.form.get('amount')

    if not amount:
        return "Enter quantity"

    amount = int(amount)

    if amount <= 0:
        return "Invalid"

    if outfit.quantity < amount:
        return "Not enough stock"

    outfit.quantity -= amount
    db.session.commit()

    return redirect('/gallery')

@app.route('/high-stock')
def high_stock():
    avg = db.session.query(func.avg(Outfit.quantity)).scalar() or 0

    # ✅ FILTER HIGH STOCK + ONLY VALID ITEMS
    outfits = Outfit.query.filter(
        Outfit.quantity > avg,
        Outfit.quantity > 0
    ).all()

    # ✅ GROUP BY
    category_counts = db.session.query(
        Outfit.category,
        func.count(Outfit.id)
    ).filter(
        Outfit.quantity > avg
    ).group_by(Outfit.category).all()

    # ✅ AGGREGATES
    stats = db.session.query(
        func.count(Outfit.id),
        func.sum(Outfit.quantity),
        func.avg(Outfit.quantity),
        func.min(Outfit.quantity),
        func.max(Outfit.quantity)
    ).filter(
        Outfit.quantity > avg
    ).first()

    # ✅ HANDLE NULLS
    stats = (
        stats[0] or 0,
        stats[1] or 0,
        round(stats[2], 2) if stats[2] else 0,
        stats[3] or 0,
        stats[4] or 0
    )

    # ✅ JOIN
    results = db.session.query(
        Outfit.name,
        Category.name
    ).join(Category, Outfit.category == Category.name)\
     .filter(Outfit.quantity > avg)\
     .all()

    # ✅ VIEW
    category_view = db.session.execute(
        text("SELECT * FROM category_summary")
    ).fetchall()

    return render_template(
        'gallery.html',
        outfits=outfits,
        highlight="High Stock (Above Average)",
        avg_quantity=round(avg, 2),
        category_counts=category_counts,
        stats=stats,
        results=results,
        category_view=category_view
    )
@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/api/add-outfit', methods=['POST'])
def add_outfit_api():
    data = request.get_json()

    name = data.get('name')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    # ✅ VALIDATION
    if not name or not category:
        return jsonify({"error": "Name and category required"}), 400

    if quantity is None or quantity < 0:
        return jsonify({"error": "Invalid quantity"}), 400

    if price is None or price < 0:
        return jsonify({"error": "Invalid price"}), 400

    # ✅ SAVE
    outfit = Outfit(
        name=name,
        category=category,
        description=data.get('description'),
        image_url=data.get('image_url'),
        quantity=quantity,
        price=price
    )

    db.session.add(outfit)
    db.session.commit()

    return jsonify({"message": "Outfit added successfully"})


if __name__ == '__main__':
    app.run(debug=True)