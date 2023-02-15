from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from Controller.TodolistController import app_info

app = Flask(__name__)
CORS(app, supports_credentials=True)
# register the blueprint into flask app
app.register_blueprint(app_info, url_prefix="/data")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yzq:zuqiangyyy@localhost:5432/flask_db'

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
