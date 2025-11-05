from models import db

class Bot(db.Model):
    __tablename__ = 'bots'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    fallback_message = db.Column(db.Text, nullable=False, default='Sorry, I did not understand that.')
    active = db.Column(db.Boolean, default=True)
    
    rules = db.relationship('Rule', backref='bot', lazy=True, cascade='all, delete-orphan')
    message_logs = db.relationship('MessageLog', backref='bot', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Bot {self.name}>'
