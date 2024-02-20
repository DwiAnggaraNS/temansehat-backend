from flask_restful import Resource, reqparse
from flaskapp.api.tables import users
from flaskapp import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

class Login(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, help="The username is missing")
        self.reqparse.add_argument('password', type=str, help="The password is missing")
        self.reqparse.add_argument('remember', type=bool,help="The remember is missing")
    
    def post(self):
        args = self.reqparse.parse_args()
        user = users.query.filter_by(username=args["username"]).first()
        
        if user:

            if bcrypt.check_password_hash(user.password, args['password']):
                if args['remember'] == True:
                    access_token = create_access_token(identity=str(user.user_id))
                    return {"access_token": access_token, "user_id":user.user_id}, 201
                elif args['remember'] == False:
                    access_token = create_access_token(identity=str(user.user_id))
                    return {"access_token": access_token, "user_id":user.user_id}, 200
            else:
                return {"message": "Incorrect password"}, 401
        else:
            return {"message": "Invalid username"}, 404