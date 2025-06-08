from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_app.routes.errors import register_error_handlers


db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    """
    Create and configure the Flask application.

    This function initializes the Flask app, sets up the database and
    Marshmallow, and registers the API routes.

    Parameters
    ----------
    config_name : str
        The configuration object to use for the Flask app.

    Returns
    -------
    Flask
        The configured Flask application instance.
    """
    # import routes
    from flask_app.routes.orders import orders_bp
    from flask_app.routes.users import users_bp
    # import error handlers
    # from flask_app.routes.errors import register_error_handlers
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)
    ma.init_app(app)

    # register the routes
    app.register_blueprint(orders_bp)
    app.register_blueprint(users_bp)
    # register the error handlers
    register_error_handlers(app=app)

    @app.route('/')
    def hello_world():
        """
        A simple route to verify the server is running.

        Returns
        -------
        tuple
            A greeting message and HTTP status code 200.
        """
        return 'hello to the pokemon world!', 200

    return app
