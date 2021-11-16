import os

from flask import Flask
from .encounter import Encounter
from .encounter_without_mana import Encounter_without_mana
from .buffs_list import Buffs_list
from .character import Character

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # from . import db
    # db.init_app(app)
    
    #from . import auth
    #app.register_blueprint(auth.bp)

    #from . import blog
    #app.register_blueprint(blog.bp)
    #app.add_url_rule('/', endpoint='index')
    
    from . import simulator
    app.register_blueprint(simulator.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app