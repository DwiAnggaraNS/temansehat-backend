from flask_restful import Resource, reqparse
from flaskapp.api.tables import db, mood
import json
from flask_jwt_extended import jwt_required
from datetime import datetime
from flask import Response
from sqlalchemy import desc  # Import the desc function
import secrets

class Mood(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=str, help="The user_id is missing")
        self.reqparse.add_argument('feeling', type=str, help="The feeling is missing")
        self.reqparse.add_argument('story', type=str, help="The story is missing")

    @jwt_required()
    def post(self):
        args = self.reqparse.parse_args()

        db.session.add(
            mood(
                mood_id = secrets.token_hex(12),
                user_id = args['user_id'],
                feeling = args['feeling'],
                story = args['story'],
                date = f"{datetime.now():%y-%m-%d %H:%M}"
            )
        )

        try:
            db.session.commit()
            return {'message': 'Mood uploaded successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
        
    @jwt_required()
    def get(self, user_id=None):
        
        try:
            # Query moods and order by datetime descending
            moods = mood.query.filter(mood.user_id == user_id).order_by(desc(mood.date)).all()

            # Create a dictionary to store user mood information
            moods_users_dict = {}

            # Populate the dictionary with mood information
            for i in moods:
                user_mood_info = {
                    "feeling": i.feeling,
                    "story": i.story,
                    "mood_date": str(i.date)
                }
                moods_users_dict[str(i.mood_id)] = user_mood_info

            # Return the response as JSON
            return moods_users_dict

        except Exception as e:
            # Handle exceptions (e.g., log the error)
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')

