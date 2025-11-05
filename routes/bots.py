from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.bot import Bot
from models.rule import Rule
from models.user import User

bots_bp = Blueprint('bots', __name__)

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@bots_bp.route('/guide')
@login_required
def guide():
    return render_template('guide.html')

@bots_bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        session.clear()
        return redirect(url_for('auth.index'))
    
    bots = Bot.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', bots=bots, user=user)

@bots_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    
    if not user:
        flash('User not found. Please login again.', 'danger')
        session.clear()
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        phone_number = request.form.get('phone_number', '').strip()
        user.phone_number = phone_number if phone_number else None
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('bots.dashboard'))
    
    return render_template('profile.html', user=user)

@bots_bp.route('/bot/create', methods=['POST'])
@login_required
def create_bot():
    name = request.form.get('name', '').strip()
    fallback_message = request.form.get('fallback_message', '').strip()
    
    if not name:
        flash('Bot name is required', 'danger')
        return redirect(url_for('bots.dashboard'))
    
    if not fallback_message:
        fallback_message = 'Sorry, I did not understand that.'
    
    bot = Bot(
        user_id=session['user_id'],
        name=name,
        fallback_message=fallback_message,
        active=True
    )
    db.session.add(bot)
    db.session.commit()
    
    flash(f'Bot "{name}" created successfully!', 'success')
    return redirect(url_for('bots.dashboard'))

@bots_bp.route('/bot/<int:bot_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_bot(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    
    if bot.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('bots.dashboard'))
    
    if request.method == 'POST':
        bot.name = request.form.get('name', '').strip()
        bot.fallback_message = request.form.get('fallback_message', '').strip()
        bot.active = request.form.get('active') == 'on'
        
        db.session.commit()
        flash(f'Bot "{bot.name}" updated successfully!', 'success')
        return redirect(url_for('bots.dashboard'))
    
    rules = Rule.query.filter_by(bot_id=bot_id).all()
    return render_template('edit_bot.html', bot=bot, rules=rules)

@bots_bp.route('/bot/<int:bot_id>/delete', methods=['POST'])
@login_required
def delete_bot(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    
    if bot.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('bots.dashboard'))
    
    bot_name = bot.name
    db.session.delete(bot)
    db.session.commit()
    
    flash(f'Bot "{bot_name}" deleted successfully!', 'success')
    return redirect(url_for('bots.dashboard'))

@bots_bp.route('/bot/<int:bot_id>/rule/add', methods=['POST'])
@login_required
def add_rule(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    
    if bot.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('bots.dashboard'))
    
    keyword = request.form.get('keyword', '').strip()
    response = request.form.get('response', '').strip()
    
    if not keyword or not response:
        flash('Keyword and response are required', 'danger')
        return redirect(url_for('bots.edit_bot', bot_id=bot_id))
    
    rule = Rule(bot_id=bot_id, keyword=keyword, response=response)
    db.session.add(rule)
    db.session.commit()
    
    flash(f'Rule added successfully!', 'success')
    return redirect(url_for('bots.edit_bot', bot_id=bot_id))

@bots_bp.route('/rule/<int:rule_id>/delete', methods=['POST'])
@login_required
def delete_rule(rule_id):
    rule = Rule.query.get_or_404(rule_id)
    bot = Bot.query.get_or_404(rule.bot_id)
    
    if bot.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('bots.dashboard'))
    
    db.session.delete(rule)
    db.session.commit()
    
    flash('Rule deleted successfully!', 'success')
    return redirect(url_for('bots.edit_bot', bot_id=bot.id))
