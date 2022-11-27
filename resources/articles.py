import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

articles = Blueprint('articles', 'articles')


@articles.route('/', methods=["GET"])
def get_all_articles():
    try:
        articles = [model_to_dict(article) for article in models.Article.select()]
        print(articles)
        return jsonify(data=articles, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@articles.route('/<id>', methods=["GET"])
def get_one_article(id):
    article = models.Article.get_by_id(id)
    print(article.__dict__)
    return jsonify(
        data=model_to_dict(article),
        status= 200,
        message="Success"
    ), 200


@articles.route('/', methods=['POST'])
@login_required
def create_article():
    if current_user.admin == True:
        payload = request.get_json()
        new_article = models.Article.create(title=payload['title'], summary=payload['summary'], body=payload['body'], image=payload['image'], author=current_user.username)
        article_dict = model_to_dict(new_article)
        return jsonify(
            data=article_dict,
            message='Successfully created article!',
            status=201
        ), 201
    else:
        return jsonify(data={}, status={"code": 403, "message": "You're not an administrator"})

@articles.route('/<id>', methods=["PUT"])
@login_required
def update_article(id):
    if current_user.admin == True:
        payload = request.get_json()
        query = models.Article.update(**payload).where(models.Article.id==id)
        query.execute()
        return jsonify(
            data=model_to_dict(models.Article.get_by_id(id)),
            status=200,
            message= 'resource updated successfully'
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "You're not an administrator"})

@articles.route('/<id>', methods=["DELETE"])
@login_required
def delete_article(id):
    if current_user.admin == True:
        query = models.Article.delete().where(models.Article.id==id)
        query.execute()
        return jsonify(
            data='resource successfully deleted',
            message= 'resource successfully deleted',
            status=200
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "You're not an administrator"})