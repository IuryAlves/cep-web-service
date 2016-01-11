# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
import postmon

from cep_web_service.app import app
from .models import Zipcode

zipcode_blueprint = Blueprint('api', __name__)
api = Api(zipcode_blueprint)


class ZipcodeResource(Resource):

    def __init__(self, *args, **kwargs):
        self.postmon = kwargs['postmon']

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('zip_code', required=True, type=int)
        args = parser.parse_args(strict=True)
        zip_code = args.get("zip_code")

        result = self.postmon.endereco(zip_code)
        if result is None:
            app.error_logger.error('Received invalid zip_code: {zip_code}'.format(zip_code=zip_code))
            abort(404, message="zip code {zip_code} invalid".format(zip_code=zip_code))

        cep = result.cep
        logradouro = result.logradouro
        bairro = result.bairro
        cidade_nome = result.cidade.nome
        estado_nome = result.estado.nome

        created = Zipcode.save_document(
            cep,
            logradouro,
            bairro,
            cidade_nome,
            estado_nome
        )

        if created:
            app.info_logger.info("Document created with data"
                                 " cep: {cep},"
                                 " logradouro: {logradouro},"
                                 " bairro: {bairro},"
                                 " cidade: {cidade},"
                                 " estado: {estado}".format(cep=cep,
                                                            logradouro=logradouro,
                                                            bairro=bairro,
                                                            cidade=cidade_nome,
                                                            estado=estado_nome))
            return None, 201

        app.info_logger.info("Document with cep {cep} has been updated with"
                             " logradouro: {logradouro},"
                             " bairro: {bairro},"
                             " cidade: {cidade},"
                             " estado: {estado}".format(cep=cep,
                                                        logradouro=logradouro,
                                                        bairro=bairro,
                                                        cidade=cidade_nome,
                                                        estado=estado_nome))
        return None, 200

    def get(self, zip_code=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        args = parser.parse_args(strict=True)

        limit = args.get('limit')
        if limit is not None:
            zip_codes = Zipcode.limit(limit)
            return [zip_code.to_dict() for zip_code in zip_codes], 200
        elif zip_code is not None:
            zip_code_document = Zipcode.get_or_404(zip_code=zip_code)
            return zip_code_document.to_dict(), 200
        abort(400, message="You must provide the limit or zipcode.")

    def delete(self, zip_code=None):
        if zip_code is None:
            abort(400, messsage="You must pass pass a zip_code")
        zip_code_document = Zipcode.get_or_404(zip_code=zip_code)
        zip_code_document.delete()
        return None, 204

api.add_resource(
    ZipcodeResource,
    '/zipcode/',
    '/zipcode/<int:zip_code>',
    resource_class_kwargs={'postmon': postmon})
