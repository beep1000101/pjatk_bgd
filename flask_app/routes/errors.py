from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed, InternalServerError


class APIError(HTTPException):
    """
    Custom exception for application-specific API errors.

    Parameters
    ----------
    message : str
        The error message to be returned in the response.
    status_code : int
        The HTTP status code to be returned.

    Attributes
    ----------
    message : str
        The error message to be returned in the response.
    code : int
        The HTTP status code to be returned.

    Examples
    --------
    >>> raise APIError("Invalid input", 400)
    """

    def __init__(self, message, status_code):
        super().__init__(description=message)
        self.message = message
        self.code = status_code


def register_error_handlers(app):
    """
    Registers global error handlers on the Flask application.

    Parameters
    ----------
    app : Flask
        The Flask application instance.

    Error Handlers
    --------------
    APIError
        Handles custom API errors with a specific message and status code.
    ValidationError
        Handles Marshmallow validation errors, returning details of the failure.
    OperationalError
        Handles database connection errors, including the request path.
    NotFound
        Handles 404 errors, returning the requested path.
    MethodNotAllowed
        Handles 405 errors, returning the method and endpoint.
    Exception
        Handles unexpected internal server errors, including the request path.

    Notes
    -----
    Each error handler returns a JSON response with an appropriate error message
    and HTTP status code.
    """
    @app.errorhandler(APIError)
    def handle_api_error(err):
        return jsonify({"error": err.message}), err.code

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return jsonify({
            "error": "Validation failed",
            "details": err.messages
        }), 400

    @app.errorhandler(OperationalError)
    def handle_db_error(err):
        return jsonify({
            "error": (
                "Database connection failed. "
                "Please ensure the database exists and is accessible."
            ),
            "path": request.path
        }), 500

    @app.errorhandler(NotFound)
    def handle_404(err):
        return jsonify({
            "error": f"Resource not found at '{request.path}'"
        }), 404

    @app.errorhandler(MethodNotAllowed)
    def handle_405(err):
        return jsonify({
            "error": (
                f"Method '{request.method}' not allowed "
                f"on endpoint '{request.path}'"
            )
        }), 405

    @app.errorhandler(InternalServerError)
    def handle_500(err):
        return jsonify({
            "error": "Internal server error.",
            "path": request.path
        }), 500
