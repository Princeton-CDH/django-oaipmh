"""
Views used to render OAI-PMH response XML.
"""

from inflection import underscore
from django.conf import settings
from django.views.generic.base import TemplateView

from django_oaipmh.exceptions import OAIPMHException, BadVerb, BadArgument
from django_oaipmh.models import OAIItem

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
        """Call :meth:`validate_config()` and initialize the view."""
        self.validate_config()
        super().__init__(*args, **kwargs)


    def validate_config(self):
        """Check that the provider configuration is valid."""
        if self.deleted_record not in self.DELETED_RECORD_STRATEGIES:
            raise OAIPMHException('Invalid value for deleted_record.')
        if self.granularity not in self.GRANULARITIES:
            raise OAIPMHException('Invalid value for granularity.')
        return True


    def dispatch(self, request, *args, **kwargs):
        """Call :meth:`get()` or :meth:`post()` & handle errors with
        :meth:`error()`."""
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
        """Parse GET parameters and send them to :meth:`delegate()`."""
        verb = request.GET.get('verb', None)
        self.params = request.GET
        return self.delegate(verb)


    def post(self, request, *args, **kwargs):
        """Parse POST parameters and send them to :meth:`delegate()`."""
        verb = request.POST.get('verb', None)
        self.params = request.POST
        return self.delegate(verb)


    def delegate(self, verb):
        """Determine the verb, add it to the context and pass to the appropriate
        handler."""
        if verb is None:
            raise BadVerb('Verb is required.')
        if verb not in self.OAI_VERBS:
            raise BadVerb('Invalid verb.')
        # add the verb to the context
        self.context.update({'verb': verb})
        # convert CamelCase verb name to underscore method name and call it
        return getattr(self, underscore(verb))()


    def error(self, error):
        self.context.update({
            'error': {
                'code': error.code,
                'message': str(error)
            }
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
        # TODO handle if we got a resumption token
        resumption_token = self.params.get('resumptionToken', None)
        if resumption_token:
            pass
        # add other params to context
        from_str = self.params.get('from', None)
        until_str = self.params.get('until', None)
        metadata_prefix = self.params.get('metadataPrefix', None)
        set_spec = self.params.get('set', None)
        self.context.update({
            'from': from_str,
            'until': until_str,
            'metadataPrefix': metadata_prefix,
            'set': set_spec
        })
        # check that we got a metadataPrefix
        if not metadata_prefix:
            raise BadArgument('Metadata prefix is required.')
        items = OAIItem.objects.filter(from_str=from_str,
                                       until_str=until_str,
                                       metadata_prefix=metadata_prefix,
                                       set=set_spec)
        self.context.update({ 'items':items })
        return self.render_to_response(self.context)
        # TODO paginate if necessary

    def get_record(self):
        self.template_name = 'django_oaipmh/get_record.xml'
        # check that we got an identifier and a metadataPrefix
        identifier = self.params.get('identifier', None)
        metadata_prefix = self.params.get('metadataPrefix', None)
        # we need them in context even if there's an error
        self.context.update({
            'identifier': identifier,
            'metadataPrefix': metadata_prefix
        })
        # throw the appropriate error
        if not identifier:
            raise BadArgument('OAI identifier is required.')
        if not metadata_prefix:
            raise BadArgument('Metadata prefix is required.')
        # try to find the item
        item = OAIItem.objects.get(identifier)
        # try to retrieve the item's record
        record = item.get_oai_record(metadata_prefix)
        # update the context and render the response
        self.context.update({
            'item': item,
            'metadata': record.serialize(pretty=True).decode()
        })
        return self.render_to_response(self.context)


    def list_metadata_formats(self):
        raise NotImplementedError

    def list_records(self):
        raise NotImplementedError

    def list_sets(self):
        raise NotImplementedError
