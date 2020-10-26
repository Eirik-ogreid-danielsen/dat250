import os 

from flask import Flask, g
import psycopg2
import psycopg2.extras
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'scuffed',
        DATABASE = os.environ['DATABASE_URL'],
    )
    

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    with app.app_context():
        db.init_db()
    

    from . import auth
    app.register_blueprint(auth.bp)

    from . import forum
    app.register_blueprint(forum.bp)
    app.add_url_rule('/', endpoint='index')

    return app

