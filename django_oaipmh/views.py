'''
Views used to render OAI-PMH response XML.
'''

from inflection import underscore
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.sites.shortcuts import get_current_site

from django_oaipmh.exceptions import OAIPMHException, BadVerb

class OAIProvider(TemplateView):
    content_type = 'text/xml'
    http_method_names = ['get', 'post']
    template_name = 'django_oaipmh/base.xml'
    repository_name = 'My OAI-PMH Repository'
    admin_emails = (email for name, email in settings.ADMINS)
    deleted_record = 'no'
    granularity = 'YYYY-MM-DDThh:mm:ssZ'

    OAI_VERBS = [
        'Identify',
        'GetRecord',
        'ListIdentifiers',
        'ListMetadataFormats',
        'ListRecords',
        'ListSets'
    ]

    DELETED_RECORD_STRATEGIES = ['no', 'transient', 'persistent']

    GRANULARITIES = ['YYYY-MM-DD', 'YYYY-MM-DDThh:mm:ssZ']

    def __init__(self, *args, **kwargs):
        '''Call :meth:`validate_config()` and initialize the view.'''
        self.validate_config()
        super().__init__(*args, **kwargs)


    def validate_config(self):
        '''Check that the provider configuration is valid.'''
        if self.deleted_record not in self.DELETED_RECORD_STRATEGIES:
            raise OAIPMHException('Invalid value for deleted_record.')
        if self.granularity not in self.GRANULARITIES:
            raise OAIPMHException('Invalid value for granularity.')
        return True


    def dispatch(self, request, *args, **kwargs):
        '''Call :meth:`get()` or :meth:`post()` & handle errors with
        :meth:`error()`.'''
        # save request for use in other functions
        self.request = request
        # request URL is needed for every response
        self.url = self.request.build_absolute_uri(self.request.path)
        # create context to pass to handlers to modify
        self.context = {'url': self.url}
        # handle errors
        try:
            return super().dispatch(request, *args, **kwargs)
        except OAIPMHException as error:
            return self.error(error)


    def get(self, request, *args, **kwargs):
        '''Parse GET parameters and send them to :meth:`delegate()`.'''
        verb = request.GET.get('verb', None)
        return self.delegate(verb)


    def post(self, request, *args, **kwargs):
        '''Parse POST parameters and send them to :meth:`delegate()`.'''
        verb = request.POST.get('verb', None)
        return self.delegate(verb)


    def delegate(self, verb):
        '''Determine the verb, add it to the context and pass to the appropriate
        handler.'''
        if verb is None:
            raise BadVerb('Verb is required.')
        if verb not in self.OAI_VERBS:
            raise BadVerb('Invalid verb.')
        # add the verb to the context
        self.context.update({'verb': verb})
        # convert CamelCase verb name to underscore method name and call it
        return getattr(self, underscore(verb))()


    def error(self, error):
        self.template_name = 'django_oaipmh/error.xml'
        self.context.update({
            'code': error.code,
            'message': str(error)
        })
        return self.render_to_response(self.context)


    def get_queryset(self):
        return []


    def identify(self):
        # TODO there are also <description> containers which can live here.
        # TODO support for compression algorithms:
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding
        self.template_name = 'django_oaipmh/identify.xml'
        self.context.update({
            'repositoryName': self.repository_name,
            'baseUrl': self.url,
            'adminEmails': self.admin_emails,
            'earliestDatestamp': None, #TODO derive from queryset
            'deletedRecord': self.deleted_record,
            'granularity': self.granularity
        })
        return self.render_to_response(self.context)


    def list_identifiers(self):
        self.template_name = 'django_oaipmh/list_identifiers.xml'
        return self.render_to_response(self.context)

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

    def get_record(self):
        raise NotImplementedError

    def list_metadata_formats(self):
        raise NotImplementedError

    def list_records(self):
        raise NotImplementedError

    def list_sets(self):
        raise NotImplementedError
