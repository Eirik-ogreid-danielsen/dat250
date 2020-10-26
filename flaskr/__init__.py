import os 

from flask import Flask, g
import psycopg2
import psycopg2.extras
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.app_context()
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

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_db()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import forum
    app.register_blueprint(forum.bp)
    app.add_url_rule('/', endpoint='index')

    return app

