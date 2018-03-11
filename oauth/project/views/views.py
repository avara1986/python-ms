# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from flask import request, jsonify
from flask import current_app
from flask_jwt import jwt_required, current_identity
from project.views import views_bp
from project.models import db
from project.models.models import User

@views_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return '%s' % current_identity


@views_bp.route('/healthcheck', methods=['GET'])
def healtcheck():
    current_app.logger.info('Test logging in healtcheck', )
    return 'OK'



@views_bp.route('/create', methods=['POST'])
def create():
    post_data = request.get_json()
    user = User(
        username=post_data.get('username'),
        password=post_data.get('password')
    )
    # insert the user
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id})
