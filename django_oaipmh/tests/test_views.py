from django.test import TestCase
from django.urls import reverse

from django_oaipmh.views import OAIProvider

class TestOAIProvider(TestCase):

    def test_allowed_http_methods(self):
        url = reverse('oai')
        allowed_methods = ['get', 'post']
        not_allowed_methods = ['put', 'patch', 'delete', 'head', 'options', 'trace']
        # GET and POST are allowed HTTP methods
        for method in allowed_methods:
            response = getattr(self.client, method)(url)
            assert response.status_code == 200
        # Other methods should raise Method Not Allowed (405)
        for method in not_allowed_methods:
            response = getattr(self.client, method)(url)
            assert response.status_code == 405