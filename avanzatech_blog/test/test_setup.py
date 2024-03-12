import pytest
from rest_framework.test import APITestCase
from faker import Faker
from rest_framework import status
from test.factories.user.factories import TeamFactory
from factory import SubFactory

fake = Faker()


class TestSetUp(APITestCase):
    
    def setUp(self):
        #definir la ruta del login
        self.login_url = '/user/login/'
        
        #permite realizar una simular un navegador que simula una petición 
        response = self.client.post(
            self.login_url, 
            {
                'username': 'usercommontest@test.com', 
                'password': 'test123456'
            },
            #format = 'json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        return super().setUp()
    
    
    def test_user_login(self):
        pass