from flask import Flask
from .blueprints.players import playersBP


def create_app():
    app = Flask(__name__)
    
    # Load configuration
    #app.config.from_object('config.Config')
    
    # Initialize extensions
    #db.init_app(app)
   # migrate.init_app(app, db)
    
    # Register blueprints
    app.register_blueprint(playersBP, url_prefix='/players')
    
    
    return app

