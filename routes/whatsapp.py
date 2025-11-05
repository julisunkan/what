import os
import hashlib
import hmac
from flask import Blueprint, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from models import db
from models.bot import Bot
from models.rule import Rule
from models.message_log import MessageLog
from services.whatsapp_service import WhatsAppService

whatsapp_bp = Blueprint('whatsapp', __name__, url_prefix='/whatsapp')
whatsapp_service = WhatsAppService()

def validate_twilio_request():
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    if not auth_token:
        return True
    
    validator = RequestValidator(auth_token)
    url = request.url
    signature = request.headers.get('X-Twilio-Signature', '')
    params = request.form.to_dict()
    
    return validator.validate(url, params, signature)

def validate_meta_signature():
    app_secret = os.environ.get('META_APP_SECRET')
    if not app_secret:
        return True
    
    signature = request.headers.get('X-Hub-Signature-256', '')
    if not signature:
        return False
    
    expected_signature = 'sha256=' + hmac.new(
        app_secret.encode('utf-8'),
        request.get_data(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

@whatsapp_bp.route('/webhook/twilio', methods=['POST'])
def twilio_webhook():
    if not validate_twilio_request():
        return 'Unauthorized', 403
    
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    
    active_bot = Bot.query.filter_by(active=True).first()
    
    if not active_bot:
        response = MessagingResponse()
        response.message('No active bot found. Please contact administrator.')
        return str(response)
    
    incoming_log = MessageLog(
        bot_id=active_bot.id,
        sender=from_number,
        direction='incoming',
        message=incoming_msg
    )
    db.session.add(incoming_log)
    
    response_text = active_bot.fallback_message
    
    rules = Rule.query.filter_by(bot_id=active_bot.id).all()
    for rule in rules:
        if rule.keyword.lower() in incoming_msg.lower():
            response_text = rule.response
            break
    
    outgoing_log = MessageLog(
        bot_id=active_bot.id,
        sender=from_number,
        direction='outgoing',
        message=response_text
    )
    db.session.add(outgoing_log)
    db.session.commit()
    
    response = MessagingResponse()
    response.message(response_text)
    
    return str(response)

@whatsapp_bp.route('/webhook/meta', methods=['GET', 'POST'])
def meta_webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        verify_token = os.environ.get('META_VERIFY_TOKEN')
        
        if not verify_token:
            print('ERROR: META_VERIFY_TOKEN not configured')
            return 'Server configuration error', 500
        
        if mode == 'subscribe' and token == verify_token:
            return challenge, 200
        else:
            return 'Forbidden', 403
    
    elif request.method == 'POST':
        if not validate_meta_signature():
            return 'Unauthorized', 403
        
        data = request.get_json()
        
        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            
            if 'messages' in value:
                message = value['messages'][0]
                from_number = message['from']
                message_body = message.get('text', {}).get('body', '')
                
                active_bot = Bot.query.filter_by(active=True).first()
                
                if not active_bot:
                    return jsonify({'status': 'error', 'message': 'No active bot'}), 404
                
                incoming_log = MessageLog(
                    bot_id=active_bot.id,
                    sender=from_number,
                    direction='incoming',
                    message=message_body
                )
                db.session.add(incoming_log)
                
                response_text = active_bot.fallback_message
                
                rules = Rule.query.filter_by(bot_id=active_bot.id).all()
                for rule in rules:
                    if rule.keyword.lower() in message_body.lower():
                        response_text = rule.response
                        break
                
                outgoing_log = MessageLog(
                    bot_id=active_bot.id,
                    sender=from_number,
                    direction='outgoing',
                    message=response_text
                )
                db.session.add(outgoing_log)
                db.session.commit()
                
                try:
                    whatsapp_service.send_message(from_number, response_text)
                except Exception as e:
                    print(f'Error sending message: {e}')
                
                return jsonify({'status': 'success'}), 200
        
        except Exception as e:
            print(f'Webhook error: {e}')
            return jsonify({'status': 'error', 'message': str(e)}), 500
        
        return jsonify({'status': 'ok'}), 200

@whatsapp_bp.route('/test', methods=['POST'])
def test_send():
    data = request.get_json()
    to_number = data.get('to')
    message = data.get('message')
    
    if not to_number or not message:
        return jsonify({'error': 'Missing to or message'}), 400
    
    try:
        message_id = whatsapp_service.send_message(to_number, message)
        return jsonify({'status': 'success', 'message_id': message_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
