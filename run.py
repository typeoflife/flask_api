from flask import jsonify, request
from jsonschema import validate, ValidationError
from app import app, db
from models import User, Adv
from schema import USER_CREATE, ADV_CREATE


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
    if User.query.filter_by(username=user_data['username']).first() or User.query.filter_by(
            email=user_data['email']).first():
        response = jsonify({'status': 'Username or email is exists'})
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
