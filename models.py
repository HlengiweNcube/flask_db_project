from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

# ✅ CATEGORY TABLE
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Category {self.name}>"

# ✅ OUTFIT TABLE
class Outfit(db.Model):
    __tablename__ = 'outfits'

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # KEEP your old column (as you decided)
    category = db.Column(db.String(50), nullable=False)

    description = db.Column(db.Text)
    image_url = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
 
    def __repr__(self):
        return f"<Outfit {self.name}>"
    
class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    # 
    price = db.Column(db.Float, nullable=False, default=0.0)

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
        CheckConstraint('price >= 0', name='check_price_positive')  # BONUS MARKS 🔥
    )