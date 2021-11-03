from typing import Union
from flask import Blueprint, jsonify, _app_ctx_stack, send_from_directory, request
import json
import os
import ast
import datetime
import pymongo
from pymongo.database import Database
from werkzeug.wrappers.response import Response
import db.mongodb_controller as db_controller
from marshmallow import ValidationError
from api.validation import is_gym_valid, is_section_valid


api_blueprint = Blueprint(
    'api_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/api'
)


def get_db() -> Database:
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'database'):
        client = pymongo.MongoClient(
            get_creds(),
            connectTimeoutMS=30000,
            socketTimeoutMS=None,
            # socketKeepAlive=True,
            connect=False,
            maxPoolsize=1)
        top.database = client["RocoLib"]
    return top.database


def get_creds() -> Union[str, None]:
    """
    Get the credentials for MongoDB either from a local file
    or from an evironment variable
    """
    creds = None
    if os.path.isfile('creds.txt'):
        with open('creds.txt', 'r') as f:
            creds = f.readline()
    else:
        try:
            creds = os.environ['MONGO_DB']
        except Exception:
            pass
    return creds


@api_blueprint.route('/docs/swagger.json')
def api_docs() -> Response:
    """
    Raw swagger document endpoint
    """
    return send_from_directory('static', 'swagger/swagger.json')


@api_blueprint.route('/gym/list', methods=['GET'])
def get_gyms() -> Response:
    """Gym list.
    ---
    get:
      tags:
        - Gyms
      responses:
        200:
          description:
            List of gyms
          content:
            application/json:
              schema: GymListSchema
            text/plain:
              schema: GymListSchema
            text/json:
              schema: GymListSchema
        400:
          description:
            Bad request
        404:
          description:
            Not found
        500:
          description:
            Server Error
    """
    return jsonify(dict(gyms=db_controller.get_gyms(get_db()))), 200


@api_blueprint.route('/gym/<string:gym_id>/walls', methods=['GET'])
def get_gym_walls(gym_id: str) -> Response:
    """Walls associated to the given gym.
    ---
    get:
      tags:
        - Gyms
      parameters:
      - in: path
        schema: GymIDParameter
      responses:
        200:
          description:
            List of walls associated to the specified gym
          content:
            application/json:
              schema: WallListSchema
            text/plain:
              schema: WallListSchema
            text/json:
              schema: WallListSchema
        400:
          description:
            Bad request
        404:
          description:
            Not found
        500:
          description:
            Server Error
    """
    return jsonify(dict(walls=db_controller.get_gym_walls(gym_id, get_db()))), 200


@api_blueprint.route('/gym/<string:gym_id>/name', methods=['GET'])
def get_gym_pretty_name(gym_id: str) -> Response:
    """Given a gym id get its display name
    ---
    get:
      tags:
        - Gyms
      parameters:
      - in: path
        schema: GymIDParameter
      responses:
        200:
          description:
            Gym name
          content:
            application/json:
              schema: GymNameSchema
            text/plain:
              schema: GymNameSchema
            text/json:
              schema: GymNameSchema
        400:
          description:
            Bad request
        404:
          description:
            Not found
        500:
          description:
            Server Error
    """
    return jsonify(dict(name=db_controller.get_gym_pretty_name(gym_id, get_db()))), 200


@api_blueprint.route('/gym/<string:gym_id>/<string:wall_section>/name', methods=['GET'])
def get_gym_wall_name(gym_id: str, wall_section: str) -> Response:
    """Get a wall name given the gym and the section
    ---
    get:
      tags:
        - Gyms
      parameters:
      - in: path
        schema: GymIDParameter
      - in: path
        schema: WallSectionParameter
      responses:
        200:
          description:
            Wall name
          content:
            application/json:
              schema: WallNameSchema
            text/plain:
              schema: WallNameSchema
            text/json:
              schema: WallNameSchema
        400:
          description:
            Bad request
        404:
          description:
            Not found
        500:
          description:
            Server Error
    """
    return jsonify(dict(name=db_controller.get_wall_name(gym_id, wall_section, get_db()))), 200


@api_blueprint.route('/boulders/<string:gym_id>/list', methods=['GET'])
def get_gym_boulders(gym_id: str) -> Response:
    """Boulders associated to the given gym.
    ---
    get:
      tags:
        - Boulders
      parameters:
      - in: path
        schema: GymIDParameter
      responses:
        200:
          description:
            List of gym boulders
          content:
            application/json:
              schema: GymBoulderListSchema
            text/plain:
              schema: GymBoulderListSchema
            text/json:
              schema: GymBoulderListSchema
        400:
          description:
            Bad request
        404:
          description:
            Not found
        500:
          description:
            Server Error
    """
    return jsonify(dict(boulders=db_controller.get_boulders(gym_id, get_db()).get('Items', []))), 200


@api_blueprint.route('/boulders/<string:gym_id>/<string:wall_section>/create', methods=['POST'])
def boulder_create(gym_id: str, wall_section: str) -> Response:
    """Create a new boulder
    ---
    post:
      tags:
        - Boulders
      parameters:
      - in: path
        schema: GymIDParameter
      - in: path
        schema: WallSectionParameter
      requestBody:
        description: Create boulder request body
        required: true
        content:
          application/json:
            schema: CreateBoulderRequestBody
          application/x-www-form-urlencoded:
            schema: CreateBoulderRequestBody
          text/json:
            schema: CreateBoulderRequestBody
          text/plain:
            schema: CreateBoulderRequestBody
      responses:
        201:
          description:
            Creation successful
          content:
            text/plain:
              schema: CreateBoulderResponseBody
            text/json:
              schema: CreateBoulderResponseBody
            application/json:
              schema: CreateBoulderResponseBody
        400:
          description:
            Bad request
          content:
            text/plain:
              schema: CreateBoulderErrorResponse
            text/json:
              schema: CreateBoulderErrorResponse
            application/json:
              schema: CreateBoulderErrorResponse
        404:
          description:
            Not found
        500:
          description:
            Server Error
    """
    if request.method == 'POST':
        # Validate gym and wall section
        valid_gym = is_gym_valid(gym_id, get_db()) 
        valid_section = is_section_valid(gym_id, wall_section, get_db())
        if not valid_gym or not valid_section:
            errors = []
            errors.append({'gym_id': f'Gym {gym_id} does not exist'}) if not valid_gym else None
            errors.append({'wall_section': f'Wall section {wall_section} does not exist'}) if not valid_section else None
            return jsonify(dict(created=False, errors=errors)), 400  
        # Get boulder data from request
        request.get_data() # required?
        data = {
          'rating': 0, 
          'raters': 0, 
          'section': wall_section,
          'time': datetime.datetime.now().isoformat()}
        request_data = {}
        from_form = False
        # Handle the different content types
        if request.data is not None:
          request_data = json.loads(request.data)
        elif request.form is not None or request.json is not None:
          request_data, from_form = request.json, False if request.json is not None else request.form, True

        for key, val in request_data.items():
          data[key.lower()] = val
          if from_form and key.lower() == 'holds':
            data[key.lower()] = ast.literal_eval(val)
            
        # Validate Boulder Schema
        try:
          from api.schemas import CreateBoulderRequestValidator
          _ = CreateBoulderRequestValidator().load(data) # Will raise ValidationError if not valid
          resp = db_controller.put_boulder(data, gym=gym_id, database=get_db())
          if resp is None:
              return jsonify(dict(created=False)), 500 # something went wrong
          return jsonify(dict(created=True, _id=resp)), 201
        except ValidationError as err:
          return jsonify(dict(created=False, errors=err.messages)), 400
