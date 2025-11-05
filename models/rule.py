from models import db

class Rule(db.Model):
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)
    keyword = db.Column(db.String(200), nullable=False)
    response = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<Rule {self.keyword}>'
