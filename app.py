from flask import Flask, render_template, request, redirect
from models import db, Outfit
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

    # 🔍 SEARCH
    if search:
        query = query.filter(Outfit.name.ilike(f"%{search}%"))

    # 🎯 FILTER
    if category:
        query = query.filter(Outfit.category.ilike(f"%{category}%"))

    # 🔢 BETWEEN
    if min_qty and max_qty:
        query = query.filter(
            Outfit.quantity.between(int(min_qty), int(max_qty))
        )

    # 🔤 SORT
    if sort == 'asc':
        query = query.order_by(Outfit.name.asc())
    elif sort == 'desc':
        query = query.order_by(Outfit.name.desc())

    outfits = query.all()

    # 📊 GROUP BY
    category_counts = db.session.query(
        Outfit.category,
        func.count(Outfit.id)
    ).group_by(Outfit.category).all()

    # 📊 AGGREGATES
    stats = db.session.query(
        func.count(Outfit.id),
        func.sum(Outfit.quantity),
        func.avg(Outfit.quantity),
        func.min(Outfit.quantity),
        func.max(Outfit.quantity)
    ).first()

    return render_template(
        'gallery.html',
        outfits=outfits,
        category_counts=category_counts,
        stats=stats
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        outfit = Outfit(
            name=request.form['name'],
            category=request.form['category'],
            description=request.form['description'],
            image_url=request.form['image_url'],
            quantity=int(request.form.get('quantity', 0))
        )
        db.session.add(outfit)
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
        outfit.quantity = int(request.form.get('quantity', 0))  # ✅ FIXED

        db.session.commit()
        return redirect('/gallery')

    return render_template('edit_outfit.html', outfit=outfit)


@app.route('/dispatch/<int:id>', methods=['POST'])
def dispatch(id):
    outfit = Outfit.query.get_or_404(id)

    amount = int(request.form['amount'])

    if amount <= 0:
        return "Invalid quantity"

    if outfit.quantity >= amount:
        outfit.quantity -= amount
        db.session.commit()
    else:
        return "Not enough stock!"

    return redirect('/gallery')


# 🔥 SUBQUERY ROUTE (VERY IMPORTANT FOR MARKS)
@app.route('/high-stock')
def high_stock():
    avg_quantity = db.session.query(
        func.avg(Outfit.quantity)
    ).scalar()

    outfits = Outfit.query.filter(
        Outfit.quantity > avg_quantity
    ).all()

    # ADD THESE 👇
    category_counts = db.session.query(
        Outfit.category,
        func.count(Outfit.id)
    ).group_by(Outfit.category).all()

    stats = db.session.query(
        func.count(Outfit.id),
        func.sum(Outfit.quantity),
        func.avg(Outfit.quantity),
        func.min(Outfit.quantity),
        func.max(Outfit.quantity)
    ).first()

    return render_template(
        'gallery.html',
        outfits=outfits,
        highlight="High Stock (Above Average)",
        avg_quantity=round(avg_quantity, 2),
        category_counts=category_counts,
        stats=stats
    )
if __name__ == '__main__':
    app.run(debug=True)