from flask import Flask
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'app.db'),
    )

    if test_config is False:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test congig if passed in
        app.config.from_mapping(test_config)

    # make the app avalilable in the app_context
    app.app_context().push()

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database.db import init_app
    init_app(app)

    from .views.admin_views import init_app
    init_app(app)

    from .views.public_views import bp
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='index')

    from .views.exercise_views import bp
    app.register_blueprint(bp)

    from .views.betsy_views import bp
    app.register_blueprint(bp)
    
    return app
