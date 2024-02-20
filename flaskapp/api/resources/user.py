from flaskapp.api.tables import db, users
from flask_restful import Resource, reqparse
import secrets
from flaskapp import bcrypt
import base64
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=str ,help='User_id required')
        self.reqparse.add_argument('username', type=str, help='Username required')
        self.reqparse.add_argument('email', type=str, help='Email required')
        self.reqparse.add_argument('password', type=str, help='Password required')
        self.reqparse.add_argument('new_password', type=str, help="The new_password is missing")
        self.reqparse.add_argument('pfp', help='Base64 encoded image data')
        self.reqparse.add_argument('bio', help='Base64 encoded image data')
        super(User, self).__init__()

    #Creating new account
    def post(self):
        args = self.reqparse.parse_args()

        # Check if username already exist in db
        user_exists = users.query.filter_by(username=args['username']).first()

        if user_exists:
            return {'message': 'Username already exists'}, 404
        else:
            new_user = users(
                user_id=secrets.token_hex(12),
                username=args['username'],
                bio=args['bio'],
                email=args['email'],
                password=bcrypt.generate_password_hash(args['password']).decode('utf-8')
            )

            db.session.add(new_user)

            try:
                db.session.commit()
                return {'message': 'User created successfully'}, 201
            except IntegrityError as e:
                db.session.rollback()  # Mengembalikan perubahan karena terjadi kesalahan
                return {'message': 'Email already exists. Choose a different email address.'}, 409
            except Exception as e:
                db.session.rollback()
                return {'error': str(e)}, 500

    #Getting account information
    @jwt_required()   
    def get(self, user_id=None):
        
        user = users.query.filter_by(user_id=user_id).first()
        if not user:
            return {"message": f"{user_id} doesn't exist"}, 404
        else:
            user_data = {
                "username": user.username,
                "bio":user.bio,
                "email": user.email,
                "pfp": base64.b64encode(user.pfp).decode('utf-8') if user.pfp else None
            }
            return user_data, 200

    #Updating account's information
    @jwt_required()   
    def put(self):
        try:
            args = self.reqparse.parse_args()

            user = users.query.filter_by(user_id = args['user_id']).first()

            if user:
                if args['username']:
                    user.username = args['username']
                if args['email']:
                    user.email = args['email']
                if args['bio']:
                    user.bio = args['bio']
                if args['pfp']:
                    image_binary = base64.b64decode(args['pfp'])
                    user.pfp = image_binary

                if args['new_password']:
                    if args['password'] and bcrypt.check_password_hash(user.password, args['password']):
                        user.password = bcrypt.generate_password_hash(args['new_password']).decode('utf-8')
                    else:
                        return {'message': 'Invalid password'}, 401

                db.session.commit()
                return {'message': 'Updating user information succeed'}, 200
            else:
                return {'message': 'User not found'}, 404
        except IntegrityError as e:
            db.session.rollback()  # Mengembalikan perubahan karena terjadi kesalahan
            return {'message': 'Email already exists. Choose a different email address.'}, 409
        except BadRequest as e:
            return {'message': str(e.description)}, e.code
        
    #Deleting an account
    @jwt_required()
    def delete(self):
        args = self.reqparse.parse_args()

        user = users.query.filter_by(user_id=args['user_id'])
        if user:
            user.delete()
            db.session.commit()
            return {"Message": "User succesfully deleted"}, 200
        else:
            return {"Message": "User not found"}, 404