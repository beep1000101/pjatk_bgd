from functools import wraps
from sqlalchemy.exc import IntegrityError
from flask_app.routes.errors import APIError
from flask_app.app import db


def transactional(on_conflict_message=None):
    """
    1. Runs the view function.
    2. Commits if all went well.
    3. On IntegrityError, rollbacks and raises APIError(409).
    Uses the db instance imported from flask_app.app.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                response = fn(*args, **kwargs)
                db.session.commit()
                return response
            except IntegrityError:
                db.session.rollback()
                msg = on_conflict_message or "Database constraint violated."
                raise APIError(msg, 409)
        return wrapper
    return decorator
