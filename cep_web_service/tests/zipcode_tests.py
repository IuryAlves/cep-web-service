# coding: utf-8

import json
import unittest

from mock import patch
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
    @patch('cep_web_service.app.zipcode.models.Zipcode.save_document')
    def test_post_zip_code(self, save_document, endereco):
        endereco.return_value = fakedata.fake_endereco()
        zip_code = 14020260
        response = self.test_app.post("/zipcode/", data={"zip_code": zip_code})

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 201)

        # mock assertions
        endereco.assert_called_once_with(zip_code)
        save_document.assert_called_once_with(
            endereco.return_value.cep,
            endereco.return_value.logradouro,
            endereco.return_value.bairro,
            endereco.return_value.cidade.nome,
            endereco.return_value.estado.nome
        )

    def test_post_zip_code_without_data(self):
        response = self.test_app.post("/zipcode/")

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 400)

    @patch('postmon.endereco')
    def test_post_zip_code_invalid(self, endereco):
        endereco.return_value = None
        zip_code = 1402260
        response = self.test_app.post("/zipcode/", data={'zip_code': zip_code})

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 404)
        endereco.assert_called_with(zip_code)

    @patch('cep_web_service.app.zipcode.models.Zipcode.get_or_404')
    def test_get_saved_zip_code(self, get_or_404):
        get_or_404.return_value = fakedata.ZipcodeFake(fakedata.fake_endereco)
        zip_code = 14020260
        response = self.test_app.get('/zipcode/%i' % zip_code)

        self.assertEquals(response.status_code, 200)

        response_data_decoded = decode(response.data)

        self.assertEquals(json.loads(response_data_decoded), get_or_404.return_value.to_dict())
        get_or_404.assert_called_with(zip_code=zip_code)

    @patch('cep_web_service.app.zipcode.models.Zipcode.limit')
    def test_get_zip_codes(self, objects_query_set):
        objects_query_set.return_value = fakedata.get_many_zip_codes()

        response = self.test_app.get('/zipcode/', data={'limit': 10})

        self.assertEquals(response.status_code, 200)

        expected = [zipcode.to_dict() for zipcode in objects_query_set.return_value]
        response_decoded = decode(response.data)
        self.assertEquals(json.loads(response_decoded), expected)

    def test_delete_zip_code(self):
        response = self.test_app.delete('/zipcode/', data={'zip_code': 14020260})

        self.assertEquals(response.status_code, 204)

    def test_delete_zip_code_without_zip_code(self):
        response = self.test_app.delete('/zipcode/')

        self.assertEquals(response.status_code, 400)
