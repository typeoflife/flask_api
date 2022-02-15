import hashlib
import salt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from jsonschema import validate, ValidationError
from schema import USER_CREATE, ADV_CREATE

app = Flask('app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __str__(self):
        return '<User {}>'.format(self.username)

    def __repr__(self):
        return str(self)

    def set_password(self, raw_password: str):
        raw_password = f'{raw_password}{salt.SALT}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        raw_password = f'{raw_password}{salt.SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()


class Adv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)

    def __str__(self):
        return '<Adv {}>'.format(self.title)


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        response = jsonify({'status': 'User not found'})
        response.status_code = 404
        return response
    return jsonify({
        'id': user.id,
        'username': user.username
    })


@app.route('/user/', methods=['POST'])
def create_user():
    user_data = request.json
    try:
        validate(request.json, USER_CREATE)
    except ValidationError as er:
        response = jsonify({'success': False, 'error': er.message})
        response.status_code = 400
        return response
    new_user = User(**user_data)
    new_user.set_password(request.json['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'id': new_user.id
    })


@app.route('/adv/<int:adv_id>', methods=['GET'])
def get_adv(adv_id):
    adv = Adv.query.get(adv_id)
    if not adv:
        response = jsonify({'status': 'Advertisement  not found'})
        response.status_code = 404
        return response
    return jsonify({
        'id': adv.id
    })


@app.route('/adv/', methods=['POST'])
def create_adv():
    adv_data = request.json
    try:
        validate(request.json, ADV_CREATE)
    except ValidationError as er:
        response = jsonify({'success': False, 'error': er.message})
        response.status_code = 400
        return response
    if not User.query.get(adv_data['user_id']):
        response = jsonify({'status': 'User  not found'})
        response.status_code = 400
        return response
    new_adv = Adv(**adv_data)
    db.session.add(new_adv)
    db.session.commit()
    return jsonify({
        'id': new_adv.id
    })


@app.route('/adv/<int:adv_id>', methods=['DELETE'])
def delete_adv(adv_id):
    adv = Adv.query.get(adv_id)
    if not adv:
        response = jsonify({'status': 'Advertisement not found'})
        response.status_code = 404
        return response
    db.session.delete(adv)
    db.session.commit()
    return jsonify({
        'id': adv.id
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
