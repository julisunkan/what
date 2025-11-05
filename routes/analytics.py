from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db
from models.bot import Bot
from models.message_log import MessageLog
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@analytics_bp.route('/analytics')
@login_required
def analytics():
    user_bots = Bot.query.filter_by(user_id=session['user_id']).all()
    
    bot_stats = []
    for bot in user_bots:
        total_messages = MessageLog.query.filter_by(bot_id=bot.id).count()
        incoming = MessageLog.query.filter_by(bot_id=bot.id, direction='incoming').count()
        outgoing = MessageLog.query.filter_by(bot_id=bot.id, direction='outgoing').count()
        
        unique_senders = db.session.query(
            func.count(func.distinct(MessageLog.sender))
        ).filter_by(bot_id=bot.id).scalar()
        
        bot_stats.append({
            'bot': bot,
            'total_messages': total_messages,
            'incoming': incoming,
            'outgoing': outgoing,
            'unique_senders': unique_senders
        })
    
    return render_template('analytics.html', bot_stats=bot_stats)
