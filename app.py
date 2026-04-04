from flask import Flask, render_template, request, redirect
from models import db, Outfit, Category
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Amanda%40123@localhost:5432/african_fashion'
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
    min_qty = request.args.get('min_qty')
    max_qty = request.args.get('max_qty')

    query = Outfit.query

    # SEARCH (LIKE)
    if search:
        query = query.filter(Outfit.name.ilike(f"%{search}%"))

    #  FILTER (WHERE)
    if category:
        query = query.filter(Outfit.category.ilike(f"%{category}%"))

    #  BETWEEN
    if min_qty and max_qty:
        query = query.filter(
            Outfit.quantity.between(int(min_qty), int(max_qty))
        )

    #  SORT (ORDER BY)
    if sort == 'asc':
        query = query.order_by(Outfit.name.asc())
    elif sort == 'desc':
        query = query.order_by(Outfit.name.desc())

    outfits = query.all()

    # GROUP BY
    category_counts = db.session.query(
        Outfit.category,
        func.count(Outfit.id)
    ).group_by(Outfit.category).all()

    # AGGREGATES
    stats = db.session.query(
        func.count(Outfit.id),
        func.sum(Outfit.quantity),
        func.avg(Outfit.quantity),
        func.min(Outfit.quantity),
        func.max(Outfit.quantity)
    ).first()

    # JOIN for demo
    results = db.session.query(
        Outfit.name,
        Category.name
    ).join(Category, Outfit.category == Category.name).all()

    return render_template(
        'gallery.html',
        outfits=outfits,
        category_counts=category_counts,
        stats=stats,
        results=results
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        # ✅ GET DATA FROM FORM
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        image_url = request.form['image_url']
        quantity = int(request.form.get('quantity', 0))
        price = float(request.form.get('price', 0.0))

        # 🔍 CHECK IF EXISTS
        existing_outfit = Outfit.query.filter_by(
            name=name,
            category=category
        ).first()

        if existing_outfit:
            # ✅ UPDATE
            existing_outfit.quantity += quantity
            existing_outfit.price = price
        else:
            # ✅ CREATE NEW
            new_outfit = Outfit(
                name=name,
                category=category,
                description=description,
                image_url=image_url,
                quantity=quantity,
                price=price
            )
            db.session.add(new_outfit)

        db.session.commit()
        return redirect('/gallery')

    return render_template('add_outfit.html')


@app.route('/delete/<int:id>')
def delete(id):
    outfit = Outfit.query.get_or_404(id)
    db.session.delete(outfit)
    db.session.commit()
    return redirect('/gallery')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    outfit = Outfit.query.get_or_404(id)

    if request.method == 'POST':
        outfit.name = request.form['name']
        outfit.category = request.form['category']
        outfit.description = request.form['description']
        outfit.image_url = request.form['image_url']
        outfit.quantity = int(request.form.get('quantity', 0))

        db.session.commit()
        return redirect('/gallery')

    return render_template('edit_outfit.html', outfit=outfit)
@app.route('/dispatch/<int:id>', methods=['POST'])
def dispatch(id):
    outfit = Outfit.query.get_or_404(id)

    amount = request.form.get('amount')

    # ✅ HANDLE EMPTY INPUT
    if not amount:
        return "Please enter a quantity"

    amount = int(amount)

    # ✅ VALIDATION
    if amount <= 0:
        return "Invalid quantity"

    if outfit.quantity < amount:
        return "Not enough stock!"

    # ✅ UPDATE
    outfit.quantity -= amount
    db.session.commit()

    return redirect('/gallery')


#  SUBQUERY (VERY IMPORTANT FOR MARKS)
@app.route('/high-stock')
def high_stock():
    avg_quantity = db.session.query(
        func.avg(Outfit.quantity)
    ).scalar()

    avg_quantity = avg_quantity or 0
    avg_quantity = round(avg_quantity, 2)

    outfits = Outfit.query.filter(
        Outfit.quantity > avg_quantity
    ).all()

    # GROUP BY (only high stock)
    category_counts = db.session.query(
        Outfit.category,
        func.count(Outfit.id)
    ).filter(
        Outfit.quantity > avg_quantity
    ).group_by(Outfit.category).all()

    # AGGREGATES (only high stock)
    stats = db.session.query(
        func.count(Outfit.id),
        func.sum(Outfit.quantity),
        func.avg(Outfit.quantity),
        func.min(Outfit.quantity),
        func.max(Outfit.quantity)
    ).filter(
        Outfit.quantity > avg_quantity
    ).first()

    # HANDLE NULLS
    stats = (
        stats[0] or 0,
        stats[1] or 0,
        round(stats[2], 2) if stats[2] else 0,
        stats[3] or 0,
        stats[4] or 0
    )

    # JOIN for demo
    results = db.session.query(
        Outfit.name,
        Category.name
    ).join(Category, Outfit.category == Category.name).filter(
        Outfit.quantity > avg_quantity
    ).all()

    return render_template(
        'gallery.html',
        outfits=outfits,
        highlight="High Stock (Above Average)",
        avg_quantity=avg_quantity,
        category_counts=category_counts,
        stats=stats,
        results=results
    )
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)