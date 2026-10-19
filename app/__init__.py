from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config, BASE_DIR

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    (BASE_DIR / 'instance').mkdir(exist_ok=True)
    db.init_app(app)
    migrate.init_app(app, db)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
