'''
Exception subclasses specific to OAI-PMH.
http://www.openarchives.org/OAI/openarchivesprotocol.html#ErrorConditions
'''

class OaiPmhException(Exception):
    pass


class BadArgument(OaiPmhException):
    code = 'badArgument'
    message = '''
    The request includes illegal arguments, is missing required arguments, 
    includes a repeated argument, or values for arguments have an illegal 
    syntax.
    '''


class BadResumptionToken(OaiPmhException):
    code = 'badResumptionToken'
    message = 'The value of the resumptionToken argument is invalid or expired.'


class BadVerb(OaiPmhException):
    code = 'badVerb'
    message = '''
    Value of the verb argument is not a legal OAI-PMH verb, the verb
    argument is missing, or the verb argument is repeated.
    '''


class CannotDisseminateFormat(OaiPmhException):
    code = 'cannotDisseminateFormat'
    message = '''
    The metadata format identified by the value given for the metadataPrefix
    argument is not supported by the item or by the repository.
    '''


class IdDoesNotExist(OaiPmhException):
    code = 'idDoesNotExist'
    message = '''
    The value of the identifier argument is unknown or illegal in this 
    repository.
    '''


class NoRecordsMatch(OaiPmhException):
    code = 'noRecordsMatch'
    message = '''
    The combination of the values of the from, until, set and metadataPrefix 
    arguments results in an empty list.
    '''


class NoMetadataFormats(OaiPmhException):
    code = 'noMetadataFormats'
    message = 'There are no metadata formats available for the specified item.'


class NoSetHierarchy(OaiPmhException):
    code = 'noSetHierarchy'
    message = 'The repository does not support sets.'





