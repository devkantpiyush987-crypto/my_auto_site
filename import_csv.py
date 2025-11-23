# import_csv.py
# Imports brand/model data from models.csv into autos.db

import csv
import os
from flask import Flask
from models import db, Brand, Model, init_db

CSV_FILE = 'models.csv'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def import_csv():
    if not os.path.exists(CSV_FILE):
        print(f"CSV file not found: {CSV_FILE}")
        return

    app = create_app()
    with app.app_context():
        init_db(app)

        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            brand_cache = {}
            added_brands = 0
            added_models = 0

            for row in reader:
                brand_name = row['brand_name'].strip()
                brand_country = row['brand_country'].strip()
                model_name = row['model_name'].strip()
                ncap = row['ncap_rating'].strip()
                stop_dist = row['stopping_distance'].strip()
                turn_rad = row['turning_radius'].strip()

                # Find or create brand
                if brand_name.lower() not in brand_cache:
                    brand = Brand.query.filter_by(name=brand_name).first()
                    if not brand:
                        brand = Brand(name=brand_name, country=brand_country)
                        db.session.add(brand)
                        db.session.flush()
                        added_brands += 1
                    brand_cache[brand_name.lower()] = brand
                else:
                    brand = brand_cache[brand_name.lower()]

                # Check if model exists
                exists = Model.query.filter_by(name=model_name, brand_id=brand.id).first()
                if exists:
                    print(f"Skipping duplicate: {brand_name} - {model_name}")
                    continue

                # Add model
                model = Model(
                    name=model_name,
                    ncap_rating=ncap or None,
                    stopping_distance=stop_dist or None,
                    turning_radius=turn_rad or None,
                    brand_id=brand.id
                )
                db.session.add(model)
                added_models += 1

            db.session.commit()
            print(f"Import complete!")
            print(f"Brands added: {added_brands}")
            print(f"Models added: {added_models}")

if __name__ == "__main__":
    import_csv()
