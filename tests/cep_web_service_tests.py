# coding: utf-8


import unittest
from cep_web_service.app import app


class CepWebServiceTests(unittest.TestCase):

    test_app = None

    @classmethod
    def setUpClass(cls):
        cls.test_app = app.test_client()

    def test_get_zipcode(self):
        response = self.test_app.get("/zipcode", data={'zipcode': 14020260})

        self.assertEquals(response.status_code, 200)

    def test_post_zipcode(self):
        response = CepWebServiceTests.test_app.post("/zipcode", data={"zipcode": 14020260})

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 201)

    def test_post_zipcode_without_data(self):
        response = CepWebServiceTests.test_app.post("/zipcode")

        self.assertEquals(response.content_type, 'application/json')
        self.assertEquals(response.status_code, 400)

    def test_get_zipcodes(self):
        response = CepWebServiceTests.test_app.get('/zipcode', data={'limit': 10})

        self.assertEquals(response.status_code, 200)

    def test_delete_zipcode(self):
        response = CepWebServiceTests.test_app.delete('/zipcode', data={'zipcode': 14020260})

        self.assertEquals(response.status_code, 204)

    def test_delete_zipcode_without_zipcode(self):
        response = CepWebServiceTests.test_app.delete('/zipcode')

        self.assertEquals(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()