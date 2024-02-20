from flask_restful import Resource, reqparse
from flaskapp.api.tables import users

class SendToken(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, help="The token is missing")

    def post(self):
        args = self.reqparse.parse_args()
        verify = users.verify_token(args["token"])
        if verify == None:
            return {"message": "invalid or expired token"}
        else:
            return {"user_id": verify}, 200