from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    message = '<p>hello world</p>'
    return message


if __name__ == '__main__':
    app.run(debug=True)
