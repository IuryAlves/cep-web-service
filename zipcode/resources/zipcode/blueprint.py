# coding: utf-8


from flask import Blueprint
from flask_restful import Api, Resource, reqparse

zipcode_blueprint = Blueprint('api', __name__)
api = Api(zipcode_blueprint)


class ZipcodeResource(Resource):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('zip_code', required=True)
        args = parser.parse_args(strict=True)

        return [], 201

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit')
        parser.add_argument('zip_code')
        args = parser.parse_args(strict=True)

        limit = args.get('limit')
        zipcode = args.get('zip_code')
        if limit is not None:
            pass
            # list zipcodes
        elif zipcode is not None:
            pass
            # get zipcode

        return [], 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('zip_code', required=True)
        args = parser.parse_args(strict=True)

        return [], 204

api.add_resource(ZipcodeResource, '/zipcode')
