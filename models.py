from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Application user allowed to manage inventory records."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

# ✅ CATEGORY TABLE
class Category(db.Model):
    """Reusable clothing category (e.g. Women, Traditional).

    Normalised into its own table so category names stay consistent
    across all outfits and can be managed independently.
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relationship: one category → many outfits
    outfits = db.relationship('Outfit', back_populates='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

# ✅ OUTFIT TABLE
class Outfit(db.Model):
    """A single clothing item held in inventory.

    quantity and price are constrained to >= 0 at the database level
    so invalid data cannot be inserted even outside the application.
    """
    __tablename__ = 'outfits'

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
        CheckConstraint('price >= 0', name='check_price_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='outfits')

    @property
    def category_name(self):
        return self.category.name if self.category else 'Uncategorized'

    def __repr__(self):
        return f"<Outfit {self.name}>"