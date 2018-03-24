# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import os
from functools import wraps
import requests
from requests.exceptions import RequestException
from werkzeug.exceptions import InternalServerError, Unauthorized
from flask import request, jsonify, current_app
from project.views import views_bp


@views_bp.route('/create', methods=['POST'])
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_server = kwargs.pop("oauth_server", False) or \
                               current_app.config.get("OAUTH_SERVER", False) or \
                               os.environ.get("OAUTH_SERVER", False)
        if not authorization_server:
            return InternalServerError("No oauth server configure")
        is_authenticated = False
        try:
            print("HEADERS")
            print(request.headers)
            authorization = request.headers.get('authorization')
            headers = {
                'content-type': "application/json",
                'authorization': authorization,
            }
            response = requests.request("GET", authorization_server, headers=headers)
            current_app.logger.info(u'Login response {}'.format(response))
            if response.status_code == 200:
                is_authenticated = True
        except RequestException as e:
            current_app.logger.error(u'Error login {}'.format(e))
            return InternalServerError("Oauth server error {}".format(e))

        if not is_authenticated:
            current_app.logger.error(u'Error NOT LOGGED IN: {}'.format(authorization))
            return Unauthorized("Invalid Token")
        return f(*args, **kwargs)

    return decorated_function


@views_bp.route('/<palette>/')
@login_required
def colors(palette):
    """Example endpoint return a list of colors by palette
    This is using docstring for specifications
    ---
    security:
      - APIKeyQueryParam: []
      - APIKeyHeader: []
    tags:
      - colors
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
        description: Which palette to filter?
    operationId: get_colors
    consumes:
      - application/json
    produces:
      - application/json
    schemes: ['http', 'https']
    deprecated: false
    externalDocs:
      description: Project repository
      url: http://github.com/rochacbruno/flasgger
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)