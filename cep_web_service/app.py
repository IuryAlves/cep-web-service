# coding: utf-8


from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)



class ZipcodeResource(Resource):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('zipcode', required=True)
        args = parser.parse_args(strict=True)

        return [], 201

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', default=1)
        args = parser.parse_args(strict=True)

        return [], 200


api.add_resource(ZipcodeResource, '/zipcode')

if __name__ == '__main__':
    app.run(debug=True)