from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import base64

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if isinstance(data, bytes):
                        # Convert BLOB to Base64
                        fields[field] = base64.b64encode(data).decode('utf-8')
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)
