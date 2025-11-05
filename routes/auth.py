from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('bots.dashboard'))
    return render_template('index.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if not username or not password:
        flash('Username and password are required', 'danger')
        return redirect(url_for('auth.index'))
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'danger')
        return redirect(url_for('auth.index'))
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    session['user_id'] = user.id
    session['username'] = user.username
    flash('Account created successfully!', 'success')
    return redirect(url_for('bots.dashboard'))

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Welcome back!', 'success')
        return redirect(url_for('bots.dashboard'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('auth.index'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.index'))
