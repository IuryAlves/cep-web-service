# coding: utf-8

import json
import unittest

from mock import patch, Mock, call
import six

import fakedata
from cep_web_service.app import app

if six.PY2:
    def decode(string):
        return string
else:
    def decode(string):
        return string.decode()


class CepWebServiceTests(unittest.TestCase):

    def setUp(self):
        self.test_app = app.test_client()

    @patch('postmon.endereco')
    @patch('cep_web_service.app.app.info_logger.info')
    @patch('cep_web_service.app.zipcode.models.Zipcode.save_document')
    def test_post_zip_code(self, save_document, logger, endereco):
        endereco.return_value = fakedata.fake_endereco()
        cep = endereco.return_value.cep
        logradouro = endereco.return_value.logradouro
        bairro = endereco.return_value.bairro
        cidade_nome = endereco.return_value.cidade.nome
        estado_nome = endereco.return_value.estado.nome

        zip_code = 14020260
        response = self.test_app.post("/zipcode/", data={"zip_code": zip_code})

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 201)

        # mock assertions
        logger.assert_called_with(six.u("Document created with data"
                                  " cep: {cep},"
                                  " logradouro: {logradouro},"
                                  " bairro: {bairro},"
                                  " cidade: {cidade},"
                                  " estado: {estado}").format(cep=cep, logradouro=logradouro,
                                                             bairro=bairro, cidade=cidade_nome,
                                                             estado=estado_nome))

        endereco.assert_called_once_with(zip_code)
        save_document.assert_called_once_with(cep, logradouro, bairro, cidade_nome, estado_nome)

    @patch('postmon.endereco')
    @patch('cep_web_service.app.app.info_logger.info')
    @patch('cep_web_service.app.zipcode.models.Zipcode.save_document')
    def test_post_update_zip_code(self, save_document, logger, endereco):
        endereco.return_value = fakedata.fake_endereco()
        cep = endereco.return_value.cep
        logradouro = endereco.return_value.logradouro
        bairro = endereco.return_value.bairro
        cidade_nome = endereco.return_value.cidade.nome
        estado_nome = endereco.return_value.estado.nome
        save_document.return_value = False

        zip_code = 14020260
        response = self.test_app.post("/zipcode/", data={"zip_code": zip_code})

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 200)

        # mock assertions
        logger.assert_called_with(six.u("Document with cep {cep} has been updated with"
                                  " logradouro: {logradouro},"
                                  " bairro: {bairro},"
                                  " cidade: {cidade},"
                                  " estado: {estado}").format(cep=cep, logradouro=logradouro,
                                                             bairro=bairro, cidade=cidade_nome,
                                                             estado=estado_nome))
        endereco.assert_called_once_with(zip_code)
        save_document.assert_called_once_with(cep, logradouro, bairro, cidade_nome, estado_nome)

    def test_post_zip_code_without_data(self):
        response = self.test_app.post("/zipcode/")

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 400)

    @patch('postmon.endereco')
    @patch('cep_web_service.app.app.error_logger.error')
    def test_post_zip_code_invalid(self, logger, endereco):
        endereco.return_value = None
        zip_code = 1402260
        response = self.test_app.post("/zipcode/", data={'zip_code': zip_code})

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 404)
        endereco.assert_called_with(zip_code)
        logger.assert_called_with('Received invalid zip_code: {zip_code}'.format(zip_code=zip_code))

    @patch('cep_web_service.app.app.error_logger.error')
    def test_get_zip_code_without_data(self, logger):
        response = self.test_app.get("/zipcode/")

        self.assertEquals(response.status_code, 400)
        logger.assert_called_with("No limit or zip_code option were found in the request")

    @patch('cep_web_service.app.app.info_logger.info')
    @patch('cep_web_service.app.zipcode.models.Zipcode.get_or_404')
    def test_get_saved_zip_code(self, get_or_404, logger):
        get_or_404.return_value = fakedata.ZipcodeFake(fakedata.fake_endereco)
        zip_code = 14020260
        response = self.test_app.get('/zipcode/%i' % zip_code)

        self.assertEquals(response.status_code, 200)

        response_data_decoded = decode(response.data)

        self.assertEquals(json.loads(response_data_decoded), get_or_404.return_value.to_dict())
        get_or_404.assert_called_with(zip_code=zip_code)
        logger.assert_called_with("Get zip_code: {zip_code}".format(zip_code=zip_code))

    @patch('cep_web_service.app.app.info_logger.info')
    @patch('cep_web_service.app.zipcode.models.Zipcode.limit')
    def test_get_zip_codes(self, limit, logger):
        limit.return_value = fakedata.get_many_zip_codes(how_many=10)

        response = self.test_app.get('/zipcode/', data={'limit': 10})

        self.assertEquals(response.status_code, 200)

        expected = [zipcode.to_dict() for zipcode in limit.return_value]
        response_decoded = decode(response.data)
        self.assertEquals(json.loads(response_decoded), expected)
        limit.assert_called_with(10)
        logger.assert_called_with("Listing 10 zip_codes")

    @patch('cep_web_service.app.app.info_logger.info')
    @patch('cep_web_service.app.zipcode.models.Zipcode.limit')
    def test_get_zip_codes_with_a_big_limit(self, limit, logger):
        limit.return_value = fakedata.get_many_zip_codes(5)

        response = self.test_app.get('/zipcode/', data={'limit': 20})

        self.assertEquals(response.status_code, 200)

        expected = [zipcode.to_dict() for zipcode in limit.return_value]
        response_decoded = decode(response.data)
        self.assertEquals(json.loads(response_decoded), expected)
        limit.assert_called_with(20)
        logger.assert_has_calls([
            call("Received option to list 20 zipcodes but only 5 were found"),
            call("Listing 5 zip_codes")
        ])

    @patch('cep_web_service.app.app.info_logger.info')
    @patch('cep_web_service.app.zipcode.models.Zipcode.get_or_404')
    def test_delete_zip_code(self, get_or_404, logger):
        zip_code = 14020260
        get_or_404.return_value = Mock(fakedata.ZipcodeFake(fakedata.fake_endereco), spec_set=['delete'])
        response = self.test_app.delete('/zipcode/%i' % zip_code)

        self.assertEquals(response.status_code, 204)
        get_or_404.assert_called_with(zip_code=zip_code)
        get_or_404.return_value.delete.assert_called_with()
        logger.assert_called_with("zip_code: {zip_code} were deleted.".format(zip_code=zip_code))

    @patch('cep_web_service.app.app.error_logger.error')
    def test_delete_zip_code_without_zip_code(self, logger):
        response = self.test_app.delete('/zipcode/')

        self.assertEquals(response.status_code, 400)
        logger.assert_called_with("No zip_code were found in the request.")
