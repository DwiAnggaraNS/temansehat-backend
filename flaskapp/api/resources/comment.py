from flask_restful import Resource, reqparse
from flaskapp.api.tables import db, posts, users, comment
import json
from sqlalchemy import desc
from datetime import datetime
from flask import Response
import secrets
from flask_jwt_extended import jwt_required


class Comments(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('post_id', type=str, help="The post_id is missing")
        self.reqparse.add_argument('user_id', type=str, help="The user_id is missing")
        self.reqparse.add_argument('comment_desc', type=str, help="The comment_desc is missing")
        self.reqparse.add_argument('comment_id', type=str, help="The comment_id is missing")

    @jwt_required()
    def post(self):
        args = self.reqparse.parse_args()

        post = posts.query.filter_by(post_id=args["post_id"]).first()
        user = users.query.filter_by(user_id=args["user_id"]).first()
        if post and user :
            db.session.add(
                comment(
                    comment_id = secrets.token_hex(12),
                    post_id = post.post_id,
                    user_id = user.user_id,
                    username = user.username,
                    comment_desc = args['comment_desc'],
                    comment_date = f"{datetime.now():%y-%m-%d %H:%M}"
                )
            )
            db.session.commit()
            return {'message': 'comment uploaded successfully'}, 200
        else:
            return {'message': 'post or user not found'}, 404

    # @jwt_required()
    def get(self, post_id = None):

        try:
            # post_list = posts.query.filter(posts.user_id == user_id).order_by(desc(posts.date_post)).all()
            # Query moods and order by datetime descending
            comments = comment.query.filter(comment.post_id == post_id).order_by(desc(comment.comment_date)).all()

            # Create a dictionary to store user mood information
            comments_users_dict = {}
            if comments:
                # Populate the dictionary with mood information
                for i in comments:
                    post_comment_info = {
                        "username": i.username,
                        "comment_desc": i.comment_desc,
                        "comment_date": str(i.comment_date)
                    }
                    comments_users_dict[str(i.comment_id)] = post_comment_info

                # Return the response as JSON
                return comments_users_dict
            else:
                return None

        except Exception as e:
            # Handle exceptions (e.g., log the error)
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


    @jwt_required()
    def delete(self):

        args = self.reqparse.parse_args()

        comment_obj = comment.query.filter_by(comment_id=args['comment_id'])
        if comment_obj:
            comment_obj.delete()
            db.session.commit()
            return {"Message": "Comment succesfully deleted"}, 200
        else:
            return {"Message": "Comment not found"}, 404