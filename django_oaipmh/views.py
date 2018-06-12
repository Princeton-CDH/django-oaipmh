'''
Views used to render OAI-PMH response XML.
'''

from inflection import underscore
from django.conf import settings
from django.views.generic.base import TemplateView

from django_oaipmh import exceptions as OaiPmhExceptions

class OAIProvider(TemplateView):
    content_type = 'text/xml'
    http_method_names = ['get', 'post']
    template_name = 'django_oaipmh/base.xml'

    OAI_VERBS = [
        'Identify',
        'GetRecord',
        'ListIdentifiers',
        'ListMetadataFormats',
        'ListRecords',
        'ListSets'
    ]

    def dispatch(self, request, *args, **kwargs):
        '''Call :meth:`get()` or :meth:`post()` & handle errors with :meth:`error()`.'''
        try:
            return super().dispatch(request, *args, **kwargs)
        except OaiPmhExceptions.OaiPmhException as error:
            return self.error(request, error)

    def get(self, request, *args, **kwargs):
        '''Parse GET parameters and send them to :meth:`delegate()`.'''
        request.verb = request.GET.get('verb', None)
        return self.delegate(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        '''Parse POST parameters and send them to :meth:`delegate()`.'''
        request.verb = request.POST.get('verb', None)
        return self.delegate(request, *args, **kwargs)   

    def delegate(self, request, *args, **kwargs):
        '''Determine the OAI-PMH verb and pass to the appropriate handler.'''
        if request.verb is None:
            raise OaiPmhExceptions.BadVerb('Verb is required.')
        if request.verb not in self.OAI_VERBS:
            raise OaiPmhExceptions.BadVerb('Invalid verb.')
        return getattr(self, underscore(request.verb))(request, *args, **kwargs)

    def error(self, request, error):
        self.template_name = 'django_oaipmh/error.xml'
        url = request.scheme + '://' + request.META['HTTP_HOST'] + request.path
        context = {
            'code': error.code,
            'message': str(error),
            'verb': request.verb,
            'url': url
        }
        return self.render_to_response(context)

    def get_queryset(self):
        # list/generator/queryset of items to be made available via oai
        # NOTE: this will probably have other optional parameters,
        # e.g. filter by set or date modified
        # - could possibly include find by id for GetRecord here also...
        pass

    def identify(self, request):
        self.template_name = 'django_oaipmh/identify.xml'
        # TODO: these should probably be class variables/configurations
        # that extending classes could set
        identify_data = {
            'name': 'oai repo name',
            # perhaps an oai_admins method with default logic settings.admins?
            'admins': (email for name, email in settings.ADMINS),
            'earliest_date': '1990-02-01T12:00:00Z',   # placeholder
            # should probably be a class variable/configuration
            'deleted': 'no',  # no, transient, persistent (?)
            # class-level variable/configuration (may affect templates also)
            'granularity': 'YYYY-MM-DDThh:mm:ssZ',  # or YYYY-MM-DD
            # class-level config?
            'compression': 'deflate',  # gzip?  - optional
            # description - optional
            # (place-holder values from OAI docs example)
            'identifier_scheme': 'oai',
            'repository_identifier': 'lcoa1.loc.gov',
            'identifier_delimiter': ':',
            'sample_identifier': 'oai:lcoa1.loc.gov:loc.music/musdi.002'
        }
        return self.render_to_response(identify_data)

    def list_identifiers(self, request):
        raise NotImplementedError
        # self.template_name = 'django_oaipmh/list_identifiers.xml'
        # items = []
        # # TODO: eventually we will need pagination with oai resumption tokens
        # # should be able to model similar to django.contrib.sitemap
        # for i in self.items():
        #     item_info = {
        #         'identifier': self.oai_identifier(i),
        #         'last_modified': self.last_modified(i),
        #         'sets': self.sets(i)
        #     }
        #     items.append(item_info)
        # return self.render_to_response({'items': items})

    def get_record(self, request):
        raise NotImplementedError

    def list_metadata_formats(self, request):
        raise NotImplementedError

    def list_records(self, request):
        raise NotImplementedError

    def list_sets(self, request):
        raise NotImplementedError
