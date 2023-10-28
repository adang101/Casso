from flask import Flask
from .models import db  # Import your database models

def create_app():
    app = Flask("Casso")

    # Database configuration (if you are using a database)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/alvindang/Documents/GitHub/CMPE133-Grp-21/Casso/Casso_database.db'
    db.init_app(app)

    # Configure the upload folder and allowed extensions
    app.config['UPLOAD_FOLDER'] = '/Users/alvindang/Documents/GitHub/CMPE133-Grp-21/Casso/static/images/userPhotos'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
    
    # Register URL routes (in routes.py)
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

