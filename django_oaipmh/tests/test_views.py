from django.test import TestCase, Client
from django.urls import reverse

from django_oaipmh.views import OAIProvider

class TestOAIProvider(TestCase):

    def setUp(self):
        self.url = reverse('oai')
        # set a host because it needs to appear in XML response
        self.client = Client(HTTP_HOST='example.com')

    def test_allowed_http_methods(self):
        # GET and POST are allowed HTTP methods
        allowed_methods = ['get', 'post']
        for method in allowed_methods:
            response = getattr(self.client, method)(self.url)
            assert response.status_code == 200

    def test_not_allowed_http_methods(self):
        # Other methods should raise Method Not Allowed (405)
        not_allowed_methods = ['put', 'patch', 'delete', 'head', 'options', 'trace']
        for method in not_allowed_methods:
            response = getattr(self.client, method)(self.url)
            assert response.status_code == 405
    
    def test_content_type(self):
        # Should return XML
        response = self.client.get(self.url)
        assert response['Content-Type'] == 'text/xml'

    def test_identify(self):
        # Should return info about the repository
        response = self.client.get(self.url, {'verb': 'Identify'})
        self.assertTemplateUsed(response, 'django_oaipmh/identify.xml')
        # self.assertContains(response, )

    def test_list_identifiers(self):
        with self.assertRaises(NotImplementedError):
            self.client.get(self.url, {'verb': 'ListIdentifiers'})

    def test_get_record(self):
        with self.assertRaises(NotImplementedError):
            self.client.get(self.url, {'verb': 'GetRecord'})

    def test_list_metadata_formats(self):
        with self.assertRaises(NotImplementedError):
            self.client.get(self.url, {'verb': 'ListMetadataFormats'})

    def test_list_records(self):
        with self.assertRaises(NotImplementedError):
            self.client.get(self.url, {'verb': 'ListRecords'})

    def test_list_sets(self):
        with self.assertRaises(NotImplementedError):
            self.client.get(self.url, {'verb': 'ListSets'})
    

