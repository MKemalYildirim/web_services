#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
import models


app = Flask(__name__)

auth = HTTPBasicAuth()

@auth.get_password
def get_password(name):
        user =models.User.query.filter_by(username=name).first()
        if name == user.username:
            return user.password
        return None
    
@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401) 

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route("/add", methods=['POST'])
def post():

    content = request.get_json()
    name=content['name']
    pas=content['pass']
    try:
     new_user=models.User(username=name,password=pas)
     models.db.session.add(new_user)
     models.db.session.commit()
     return "Ekleme Başarılı"
    except:
     return "Ekleme Başarısız"


@app.route("/delete/<string:name>")
@auth.login_required
def DELETE(name):
    try:
     user = models.User.query.filter_by(username=name).first()
     models.db.session.delete(user)
     models.db.session.commit()
     return "Silme başarılı"
    except:
      return "Kişi Bulunamadı"




if __name__ == '__main__':
    app.run(debug = True)
