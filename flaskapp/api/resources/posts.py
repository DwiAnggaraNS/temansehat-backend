import base64
from datetime import datetime
import secrets
from flask_restful import Resource, reqparse
from flaskapp.api.tables import db, posts, image, users
from sqlalchemy import desc
from flaskapp.api.resources.comment import Comments
from flaskapp.api.resources.image import Image
from flask_jwt_extended import jwt_required


class Posts(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=str,  required=False,help='User ID is required')
        self.reqparse.add_argument('post_id', type=str,  required=False,help='User ID is required')
        self.reqparse.add_argument('title', type=str,  required=False,help='Title is required')
        self.reqparse.add_argument('desc', type=str, required=False, help='Description is required')
        self.reqparse.add_argument('pictures', type=list, location='json', required=False,help ='List of pictures is required')
    
    @jwt_required()
    def post(self):
        args = self.reqparse.parse_args()
        user = users.query.filter_by(user_id=args["user_id"]).first()

        if user:
            # Create a new post
            new_post = posts(
                post_id=secrets.token_hex(12),
                user_id=args['user_id'],
                username=user.username,
                pfp=user.pfp,
                title=args['title'],
                desc=args['desc'],
                date_post=f"{datetime.now():%y-%m-%d %H:%M}"
            )
            db.session.add(new_post)
            db.session.commit()

            # Check if pictures are provided
            if args['pictures']:
                # Save images associated with the post
                for picture_data in args['pictures']:
                    image_binary = base64.b64decode(picture_data)
                    new_image = image(
                        image_id = secrets.token_hex(12),
                        user_id=args['user_id'],
                        post_id=new_post.post_id,
                        image_data=image_binary
                    )
                    db.session.add(new_image)
                    db.session.commit()
                return {'message': 'Post created successfully'}, 200
            return {'message': 'Post created successfully'}, 201
        else:
            return {"user not found"}, 404

    @jwt_required()
    def put(self):
        args = self.reqparse.parse_args()
        post = posts.query.filter_by(post_id=args['post_id']).first()
            
        if post:
            if args['title']:
                post.title = args['title']
            if args['desc']:
                post.desc = args['desc']
            db.session.commit()
            return {'message': 'Updating post information succeed'}, 200
        else:
            return {'message': 'Post not found'}, 404
        
    @jwt_required()
    def get(self, user_id=None):
        try:

            if user_id is None:
                post_list = posts.query.order_by(desc(posts.date_post)).all()
            else:
                post_list = posts.query.filter(posts.user_id == user_id).order_by(desc(posts.date_post)).all()

            posts_users_dict = {}
            comment = Comments()
            image = Image()

            for post in post_list:
                user_post_info = {
                    "username": post.username,
                    "user_pfp": base64.b64encode(post.pfp).decode('utf-8') if post.pfp else None,
                    "post_date": str(post.date_post),
                    "title": post.title,
                    "desc": post.desc,
                    "images": image.get(post_id=post.post_id),
                    "comments": comment.get(post_id=post.post_id),
                    "total_share": post.total_share,
                    "total_like": post.total_like,
                }
                posts_users_dict[str(post.post_id)] = user_post_info

            return posts_users_dict

        except Exception as e:
            # Handle exceptions (e.g., log the error)
            return {"error": str(e)}, 500


    @jwt_required()
    def delete(self):
        args = self.reqparse.parse_args()
        post = posts.query.filter_by(post_id=args['post_id'])

        if post:
            post.delete()
            db.session.commit()
            return {"Message": "Post succesfully deleted"}, 200
        else:
            return {"Message": "Post not found"}, 404
