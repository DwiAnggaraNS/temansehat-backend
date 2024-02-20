from flask import Blueprint
from flask_restful import Api


back = Blueprint('api', __name__)



api = Api(back)

from flaskapp.api.resources.user import User
from flaskapp.api.resources.login import Login
from flaskapp.api.resources.forgotpw import ForgotPw
from flaskapp.api.resources.mood import Mood
from flaskapp.api.resources.posts import Posts
from flaskapp.api.resources.likes import Likes
from flaskapp.api.resources.shares import Shares
from flaskapp.api.resources.comment import Comments
from flaskapp.api.resources.image import Image
from flaskapp.api.resources.sendtoken import SendToken



api.add_resource(Login, '/api/users/login')
api.add_resource(ForgotPw, '/api/users/forgotpw')
api.add_resource(SendToken, '/api/users/forgotpw/sendtoken')
api.add_resource(User, '/api/users', '/api/users/<user_id>')
api.add_resource(Mood, '/api/users/moods', "/api/users/moods/<user_id>")
api.add_resource(Posts, '/api/users/posts', '/api/users/posts/<user_id>')
api.add_resource(Likes, '/api/users/posts/likes')
api.add_resource(Shares, '/api/users/posts/shares')
api.add_resource(Comments, '/api/users/posts/comments', '/api/users/posts/comments/<post_id>')
api.add_resource(Image, '/api/users/posts/images', '/api/users/posts/images/<post_id>')
