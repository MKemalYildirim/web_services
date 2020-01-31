#!flask/bin/python

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Mehmet_Kemal/Desktop/web_services/veriler.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


app = Flask(__name__)
db.create_all()

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'kemal':
        return '123'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)    

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)



@app.route("/add", methods=['POST'])
def post():
    print(request.is_json)
    content = request.get_json()
    name=content['name']
    pas=content['pass']

    new_user=User(username=name,password=pas)
    db.session.add(new_user)
    db.session.commit()
    return 'JSON posted'

@app.route("/delete/<string:name>")
def DELETE(name):
    user=User.query.filter_by(username=name).first()
    db.session.delete(user)
    db.session.commit()
    return "Silme başarılı"
    

    new_user=User(username=name,password=pas)
    db.session.add(new_user)
    db.session.commit()
    return 'Ekleme Başarılı'


if __name__ == '__main__':
    app.run(debug = True)
