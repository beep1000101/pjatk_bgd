from flask import Blueprint, request
from web.enums import HTTP

app_routes = Blueprint('app_routes', __name__)


@app_routes.route('/not_dead', methods=[HTTP.POST, HTTP.GET])
def not_dead():
    """Testing request, to be terminated later."""
    if request.method == HTTP.POST:
        result = f'Not dead, {request.method}'
        return result
    elif request.method == HTTP.GET:
        result = f'Not dead, {request.method}'
        return result
    else:
        return 'Cosmic Ray Deteced!'
