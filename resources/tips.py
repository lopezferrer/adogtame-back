import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

tips = Blueprint('tips', 'tips')


@tips.route('/', methods=["GET"])
def get_all_tips():
    try:
        tips = [model_to_dict(tip) for tip in models.Tip.select()]
        print(tips)
        return jsonify(data=tips, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


@tips.route('/', methods=['POST'])
@login_required
def create_tip():
    #print(current_user.username)
    payload = request.get_json()
    new_tip = models.Tip.create(tip=payload['tip'], author=current_user.username)
    tip_dict = model_to_dict(new_tip)

    return jsonify(
        data=tip_dict,
        message='Successfully created tip!',
        status=201
    ), 201


@tips.route('/<id>', methods=["GET"])
def get_one_tip(id):
    print(id, 'reserved word?')
    tip = models.Tip.get_by_id(id)
    print(tip.__dict__)
    return jsonify(
        data=model_to_dict(tip),
        status= 200,
        message="Success"
    ), 200


@tips.route('/<id>', methods=["PUT"])
@login_required
def update_tip(id):
    payload = request.get_json()
    query = models.Tip.update(**payload).where(models.Tip.id==id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.Tip.get_by_id(id)),
        status=200,
        message= 'resource updated successfully'
    ), 200


@tips.route('/<id>', methods=["DELETE"])
@login_required
def delete_tip(id):
    query = models.Tip.delete().where(models.Tip.id==id)
    query.execute()
    return jsonify(
        data='resource successfully deleted',
        message= 'resource successfully deleted',
        status=200
    ), 200