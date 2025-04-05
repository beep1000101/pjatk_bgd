from flask import Flask

from web.routes import app_routes

app = Flask(__name__)
app.register_blueprint(app_routes)


@app.route('/')
def hello_world():
    message = '<p>hello world</p>'
    return message


if __name__ == '__main__':
    app.run(debug=True)
