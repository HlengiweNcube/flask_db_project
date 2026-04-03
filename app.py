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

    #  NEW (BETWEEN example)
    min_qty = request.args.get('min_qty')
    max_qty = request.args.get('max_qty')

    query = Outfit.query

    # LIKE (SEARCH)
    if search:
        query = query.filter(Outfit.name.ilike(f"%{search}%"))

    #  WHERE (FILTER)
    if category:
        query = query.filter(Outfit.category.ilike(f"%{category}%"))

    #  BETWEEN (NEW)
    if min_qty and max_qty:
        query = query.filter(
            Outfit.quantity.between(int(min_qty), int(max_qty))
        )

    # Example: show only certain categories
    # query = query.filter(Outfit.category.in_(["Women", "Men"]))

    #  ORDER BY
    if sort == 'asc':
        query = query.order_by(Outfit.name.asc())
    elif sort == 'desc':
        query = query.order_by(Outfit.name.desc())

    outfits = query.all()

    #  GROUP BY + COUNT
    category_counts = db.session.query(
        Outfit.category,
        func.count(Outfit.id)
    ).group_by(Outfit.category).all()

    #  HAVING (ADVANCED)
    category_counts_filtered = db.session.query(
        Outfit.category,
        func.count(Outfit.id).label("total")
    ).group_by(Outfit.category)\
     .having(func.count(Outfit.id) > 0)\
     .all()

    #  AGGREGATE FUNCTIONS (BIG MARKS)
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
        category_counts_filtered=category_counts_filtered,
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
           quantity = int(request.form.get('quantity', 0))
        )
        db.session.add(outfit)
        db.session.commit()
        return redirect('/gallery')

    return render_template('add_outfit.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/delete/<int:id>')
def delete(id):
    outfit = Outfit.query.get_or_404(id)
    db.session.delete(outfit)
    db.session.commit()
    return redirect('/gallery')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    outfit = Outfit.query.get(id)

    if request.method == 'POST':
        outfit.name = request.form['name']
        outfit.category = request.form['category']
        outfit.description = request.form['description']
        outfit.image_url = request.form['image_url']
        quantity=int(request.form.get('quantity', 0)) 

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


    outfits = Outfit.query.filter_by(category=category).all()

    for outfit in outfits:
        if outfit.quantity >= amount:
            outfit.quantity -= amount
            

    db.session.commit()

    return redirect('/gallery')

if __name__ == '__main__':
    app.run(debug=True)