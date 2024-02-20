from flask_restful import Resource, reqparse
from flask import Response
import base64
from flaskapp.api.tables import image
import json

class Image(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('post_id', type=str, help="The post_id is missing")

    def get(self, post_id = None):

        try:
            # Query moods and order by datetime descending
            images = image.query.filter(image.post_id == post_id).all()

            # Create a dictionary to store user mood information
            images_users_dict = {}
            if images:
                # Populate the dictionary with mood information
                for i in images:
                    post_image_info = {
                        "image": base64.b64encode(i.image_data).decode('utf-8') if i.image_data else None,
                    }
                    images_users_dict[str(i.image_id)] = post_image_info

                # Return the response as JSON
                return images_users_dict
            else:
                return None
        except Exception as e:
            # Handle exceptions (e.g., log the error)
            return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')