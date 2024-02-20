from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
import base64
import json
import time
with open('flaskapp/config.json') as config_file:
    config = json.load(config_file)

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(25), primary_key=True)
    username = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    pfp = db.Column(db.LargeBinary)

    def get_token(self):
        serializer = URLSafeTimedSerializer(config.get("SECRET_KEY"))
        token = serializer.dumps({"user_id": self.user_id, "timestamp": int(time.time())}, )
        encoded_token = base64.urlsafe_b64encode(token.encode("utf-8")).decode("utf-8")

        return encoded_token

    @staticmethod
    def verify_token(token):
        padding_length = len(token) % 4
        if padding_length != 0:
            token += "=" * (4 - padding_length)

        # Decode the base64-encoded token
        decoded_token = base64.urlsafe_b64decode(token).decode("utf-8")
        serializer = URLSafeTimedSerializer(config.get("SECRET_KEY"))
        try:
            data = serializer.loads(decoded_token, max_age = 500)  # max_age set to 300 seconds
        except Exception as e:
            print(e)
            return None
        return data["user_id"]

    def __repr__(self):
        return '<User %s>' % self.user_id
    
class mood(db.Model):
    __tablename__ = 'mood'
    mood_id = db.Column(db.String(25), primary_key=True)
    user_id = db.Column(db.String(25), db.ForeignKey('users.user_id'), nullable=False)
    feeling = db.Column(db.String(255), nullable=False)
    story   = db.Column(db.String(355), nullable=False)
    date    = db.Column(db.DateTime, nullable=False)
 
    def __repr__(self):
        return '<Mood %s>' % self.mood_id
    
class posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.String(25), primary_key=True)
    user_id = db.Column(db.String(25), db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    pfp = db.Column(db.LargeBinary)
    title = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text(length='long'), nullable=False)
    total_share = db.Column(db.Integer, default=0)
    date_post = db.Column(db.DateTime, nullable=False)
    total_like = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post %s>' % self.post_id

class comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.String(25), primary_key=True)
    post_id = db.Column(db.String(25), db.ForeignKey('posts.post_id'), nullable=False)
    user_id = db.Column(db.String(25), db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    comment_desc = db.Column(db.Text(length='long'), nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Comment %s>' % self.comment_id
    
class image(db.Model):

    __tablename__ = 'image'
    image_id = db.Column(db.String(25), primary_key=True)
    user_id = db.Column(db.String(25), db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.String(25), db.ForeignKey('posts.post_id'), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return '<image %s>' % self.image_id
    