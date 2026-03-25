from flask import Flask, render_template
from models import db, Outfit

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Amanda%40123@localhost:5432/african_fashion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template("home.html")

with app.app_context():
    test = Outfit(name="Test", category="Ankara", description="Test desc", image_url="https://via.placeholder.com/150")
    db.session.add(test)
    db.session.commit()

@app.route('/gallery')
def gallery():
    outfits = Outfit.query.all()
    print(outfits)  # DEBUG LINE
    return render_template('gallery.html', outfits=outfits)

from flask import request, redirect
from models import Outfit, db

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        outfit = Outfit(
            name=request.form['name'],
            category=request.form['category'],
            description=request.form['description'],
            image_url=request.form['image_url']
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
    outfit = Outfit.query.get(id)
    db.session.delete(outfit)
    db.session.commit()
    return redirect('/gallery')

if __name__ == '__main__':
    app.run(debug=True)