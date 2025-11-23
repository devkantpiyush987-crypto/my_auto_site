from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120))
    models = db.relationship('Model', backref='brand', cascade='all, delete-orphan')

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    ncap_rating = db.Column(db.String(20))
    stopping_distance = db.Column(db.String(50))
    turning_radius = db.Column(db.String(50))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)

def init_db(app):
    """
    Call init_db(app) once (inside app) to create the database tables.
    It uses the app's SQLALCHEMY_DATABASE_URI setting.
    """
    with app.app_context():
        db.create_all()
