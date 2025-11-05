from datetime import datetime
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from utils.encryption import encrypt_value, decrypt_value

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    whatsapp_provider = db.Column(db.String(20), default='meta')
    
    meta_access_token_encrypted = db.Column(db.Text, nullable=True)
    meta_phone_number_id_encrypted = db.Column(db.Text, nullable=True)
    meta_api_version = db.Column(db.String(10), default='v21.0')
    
    twilio_account_sid_encrypted = db.Column(db.Text, nullable=True)
    twilio_auth_token_encrypted = db.Column(db.Text, nullable=True)
    twilio_whatsapp_number = db.Column(db.String(30), nullable=True)

    bots = db.relationship('Bot', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_meta_credentials(self, access_token, phone_number_id, api_version='v21.0'):
        self.meta_access_token_encrypted = encrypt_value(access_token) if access_token else None
        self.meta_phone_number_id_encrypted = encrypt_value(phone_number_id) if phone_number_id else None
        self.meta_api_version = api_version if api_version else 'v21.0'
    
    def get_meta_credentials(self):
        return {
            'access_token': decrypt_value(self.meta_access_token_encrypted),
            'phone_number_id': decrypt_value(self.meta_phone_number_id_encrypted),
            'api_version': self.meta_api_version or 'v21.0'
        }
    
    def set_twilio_credentials(self, account_sid, auth_token, whatsapp_number):
        self.twilio_account_sid_encrypted = encrypt_value(account_sid) if account_sid else None
        self.twilio_auth_token_encrypted = encrypt_value(auth_token) if auth_token else None
        self.twilio_whatsapp_number = whatsapp_number
    
    def get_twilio_credentials(self):
        return {
            'account_sid': decrypt_value(self.twilio_account_sid_encrypted),
            'auth_token': decrypt_value(self.twilio_auth_token_encrypted),
            'whatsapp_number': self.twilio_whatsapp_number
        }
    
    def has_meta_credentials(self):
        creds = self.get_meta_credentials()
        return bool(creds['access_token'] and creds['phone_number_id'])
    
    def has_twilio_credentials(self):
        creds = self.get_twilio_credentials()
        return bool(creds['account_sid'] and creds['auth_token'])

    def __repr__(self):
        return f'<User {self.username}>'