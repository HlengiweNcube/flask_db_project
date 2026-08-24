from flask import Flask, abort, jsonify, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Outfit, Category, User
from sqlalchemy import func, select
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'local-development-change-me')

uri = os.environ.get("DATABASE_URL", "sqlite:///local_test.db")

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

DEFAULT_CATEGORIES = ('Women', 'Men', 'Children', 'Accessories', 'Traditional')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to manage the inventory.'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Load the logged-in user from the users table."""
    return db.session.get(User, int(user_id))


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

    return category


def parse_outfit_values(source):
    """Validate and normalize outfit fields from a form or JSON object."""
    name = str(source.get('name', '')).strip()
    category_name = str(source.get('category', '')).strip()
    image_url = str(source.get('image_url', '')).strip()

    if not name or not category_name or not image_url:
        raise ValueError('Name, category, and image URL are required.')

    try:
        quantity = int(source.get('quantity', 0))
        price = float(source.get('price', 0))
    except (TypeError, ValueError):
        raise ValueError('Quantity must be a whole number and price must be numeric.')

    if quantity < 0 or price < 0:
        raise ValueError('Quantity and price cannot be negative.')

    return {
        'name': name,
        'category_name': category_name,
        'description': str(source.get('description', '')).strip(),
        'image_url': image_url,
        'quantity': quantity,
        'price': price,
    }


def get_category_choices():
    """Return database categories for templates."""
    return db.session.scalars(
        select(Category).order_by(Category.name)
    ).all()


def get_category_options():
    """Return default and previously created categories for dropdowns."""
    existing_names = {category.name for category in get_category_choices()}
    return sorted(existing_names.union(DEFAULT_CATEGORIES))


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Create a user account with a securely hashed password."""
    if current_user.is_authenticated:
        return redirect(url_for('gallery'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or len(password) < 8:
            return render_template('register.html', error='Username is required and password must be at least 8 characters.'), 400
        if db.session.scalar(select(User).where(User.username == username)):
            return render_template('register.html', error='That username is already registered.'), 400

        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('gallery'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate a user before allowing inventory management."""
    if current_user.is_authenticated:
        return redirect(url_for('gallery'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = db.session.scalar(select(User).where(User.username == username))
        if not user or not check_password_hash(user.password_hash, password):
            return render_template('login.html', error='Invalid username or password.'), 401
        login_user(user)
        return redirect(request.args.get('next') or url_for('gallery'))

    return render_template('login.html')


@app.post('/logout')
@login_required
def logout():
    """End the current authenticated session."""
    logout_user()
    return redirect(url_for('home'))


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

    categories = get_category_choices()

    return render_template(
        'gallery.html',
        outfits=outfits,
        category_counts=category_counts,
        stats=stats,
        categories=categories,
        selected_category=category_name
    )


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add a new outfit and create or reuse the selected category."""
    if request.method == 'POST':
        try:
            values = parse_outfit_values(request.form)
        except ValueError as error:
            return render_template('add_outfit.html', categories=get_category_options(), error=str(error)), 400

        category = get_or_create_category(values['category_name'])

        if not category:
            return render_template('add_outfit.html', categories=get_category_options(), error="Category is required")

        existing = db.session.scalars(
            select(Outfit).filter_by(name=values['name'], category_id=category.id)
        ).first()

        if existing:
            # If the same outfit exists, update stock and pricing
            existing.quantity += values['quantity']
            existing.price = values['price']
            existing.description = values['description']
            existing.image_url = values['image_url']
        else:
            # Create a new Outfit record and associate it with its Category
            new_outfit = Outfit(
                name=values['name'],
                description=values['description'],
                image_url=values['image_url'],
                quantity=values['quantity'],
                price=values['price'],
                category=category
            )
            db.session.add(new_outfit)

        db.session.commit()
        return redirect('/gallery')

    return render_template('add_outfit.html', categories=get_category_options())


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_outfit(id):
    """Edit an existing outfit and update its category if needed."""
    outfit = db.session.get(Outfit, id)
    if not outfit:
        abort(404)

    if request.method == 'POST':
        try:
            values = parse_outfit_values(request.form)
        except ValueError as error:
            return render_template('edit_outfit.html', outfit=outfit, categories=get_category_options(), error=str(error)), 400

        outfit.name = values['name']
        outfit.description = values['description']
        outfit.image_url = values['image_url']
        outfit.quantity = values['quantity']
        outfit.price = values['price']
        outfit.category = get_or_create_category(values['category_name'])

        db.session.commit()
        return redirect('/gallery')

    return render_template('edit_outfit.html', outfit=outfit, categories=get_category_options())


@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    outfit = db.session.get(Outfit, id)
    if not outfit:
        abort(404)
    db.session.delete(outfit)
    db.session.commit()
    return redirect('/gallery')


@app.route('/dispatch/<int:id>', methods=['POST'])
@login_required
def dispatch(id):
    """Decrease an outfit stock level when it is dispatched."""
    outfit = db.session.get(Outfit, id)
    if not outfit:
        abort(404)
    amount = request.form.get('amount')

    if not amount:
        return "Enter quantity"

    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return "Quantity must be a whole number", 400

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

    categories = get_category_choices()

    return render_template(
        'gallery.html',
        outfits=outfits,
        highlight="High Stock (Above Average)",
        avg_quantity=round(avg, 2),
        category_counts=category_counts,
        stats=stats,
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
@login_required
def add_outfit_api():
    """Create an outfit record from a JSON API request."""
    data = request.get_json(silent=True) or {}
    try:
        values = parse_outfit_values(data)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    category = get_or_create_category(values['category_name'])
    outfit = Outfit(
        name=values['name'],
        description=values['description'],
        image_url=values['image_url'],
        quantity=values['quantity'],
        price=values['price'],
        category=category
    )

    db.session.add(outfit)
    db.session.commit()

    return jsonify({"message": "Outfit added successfully"})


@app.cli.command('init-db')
def init_db_command():
    """Create database tables for a new local or hosted database."""
    with app.app_context():
        db.create_all()
    print('Database tables created.')


if __name__ == '__main__':
    app.run(debug=True)