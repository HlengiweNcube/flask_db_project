from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))