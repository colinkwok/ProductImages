import os

from flask import Flask
from . import db
from . import product
from . import search

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'product.sqlite'),
    )

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

    db.init_app(app)

    app.register_blueprint(product.bp)
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/add_product', endpoint='add_product')

    app.register_blueprint(search.bp)
    app.add_url_rule('/keyword', endpoint='keyword')

    return app