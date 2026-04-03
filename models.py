from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
db = SQLAlchemy()

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # PRIMARY KEY
    name = db.Column(db.String(100), nullable=False)  # NOT NULL
    category = db.Column(db.String(50), nullable=False)  # NOT NULL
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200), nullable=False)  # NOT NULL
    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=0  # DEFAULT
    )
    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
    )