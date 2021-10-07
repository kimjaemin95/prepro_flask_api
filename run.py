# Api version
# from api.v1 import api_v1
from api.v2 import api_v2

# f
from flask import Flask, request


# Run apps
app = Flask(__name__)
# app.register_blueprint(api_v1, url_prefix='/api/v1/data')
app.register_blueprint(api_v2, url_prefix='/api/v2/data')


@app.route('/')
def index():
    return 'Main index page!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)