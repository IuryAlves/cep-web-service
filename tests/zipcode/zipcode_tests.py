# coding: utf-8

import unittest
from app import app


class CepWebServiceTests(unittest.TestCase):

    def setUp(self):
        self.test_app = app.test_client()

    def test_get_zip_code(self):
        response = self.test_app.get("/zipcode", data={'zip_code': 14020260})

        self.assertEquals(response.status_code, 200)

    def test_post_zip_code(self):
        response = self.test_app.post("/zipcode", data={"zip_code": 14020260})

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 201)

    def test_post_zip_code_without_data(self):
        response = self.test_app.post("/zipcode")

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 400)

    def test_get_zip_codes(self):
        response = self.test_app.get('/zipcode', data={'limit': 10})

        self.assertEquals(response.status_code, 200)

    def test_delete_zip_code(self):
        response = self.test_app.delete('/zipcode', data={'zip_code': 14020260})

        self.assertEquals(response.status_code, 204)

    def test_delete_zip_code_without_zip_code(self):
        response = self.test_app.delete('/zipcode')

        self.assertEquals(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
