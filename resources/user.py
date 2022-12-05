import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

@user.route('/', methods=["GET"])
@login_required
def get_my_user():
    user = model_to_dict(current_user)
    return jsonify(
        data=user,
        status= 200,
        message="Success"
    ), 200

@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)

        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password'] # delete the password since the client doesn't need it
            login_user(user)
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"}) # respond to the client
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})


@user.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify(
        data={},
        status=200,
        message= 'successful logout'
    ), 200


@user.route('/admin/users', methods=["GET"])
@login_required
def get_all_users():
    print(current_user)
    if current_user.admin == True:
        try:
            users = [model_to_dict(user) for user in models.User.select()]
            return jsonify(data=users, status={"code": 200, "message": "Success"})
        except models.DoesNotExist:
            return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})
    else:
        return jsonify(data={}, status={"code": 403, "message": "You're not an administrator"})

@user.route('/admin/users/<id>', methods=["GET"])
@login_required
def get_one_user(id):
    if current_user.admin == True:
        print(id, 'reserved word?')
        user = models.User.get_by_id(id)
        print(user.__dict__)
    return jsonify(
        data=model_to_dict(user),
        status= 200,
        message="Success"
    ), 200

@user.route('/admin/users/<id>', methods=["DELETE"])
@login_required
def delete_user(id):
    if (current_user.admin == True) or (current_user.username == models.Dog.created_by):
        query = models.User.delete().where(models.User.id==id)
        query.execute()
        return jsonify(
            data='resource successfully deleted',
            message= 'resource successfully deleted',
            status=200
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "You're not an administrator"})