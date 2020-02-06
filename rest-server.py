#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
from flask import g
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import model


app = Flask(__name__)

db = SQLAlchemy(app)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Mehmet_Kemal/Desktop/web_services/veriler.db'


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@auth.verify_password
def verify_password(name, pas):

    user = model.User.verify_auth_token(name)
    if not user:

        user = model.User.query.filter_by(username = name).first()
        if not user or not user.verify_password(pas):
            return False
    g.user = user
    return True

@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if model.User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = model.User(username = username)
    user.hash_password(password)
    model.db.session.add(user)
    model.db.session.commit()
    return jsonify({ 'username': user.username })



@app.route("/delete/<string:name>")
@auth.login_required
def DELETE(name):
    user = model.User.query.filter_by(username=name).first()
    if user is None:
        return "Böyle Bir Kişi Yok"
    else:
      try:  
        model.db.session.delete(user)
        model.db.session.commit()
        return "Silme başarılı"
    
      except:
        
        return "Kişi silinemedi"
    
      



@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)



if __name__ == '__main__':
    app.run(debug = True)
