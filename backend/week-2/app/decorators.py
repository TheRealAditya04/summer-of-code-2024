from flask import session, redirect, url_for, flash
from functools import wraps

# Login Required Decorator
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to access this page.', 'warning')
            return redirect(url_for('auth_bp.login'))
        return func(*args, **kwargs)
    return wrapper

# Admin Required Decorator
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin', False):
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('product_bp.list_products'))
        return func(*args, **kwargs)
    return wrapper
