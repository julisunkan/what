
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
        form_type = request.form.get('form_type')
        
        if form_type == 'appearance':
            theme = request.form.get('theme', 'light')
            session['theme'] = theme
            flash('Appearance settings updated!', 'success')
        
        elif form_type == 'api':
            whatsapp_provider = request.form.get('whatsapp_provider', 'meta')
            user.whatsapp_provider = whatsapp_provider
            
            if whatsapp_provider == 'meta':
                meta_access_token = request.form.get('meta_access_token', '').strip()
                meta_phone_number_id = request.form.get('meta_phone_number_id', '').strip()
                meta_api_version = request.form.get('meta_api_version', 'v21.0').strip()
                
                if meta_access_token or meta_phone_number_id:
                    user.set_meta_credentials(
                        meta_access_token if meta_access_token else None,
                        meta_phone_number_id if meta_phone_number_id else None,
                        meta_api_version if meta_api_version else 'v21.0'
                    )
                    db.session.commit()
                    flash('Meta Cloud API credentials saved successfully!', 'success')
                else:
                    flash('Please provide both Access Token and Phone Number ID for Meta API.', 'warning')
                    
            elif whatsapp_provider == 'twilio':
                twilio_account_sid = request.form.get('twilio_account_sid', '').strip()
                twilio_auth_token = request.form.get('twilio_auth_token', '').strip()
                twilio_whatsapp_number = request.form.get('twilio_whatsapp_number', '').strip()
                
                if twilio_account_sid or twilio_auth_token:
                    user.set_twilio_credentials(
                        twilio_account_sid if twilio_account_sid else None,
                        twilio_auth_token if twilio_auth_token else None,
                        twilio_whatsapp_number if twilio_whatsapp_number else None
                    )
                    db.session.commit()
                    flash('Twilio credentials saved successfully!', 'success')
                else:
                    flash('Please provide both Account SID and Auth Token for Twilio.', 'warning')
            
            db.session.commit()
        
        elif form_type == 'notifications':
            email_notifications = request.form.get('email_notifications') == 'on'
            session['email_notifications'] = email_notifications
            flash('Notification settings updated!', 'success')
        
        return redirect(url_for('settings.settings'))
    
    current_theme = session.get('theme', 'light')
    current_provider = user.whatsapp_provider if user.whatsapp_provider else 'meta'
    email_notifications = session.get('email_notifications', True)
    
    meta_credentials = user.get_meta_credentials()
    twilio_credentials = user.get_twilio_credentials()
    
    env_status = {
        'meta_configured': user.has_meta_credentials(),
        'twilio_configured': user.has_twilio_credentials(),
        'session_secret': bool(os.environ.get('SESSION_SECRET'))
    }
    
    return render_template('settings.html', 
                         user=user, 
                         current_theme=current_theme,
                         current_provider=current_provider,
                         email_notifications=email_notifications,
                         env_status=env_status,
                         meta_credentials=meta_credentials,
                         twilio_credentials=twilio_credentials)
