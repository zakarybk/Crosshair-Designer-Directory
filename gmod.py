from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Home!'


@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello! This is some awesome data'


if __name__ == '__main__':
    app.run(debug=True)
