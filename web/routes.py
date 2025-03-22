from flask import Blueprint, request

app_routes = Blueprint('app_routes', __name__)


@app_routes.route('/not_dead', methods=['POST', 'GET'])
def not_dead():
    """Testing request, to be terminated later."""
    if request.method == 'POST':
        result = f'Not dead, {request.method}'
        return result
    elif request.method == 'GET':
        result = f'Not dead, {request.method}'
        return result
    else:
        return 'Cosmic Ray Deteced!'
