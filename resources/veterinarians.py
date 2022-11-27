import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

veterinarians = Blueprint('veterinarians', 'veterinarians')

@veterinarians.route('/', methods=["GET"])
def get_all_veterinarians():
    try:
        veterinarians = [model_to_dict(veterinarian) for veterinarian in models.Veterinarian.select()]
        print(veterinarians)
        return jsonify(data=veterinarians, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


@veterinarians.route('/', methods=['POST'])
@login_required
def create_veterinarian():
    print(current_user.username)
    payload = request.get_json()
    new_veterinarian = models.Veterinarian.create(name=payload['name'], address=payload['address'], city=payload['city'], phone=payload['phone'], email=payload['email'], created_by=current_user.username)
    veterinarian_dict = model_to_dict(new_veterinarian)

    return jsonify(
        data=veterinarian_dict,
        message='Successfully created veterinarian!',
        status=201
    ), 201


@veterinarians.route('/<id>', methods=["GET"])
def get_one_veterinarian(id):
    print(id, 'reserved word?')
    veterinarian = models.Veterinarian.get_by_id(id)
    print(veterinarian.__dict__)
    return jsonify(
        data=model_to_dict(veterinarian),
        status= 200,
        message="Success"
    ), 200


@veterinarians.route('/<id>', methods=["PUT"])
@login_required
def update_veterinarian(id):
    payload = request.get_json()
    query = models.Veterinarian.update(**payload).where(models.Veterinarian.id==id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.Veterinarian.get_by_id(id)),
        status=200,
        message= 'resource updated successfully'
    ), 200


@veterinarians.route('/<id>', methods=["DELETE"])
@login_required
def delete_veterinarian(id):
    query = models.Veterinarian.delete().where(models.Veterinarian.id==id)
    query.execute()
    return jsonify(
        data='resource successfully deleted',
        message= 'resource successfully deleted',
        status=200
    ), 200