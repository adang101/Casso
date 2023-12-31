from flask import Flask, g, request
from .models import db  # Import your database models
from flask_migrate import Migrate
import os

def create_app():
    template_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'templates')
    static_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'static')
    print("Template directory:", template_dir)
    app = Flask("Casso", template_folder=template_dir, static_folder=static_dir)
    migrate = Migrate(app, db)

    print("Current working directory:", os.getcwd())
    # Database configuration (if you are using a database)
    db_path = os.path.join(os.path.dirname(__file__), '..', 'Casso_database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)

    # Create the database tables (if they do not exist)
    with app.app_context():
        db.create_all()

    # Configure the upload folder and allowed extensions
    app.config['UPLOAD_FOLDER_PROFILE_PICS'] = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'userPhotos')
    app.config['UPLOAD_FOLDER_POSTS'] = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'userPosts')
    app.config['UPLOAD_FOLDER_CHAT'] = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'userShareables')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
    
    # Register URL routes (in routes.py)
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    @app.before_request
    def before_request():
        g.current_page = request.endpoint  # Set current_page to the endpoint of the current request
        if request.endpoint == '/':
            g.current_page = 'home'  # Set current_page to 'home' for the homepage
        elif request.endpoint == '/home-feed':
            g.current_page = 'home-feed'  # Set current_page to 'home-feed' for the home-feed page
        elif request.endpoint == '/profile':
            g.current_page = 'profile'  # Set current_page to 'profile' for the profile page
        elif request.endpoint == '/create-page': 
            g.current_page = 'create-page'
        elif request.endpoint == '/login':
            g.current_page = 'login'
        elif request.endpoint == '/sign-up':
            g.current_page = 'sign-up'

    return app

