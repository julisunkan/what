from datetime import datetime
from models import db

class MessageLog(db.Model):
    __tablename__ = 'message_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)
    sender = db.Column(db.String(100), nullable=False)
    direction = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MessageLog {self.direction} - {self.sender}>'
