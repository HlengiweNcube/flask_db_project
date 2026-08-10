from flask import Flask, abort, jsonify, render_template, request, redirect
from models import db, Outfit, Category
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

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


def get_or_create_category(name):
    """Return an existing Category or create a new one.

    This helper normalizes category names and ensures the Category table
    is used consistently across Outfit records.
    """
    if not name:
        return None

    normalized_name = name.strip().title()
    category = db.session.execute(
        select(Category).filter_by(name=normalized_name)
    ).scalar_one_or_none()

    if not category:
        category = Category(name=normalized_name)
        db.session.add(category)
        db.session.commit()

    return category


def get_category_choices():
    """Return category options for templates."""
    return db.session.scalars(
        select(Category).order_by(Category.name)
    ).all()


def get_category_counts(self_filter=None):
    """Return counts of outfits grouped by category."""
    stmt = select(Category.name, func.count(Outfit.id)).join(Outfit)
    if self_filter is not None:
        stmt = stmt.filter(self_filter)
    stmt = stmt.group_by(Category.name)
    return db.session.execute(stmt).all()


def get_stock_stats(self_filter=None):
    """Return aggregated outfit stock statistics."""
    stmt = select(
        func.count(Outfit.id),
        func.sum(Outfit.quantity),
        func.avg(Outfit.quantity),
        func.min(Outfit.quantity),
        func.max(Outfit.quantity),
    )
    if self_filter is not None:
        stmt = stmt.filter(self_filter)

    stats = db.session.execute(stmt).one_or_none()
    if not stats:
        return (0, 0, 0, 0, 0)

    return (
        stats[0] or 0,
        stats[1] or 0,
        round(stats[2], 2) if stats[2] else 0,
        stats[3] or 0,
        stats[4] or 0,
    )


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/gallery')
def gallery():
    """Render the gallery view with filters, sorting, and category counts."""
    category_name = request.args.get('category')
    sort = request.args.get('sort')
    search = request.args.get('search')

    # Use a join to connect Outfits to Categories for accurate category filtering
    stmt = select(Outfit).join(Category).filter(Outfit.quantity > 0)

    if search:
        stmt = stmt.filter(Outfit.name.ilike(f"%{search}%"))

    if category_name:
        stmt = stmt.filter(Category.name == category_name)

    if sort == 'asc':
        stmt = stmt.order_by(Outfit.name.asc())
    elif sort == 'desc':
        stmt = stmt.order_by(Outfit.name.desc())

    # Provide a category list for sidebar filters and current selection highlighting

    outfits = db.session.scalars(stmt).all()

    category_counts = get_category_counts(Outfit.quantity > 0)
    stats = get_stock_stats(Outfit.quantity > 0)

    results = db.session.scalars(
        select(Outfit)
        .options(joinedload(Outfit.category))
        .join(Category)
        .filter(Outfit.quantity > 0)
    ).all()

    categories = get_category_choices()

    return render_template(
        'gallery.html',
        outfits=outfits,
        category_counts=category_counts,
        stats=stats,
        results=results,
        categories=categories,
        selected_category=category_name
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new outfit and create or reuse the selected category."""
    if request.method == 'POST':
        name = request.form['name'].strip()
        category_name = request.form['category'].strip()
        description = request.form.get('description', '').strip()
        image_url = request.form['image_url'].strip()
        quantity = int(request.form.get('quantity', 0))
        price = float(request.form.get('price', 0.0))

        category = get_or_create_category(category_name)

        if not category:
            return render_template('add_outfit.html', categories=get_category_choices(), error="Category is required")

        existing = db.session.scalars(
            select(Outfit).filter_by(name=name, category_id=category.name)
        ).first()

        if existing:
            # If the same outfit exists, update stock and pricing
            existing.quantity += quantity
            existing.price = price
            existing.description = description
            existing.image_url = image_url
        else:
            # Create a new Outfit record and associate it with its Category
            new_outfit = Outfit(
                name=name,
                description=description,
                image_url=image_url,
                quantity=quantity,
                price=price,
                category=category
            )
            db.session.add(new_outfit)

        db.session.commit()
        return redirect('/gallery')

    return render_template('add_outfit.html', categories=get_category_choices())


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_outfit(id):
    """Edit an existing outfit and update its category if needed."""
    outfit = db.session.get(Outfit, id)
    if not outfit:
        abort(404)

    if request.method == 'POST':
        outfit.name = request.form['name'].strip()
        category_name = request.form['category'].strip()
        outfit.description = request.form.get('description', '').strip()
        outfit.image_url = request.form['image_url'].strip()
        outfit.quantity = int(request.form.get('quantity', 0))
        outfit.price = float(request.form.get('price', 0.0))

        category = get_or_create_category(category_name)
        if category:
            outfit.category = category

        db.session.commit()
        return redirect('/gallery')

    return render_template('edit_outfit.html', outfit=outfit, categories=get_category_choices())


@app.route('/delete/<int:id>')
def delete(id):
    outfit = db.session.get(Outfit, id)
    if not outfit:
        abort(404)
    db.session.delete(outfit)
    db.session.commit()
    return redirect('/gallery')


@app.route('/dispatch/<int:id>', methods=['POST'])
def dispatch(id):
    """Decrease an outfit stock level when it is dispatched."""
    outfit = db.session.get(Outfit, id)
    if not outfit:
        abort(404)
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
    """Display outfits with stock above the average level."""
    avg = db.session.execute(select(func.avg(Outfit.quantity))).scalar() or 0

    outfits = db.session.scalars(
        select(Outfit)
        .join(Category)
        .filter(
            Outfit.quantity > avg,
            Outfit.quantity > 0
        )
    ).all()

    category_counts = get_category_counts(Outfit.quantity > avg)
    stats = get_stock_stats(Outfit.quantity > avg)

    results = db.session.scalars(
        select(Outfit)
        .options(joinedload(Outfit.category))
        .join(Category)
        .filter(Outfit.quantity > avg)
    ).all()

    categories = get_category_choices()

    return render_template(
        'gallery.html',
        outfits=outfits,
        highlight="High Stock (Above Average)",
        avg_quantity=round(avg, 2),
        category_counts=category_counts,
        stats=stats,
        results=results,
        categories=categories,
        selected_category=None
    )
@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/api/add-outfit', methods=['POST'])
def add_outfit_api():
    """Create an outfit record from a JSON API request."""
    data = request.get_json()

    name = data.get('name')
    category_name = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    if not name or not category_name:
        return jsonify({"error": "Name and category required"}), 400

    if quantity is None or quantity < 0:
        return jsonify({"error": "Invalid quantity"}), 400

    if price is None or price < 0:
        return jsonify({"error": "Invalid price"}), 400

    category = get_or_create_category(category_name)
    outfit = Outfit(
        name=name,
        description=data.get('description'),
        image_url=data.get('image_url'),
        quantity=quantity,
        price=price,
        category=category
    )

    db.session.add(outfit)
    db.session.commit()

    return jsonify({"message": "Outfit added successfully"})


if __name__ == '__main__':
    app.run(debug=True)