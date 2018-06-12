from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from django_oaipmh.views import OAIProvider
from django_oaipmh.exceptions import OAIPMHException

class TestOAIProvider(TestCase):

    def setUp(self):
        self.url = reverse('oai')
        self.factory = RequestFactory()
        self.allowed_methods = ['get', 'post']
        self.not_allowed_methods = ['put', 'patch', 'delete', 'head', 'options',
                                    'trace']


    def test_validate_config(self):
        # Default implementation of OAIProvider should validate
        class TestProvider(OAIProvider):
            pass
        assert TestProvider().validate_config() is True
        # Known valid deletedRecord strategies should validate
        for strategy in OAIProvider.DELETED_RECORD_STRATEGIES:
            provider = TestProvider()
            provider.deleted_record = strategy
            assert provider.validate_config() is True
        # Known valid granularities should validate
        for granularity in OAIProvider.GRANULARITIES:
            provider = TestProvider()
            provider.granularity = granularity
            assert provider.validate_config() is True
        # Implementation with an invalid deletedRecord strategy should fail
        provider = TestProvider()
        provider.deleted_record = 'fake'
        with self.assertRaises(OAIPMHException):
            provider.validate_config()
        # Implementation with an invalid granularity should fail
        provider = TestProvider()
        provider.granularity = 'fake'
        with self.assertRaises(OAIPMHException):
            provider.validate_config()


    def test_http_methods(self):
        # GET and POST are allowed HTTP methods
        for method in self.allowed_methods:
            response = getattr(self.client, method)(self.url)
            assert response.status_code == 200
        # Other methods should raise Method Not Allowed (405)
        for method in self.not_allowed_methods:
            response = getattr(self.client, method)(self.url)
            assert response.status_code == 405


    def test_content_type(self):
        # Should return XML
        response = self.client.get(self.url)
        assert response['Content-Type'] == 'text/xml'


    def test_identify(self):
        # Test that the default implementation renders identify.xml
        response = self.client.get(self.url, {'verb': 'Identify'})
        self.assertTemplateUsed(response, 'django_oaipmh/identify.xml')
        # Create an implementation with some customized values
        class TestProvider(OAIProvider):
            repository_name = 'Test Repository'
            admin_emails = ['me@example.com', 'you@example.com']
            deleted_record = 'transient'
            granularity = 'YYYY-MM-DD'
        # Fake an identify request
        provider = TestProvider()
        request = self.factory.get(self.url, {'verb': 'Identify'})
        provider.request = request
        provider.context = {}
        response = provider.identify()
        # Should include the chosen values for an identify request
        self.assertContains(response, TestProvider.repository_name)
        self.assertContains(response, TestProvider.admin_emails[0])
        self.assertContains(response, TestProvider.admin_emails[1])
        self.assertContains(response, TestProvider.deleted_record)
        self.assertContains(response, TestProvider.granularity)


    def test_list_identifiers(self):
    # Test that the default implementation renders list_identifiers.xml
        response = self.client.get(self.url, {'verb': 'ListIdentifiers'})
        self.assertTemplateUsed(response, 'django_oaipmh/list_identifiers.xml')


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
