from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import check_password_hash
from .models import Staff
from . import db

auth_bp = Blueprint('auth_bp', __name__)

# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle None values and strip whitespace
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Validate empty inputs
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('auth/login.html')

        print(f"Login Attempt - Email: {email}, Password: {password}")  # Debugging

        # Query the database
        staff = Staff.query.filter_by(s_email=email).first()
        print(f"Staff Found: {staff}")  # Debugging

        if staff:
            print(f"Stored Password Hash: {staff.password_hash}")  # Debugging

            if check_password_hash(staff.password_hash, password):
                # Set session variables
                session['user_id'] = staff.s_id
                session['is_admin'] = staff.s_is_admin
                session['username'] = staff.s_name

                flash(f'Welcome, {staff.s_name}!', 'success')
                print(f"Login Successful for {staff.s_name}")  # Debugging
                return redirect(url_for('product_bp.list_products'))
            else:
                print("Password does not match.")  # Debugging
        else:
            print("No user found with the provided email.")  # Debugging

        # If email or password is invalid
        flash('Invalid email or password', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'info')  # Flash a logout message
    return redirect(url_for('auth_bp.login'))  # Redirect to the login page

