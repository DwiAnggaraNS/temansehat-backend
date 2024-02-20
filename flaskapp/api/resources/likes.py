from flask_restful import Resource, reqparse
from flaskapp.api.tables import db, posts, users
from flask_jwt_extended import jwt_required

class Likes(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('post_id', type=str, help="The post_id is missing")
        self.reqparse.add_argument('user_id', type=str, help="The user_id is missing")
        self.reqparse.add_argument('like', type=bool, help="The likes is missing")

    @jwt_required()
    def post(self):
        args = self.reqparse.parse_args()

        post = posts.query.filter_by(post_id=args["post_id"]).first()
        user = users.query.filter_by(user_id=args["user_id"]).first()

        if user and post:
            if args['like'] == True:
                post.total_like += 1
            elif args["like"] == False:
                if post.total_like > 0:
                    post.total_like -= 1
        try:
            db.session.commit()
            return {'message': 'post successfully liked/unliked'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500