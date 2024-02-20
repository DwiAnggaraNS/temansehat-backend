from flask_restful import Resource, reqparse
from flaskapp.api.tables import db, users
from flaskapp import bcrypt, mail
from flask_mail import Message

def send_mail(user):
    token = user.get_token ()
    msg = Message(subject="Password Reset Request",
                  recipients =[user.email],
                  sender=("TemanSehat App","temansehatapp@gmail.com"))
    msg.body = f'''
This is your verification token to change your password (Token will expire after 5 minutes):

{token}
'''
    mail.send(msg)


class ForgotPw(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, help="The username is missing")
        self.reqparse.add_argument('email', type=str, help="The email is missing")
        self.reqparse.add_argument('token', type=str, help="The token is missing")
        self.reqparse.add_argument('new_password', type=str, help="The new_password is missing")
        self.reqparse.add_argument('id_in_verify', type=str, help="The id_in_verify is missing")

    def post(self):
        args = self.reqparse.parse_args()
        user = users.query.filter_by(username=args["username"]).first()
        if user:
            if user.email == args["email"]:
                send_mail(user)
                return {"message":"token successfully sent to user's email"}, 200
            else:
                return {"message":"username and email do not match any accounts"}, 401
        else:
            return {"message":"username doesn't belong to any account"}, 404

    def put(self):
        args = self.reqparse.parse_args()
        user = users.query.filter_by(user_id=args["id_in_verify"]).first()
        if user:
            user.password = bcrypt.generate_password_hash(args['new_password']).decode('utf-8')
            db.session.commit()
            return {"message":"password updated successfully"}, 200
        else:
            return {"message":"Account not exist"}, 404
