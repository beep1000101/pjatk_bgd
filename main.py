from flask_app.app import create_app
from flask_app.config import get_flask_config

flask_config = get_flask_config()
app = create_app(flask_config)

if __name__ == '__main__':
    app.run()
