# coding: utf-8
from __future__ import absolute_import

import six
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
import postmon

from cep_web_service.app import app
from cep_web_service.app.constants import NULL
from .models import Zipcode

zipcode_blueprint = Blueprint('api', __name__)
api = Api(zipcode_blueprint)


class ZipcodeResource(Resource):

    def __init__(self, *args, **kwargs):
        self.postmon = kwargs['postmon']

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('zip_code', required=True, type=six.text_type)
        args = parser.parse_args(strict=True)
        zip_code = args.get("zip_code")

        result = self.postmon.endereco(zip_code)
        if result is None:
            app.error_logger.error('Received invalid zip_code: {zip_code}'.format(zip_code=zip_code))
            abort(422, message="zip code {zip_code} is invalid".format(zip_code=zip_code))

        cep = result.cep
        logradouro = result.logradouro
        bairro = result.bairro
        cidade_nome = result.cidade.nome
        estado_nome = result.estado.nome

        created = Zipcode.save_document(cep, logradouro, bairro, cidade_nome, estado_nome)
        if created:
            message = six.u("Document created with data"
                            " cep: {cep},"
                            " logradouro: {logradouro},"
                            " bairro: {bairro},"
                            " cidade: {cidade},"
                            " estado: {estado}").format(cep=cep,
                                                        logradouro=logradouro if logradouro is not None else NULL,
                                                        bairro=bairro if logradouro is not None else NULL,
                                                        cidade=cidade_nome,
                                                        estado=estado_nome)
            app.info_logger.info(message)
        else:
            message = six.u("Document with cep {cep} has been updated with"
                            " logradouro: {logradouro},"
                            " bairro: {bairro},"
                            " cidade: {cidade},"
                            " estado: {estado}").format(cep=cep,
                                                        logradouro=logradouro,
                                                        bairro=bairro,
                                                        cidade=cidade_nome,
                                                        estado=estado_nome)
            app.info_logger.info(message)
        return None, 201

    def get(self, zip_code=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        args = parser.parse_args(strict=True)

        limit = args.get('limit')
        if limit is not None:
            zip_codes = Zipcode.limit(limit)
            zip_codes_len = len(zip_codes)
            if zip_codes_len < limit:
                app.info_logger.info("Received option to list {limit}"
                                     " zipcodes but only {quantity} were found".format(limit=limit,
                                                                                       quantity=zip_codes_len))
            app.info_logger.info("Listing {quantity} zip_codes".format(quantity=zip_codes_len))
            return [zip_code.to_dict() for zip_code in zip_codes], 200
        elif zip_code is not None:
            zip_code_document = Zipcode.get_or_404(zip_code=zip_code,
                                                   message="zip code {zip_code} not found.".format(zip_code=zip_code))
            app.info_logger.info("Get zip_code: {zip_code}".format(zip_code=zip_code))
            return zip_code_document.to_dict(), 200
        app.error_logger.error("No limit or zip_code option were found in the request")
        abort(400, message="You must provide the limit or zip_code.")

    def delete(self, zip_code=None):
        if zip_code is None:
            app.error_logger.error("No zip_code were found in the request.")
            abort(400, messsage="You must provide a zip_code.")
        zip_code_document = Zipcode.get_or_404(zip_code=zip_code,
                                               message="zip code {zip_code} not found.".format(zip_code=zip_code))
        zip_code_document.delete()
        app.info_logger.info("zip_code: {zip_code} were deleted.".format(zip_code=zip_code))
        return None, 204

api.add_resource(
    ZipcodeResource,
    '/zipcode/',
    '/zipcode/<string:zip_code>',
    resource_class_kwargs={'postmon': postmon})
