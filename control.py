from flask import Response, request, jsonify
from flask_restful import Resource

from main import work_session

from models import *
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import json
from werkzeug.security import generate_password_hash, check_password_hash
from main import *
from sqlalchemy.ext.declarative import DeclarativeMeta


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
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class SignUpUser(Resource):
    def post(self):
        data = request.json
        try:
            user = User(data["username"], data["password"])
            if session.query(User).filter(User.email == user.email).all() \
                    and session.query(User).filter(User.username == user.username).all():
                return Response(
                    response=json.dumps({"message": "user already created"}),
                    status=405,
                    mimetype="application/json"
                )
            user.password = generate_password_hash(data["password"])
            session.add(user)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "wrong input"}),
                status=404,
                mimetype="application/json"
            )
