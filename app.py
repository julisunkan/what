import os
from flask import Flask, render_template
from models import db
from models.user import User
from models.bot import Bot
from models.rule import Rule
from models.message_log import MessageLog

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whatsapp_bot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    from routes.auth import auth_bp
    from routes.bots import bots_bp
    from routes.api import api_bp
    from routes.analytics import analytics_bp
    from routes.whatsapp import whatsapp_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(bots_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(whatsapp_bp)
    
    @app.route('/static/manifest.webmanifest')
    def manifest():
        return app.send_static_file('manifest.webmanifest')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
