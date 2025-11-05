from flask import Blueprint, request, jsonify
from models import db
from models.bot import Bot
from models.rule import Rule
from models.message_log import MessageLog

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    
    if not data or 'sender' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    sender = data['sender']
    message = data['message'].strip()
    bot_id = data.get('bot_id')
    
    if bot_id:
        active_bot = Bot.query.filter_by(id=bot_id, active=True).first()
    else:
        active_bot = Bot.query.filter_by(active=True).first()
    
    if not active_bot:
        return jsonify({'response': 'No active bot found'}), 404
    
    incoming_log = MessageLog(
        bot_id=active_bot.id,
        sender=sender,
        direction='incoming',
        message=message
    )
    db.session.add(incoming_log)
    
    response_text = active_bot.fallback_message
    
    rules = Rule.query.filter_by(bot_id=active_bot.id).all()
    for rule in rules:
        if rule.keyword.lower() in message.lower():
            response_text = rule.response
            break
    
    outgoing_log = MessageLog(
        bot_id=active_bot.id,
        sender=sender,
        direction='outgoing',
        message=response_text
    )
    db.session.add(outgoing_log)
    db.session.commit()
    
    return jsonify({'response': response_text})
