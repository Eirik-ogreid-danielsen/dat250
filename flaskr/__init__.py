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
    DATABASE = 'database.db'
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
    
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = psycopg2.connect(DATABASE)
        return db

    def init_db():
        with app.app_context():
            db = get_db()
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().execute(f.read())
            db.commit()


    from . import auth
    app.register_blueprint(auth.bp)

    from . import forum
    app.register_blueprint(forum.bp)
    app.add_url_rule('/', endpoint='index')

    return app

