import json
from api.blueprint import get_auth_token, get_boulder_by_id, get_boulder_by_name
from api.blueprint import get_gym_boulders, get_gym_pretty_name, get_gym_wall_name
from api.blueprint import get_gyms, get_gym_walls, boulder_create, get_resource, new_user
from api.blueprint import get_user_ticklist, rate_boulder


def generate_api_docs(app) -> None:
    """
    Generate the OpenAPI spec doc
    """
    # Generate API documentation
    from api.schemas import spec
    from api.schemas import GymListSchema
    from api.schemas import WallListSchema
    from api.schemas import GymNameSchema
    from api.schemas import WallNameSchema
    from api.schemas import GymBoulderListSchema
    from api.schemas import BoulderSchema
    from api.schemas import BoulderIDParameter
    from api.schemas import BoulderNameParameter
    from api.schemas import GymIDParameter
    from api.schemas import CreateBoulderRequestBody
    from api.schemas import CreateBoulderResponseBody
    from api.schemas import CreateBoulderErrorResponse
    from api.schemas import AuthenticationErrorResponse
    from api.schemas import AuthenticationRequestBody
    from api.schemas import AuthenticationResponseBody
    from api.schemas import SignUpErrorResponse
    from api.schemas import SignUpRequestBody
    from api.schemas import SignUpResponseBody
    from api.schemas import TestTokenErrorResponse
    from api.schemas import TestTokenResponseBody
    from api.schemas import TicklistBoulder
    from api.schemas import TicklistResponseBody
    from api.schemas import TicklistErrorResponse
    from api.schemas import RateBoulderRequestBody
    from api.schemas import RateBoulderResponseBody
    from api.schemas import RateBoulderErrorResponse

    spec.components.schema("Gyms", schema=GymListSchema)
    spec.components.schema("Walls", schema=WallListSchema)
    spec.components.schema("Boulder", schema=BoulderSchema)
    spec.components.schema("Boulders", schema=GymBoulderListSchema)
    spec.components.schema("GymName", schema=GymNameSchema)
    spec.components.schema("WallName", schema=WallNameSchema)
    spec.components.schema(
        "CreateBoulder", schema=CreateBoulderRequestBody)
    spec.components.schema("CreateBoulderResponse",
                           schema=CreateBoulderResponseBody)
    spec.components.schema("CreateBoulderErrorResponse",
                           schema=CreateBoulderErrorResponse)
    spec.components.schema("GymIDParameter", schema=GymIDParameter)
    spec.components.schema("BoulderIDParameter", schema=BoulderIDParameter)
    spec.components.schema("BoulderNameParameter", schema=BoulderNameParameter)
    spec.components.schema("AuthenticationRequestBody",
                           schema=AuthenticationRequestBody)
    spec.components.schema("AuthenticationResponseBody",
                           schema=AuthenticationResponseBody)
    spec.components.schema("AuthenticationErrorResponse",
                           schema=AuthenticationErrorResponse)
    spec.components.schema("SignUpRequestBody", schema=SignUpRequestBody)
    spec.components.schema("SignUpResponseBody", schema=SignUpResponseBody)
    spec.components.schema("SignUpErrorResponse", schema=SignUpErrorResponse)
    spec.components.schema("TestTokenResponseBody",
                           schema=TestTokenResponseBody)
    spec.components.schema("TestTokenErrorResponse",
                           schema=TestTokenErrorResponse)
    spec.components.schema("TicklistBoulder",
                           schema=TicklistBoulder)
    spec.components.schema("TicklistErrorResponse",
                           schema=TicklistErrorResponse)
    spec.components.schema("TicklistResponseBody",
                           schema=TicklistResponseBody)
    spec.components.schema("RateBoulderRequestBody",
                           schema=RateBoulderRequestBody)
    spec.components.schema("RateBoulderResponseBody",
                           schema=RateBoulderResponseBody)
    spec.components.schema("RateBoulderErrorResponse",
                           schema=RateBoulderErrorResponse)
    with app.test_request_context():
        spec.path(view=get_gyms)
        spec.path(view=get_gym_walls)
        spec.path(view=get_gym_pretty_name)
        spec.path(view=get_gym_wall_name)
        spec.path(view=get_gym_boulders)
        spec.path(view=get_boulder_by_id)
        spec.path(view=get_boulder_by_name)
        spec.path(view=boulder_create)
        spec.path(view=new_user)
        spec.path(view=get_auth_token)
        spec.path(view=get_resource)
        spec.path(view=get_user_ticklist)
        spec.path(view=rate_boulder)
    with open('./static/swagger/swagger.json', 'w') as f:
        json.dump(spec.to_dict(), f)
