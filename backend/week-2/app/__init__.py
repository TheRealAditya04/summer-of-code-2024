from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:winterdsoc@localhost:5432/myproject'

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    # Register Blueprints
    from .routes import product_bp
    from .auth_routes import auth_bp
    app.register_blueprint(product_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Create tables and seed initial admin user
    with app.app_context():
        db.create_all()
        seed_admin_user()

    return app


def seed_admin_user():
    """Create an admin user if none exists."""
    from .models import Staff
    if not Staff.query.filter_by(s_is_admin=True).first():
        admin = Staff(
            s_name='Admin User',
            s_email='admin@example.com',
            s_is_admin=True,
            s_contact=1234567890
        )
        admin.set_password('admin123')  # Add the `set_password` method in your Staff model
        db.session.add(admin)
        db.session.commit()


