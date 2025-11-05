
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.user import User
import os

settings_bp = Blueprint('settings', __name__)

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = User.query.get(session['user_id'])
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        session.clear()
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        # Handle different form submissions
        form_type = request.form.get('form_type')
        
        if form_type == 'appearance':
            # Store theme preference in session
            theme = request.form.get('theme', 'light')
            session['theme'] = theme
            flash('Appearance settings updated!', 'success')
        
        elif form_type == 'api':
            # Update API configuration in session/user preferences
            whatsapp_provider = request.form.get('whatsapp_provider', 'meta')
            session['whatsapp_provider'] = whatsapp_provider
            flash('API settings updated!', 'success')
        
        elif form_type == 'notifications':
            # Store notification preferences
            email_notifications = request.form.get('email_notifications') == 'on'
            session['email_notifications'] = email_notifications
            flash('Notification settings updated!', 'success')
        
        return redirect(url_for('settings.settings'))
    
    # Get current settings
    current_theme = session.get('theme', 'light')
    current_provider = session.get('whatsapp_provider', os.environ.get('WHATSAPP_PROVIDER', 'meta'))
    email_notifications = session.get('email_notifications', True)
    
    # Get environment variables status
    env_status = {
        'meta_configured': bool(os.environ.get('META_WHATSAPP_TOKEN')),
        'twilio_configured': bool(os.environ.get('TWILIO_ACCOUNT_SID')),
        'session_secret': bool(os.environ.get('SESSION_SECRET'))
    }
    
    return render_template('settings.html', 
                         user=user, 
                         current_theme=current_theme,
                         current_provider=current_provider,
                         email_notifications=email_notifications,
                         env_status=env_status)
