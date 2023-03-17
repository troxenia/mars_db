import flask
from flask import request, jsonify

from . import db_session
from .users import User

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {'users': [user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                                      'city_from', 'hashed_password')) for user in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify({'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address',
                                               'email', 'city_from', 'hashed_password'))})


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if 'id' in request.json:
        if request.json['id'] in tuple(user.id for user in db_sess.query(User).all()):
            return jsonify({'error': 'Id already exists'})
    if db_sess.query(User).filter(User.email == request.json['email']).first():
        return jsonify({'error': 'User already exists'})
    user = User(**{k: v for k, v in request.json.items() if k != 'password'})
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address',
                         'email', 'city_from', 'password']
                 for key in request.json):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user_to_edit = db_sess.query(User).get(user_id)
    if not user_to_edit:
        return jsonify({'error': 'Not found'})
    if 'id' in request.json:
        if request.json['id'] in tuple(user.id for user in db_sess.query(User).all() if user_to_edit.id != user.id):
            return jsonify({'error': 'Id already exists'})
    if 'email' in request.json:
        if db_sess.query(User).filter(User.email == request.json['email'], User.id != user_to_edit.id).first():
            return jsonify({'error': 'User already exists'})
    if 'password' in request.json:
        user_to_edit.set_password(request.json['password'])
    db_sess.query(User).filter(User.id == user_id).update({k: v for k, v in request.json.items() if k != 'password'})
    db_sess.commit()
    return jsonify({'success': 'OK'})
