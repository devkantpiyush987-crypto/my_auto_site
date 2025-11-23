from flask import Flask, render_template, request, redirect, url_for
from models import db, Brand, Model, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Attach database to app
db.init_app(app)

# Create DB tables at startup (Flask 3.x compatible)
with app.app_context():
    init_db(app)


@app.route('/')
def index():
    return render_template('index.html')


# ------------------------------
# BRAND ROUTES
# ------------------------------

# List all brands
@app.route('/brands')
def brands():
    all_brands = Brand.query.order_by(Brand.name).all()
    return render_template('brands.html', brands=all_brands)


# Add a new brand
@app.route('/brands/add', methods=['GET', 'POST'])
def add_brand():
    if request.method == 'POST':
        name = request.form.get('name')
        country = request.form.get('country')
        if name:
            new_brand = Brand(name=name, country=country)
            db.session.add(new_brand)
            db.session.commit()
            return redirect(url_for('brands'))
    return render_template('add_brand.html')


# ------------------------------
# MODEL ROUTES
# ------------------------------

# List all models of a brand
@app.route('/brands/<int:brand_id>/models')
def brand_models(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    models = Model.query.filter_by(brand_id=brand.id).order_by(Model.name).all()
    return render_template('models.html', brand=brand, models=models)


# Add a model for a specific brand
@app.route('/brands/<int:brand_id>/models/add', methods=['GET', 'POST'])
def add_model(brand_id):
    brand = Brand.query.get_or_404(brand_id)

    if request.method == 'POST':
        name = request.form.get('name')
        ncap = request.form.get('ncap')
        stopping = request.form.get('stopping_distance')
        turning = request.form.get('turning_radius')

        if name:
            new_model = Model(
                name=name,
                ncap_rating=ncap or None,
                stopping_distance=stopping or None,
                turning_radius=turning or None,
                brand_id=brand.id
            )
            db.session.add(new_model)
            db.session.commit()
            return redirect(url_for('brand_models', brand_id=brand.id))

    return render_template('add_model.html', brand=brand)


# ------------------------------
# Run app
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
