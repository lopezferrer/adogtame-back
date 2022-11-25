import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

dogs = Blueprint('dogs', 'dogs')

@dogs.route('/', methods=["GET"])
def get_all_dogs():
    try:
        dogs = [model_to_dict(dog) for dog in models.Dog.select()]
        print(dogs)
        return jsonify(data=dogs, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@dogs.route('/mydogs', methods=["GET"])
@login_required
def dogs_index():
    dog_dicts = [model_to_dict(dog) for dog in current_user.my_dogs]
    return jsonify({
        'data': dog_dicts,
        'message': f"Successfully found {len(dog_dicts)} dogs",
        'status': 200
    }), 200

@dogs.route('/', methods=['POST'])
@login_required
def create_dog():
    print(current_user.username)
    payload = request.get_json()
    new_dog = models.Dog.create(name=payload['name'], age=payload['age'], breed=payload['breed'], personality=payload['personality'], city=payload['city'], vaccines=payload['vaccines'])
    dog_dict = model_to_dict(new_dog)

    return jsonify(
        data=dog_dict,
        message='Successfully created dog!',
        status=201
    ), 201


@dogs.route('/<id>', methods=["GET"])
def get_one_dog(id):
    print(id, 'reserved word?')
    dog = models.Dog.get_by_id(id)
    print(dog.__dict__)
    return jsonify(
        data=model_to_dict(dog),
        status= 200,
        message="Success"
    ), 200

@dogs.route('/<id>', methods=["PUT"])
@login_required
def update_dog(id):
    payload = request.get_json()
    query = models.Dog.update(**payload).where(models.Dog.id==id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.Dog.get_by_id(id)),
        status=200,
        message= 'resource updated successfully'
    ), 200

@dogs.route('/<id>', methods=["DELETE"])
@login_required
def delete_dog(id):
    query = models.Dog.delete().where(models.Dog.id==id)
    query.execute()
    return jsonify(
        data='resource successfully deleted',
        message= 'resource successfully deleted',
        status=200
    ), 200