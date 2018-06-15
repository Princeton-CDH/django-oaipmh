"""
Exception subclasses specific to OAI-PMH.
http://www.openarchives.org/OAI/openarchivesprotocol.html#ErrorConditions
"""

class OAIPMHException(Exception):
    message = 'The OAI-PMH repository encountered an error.'

    def __init__(self, message=None):
        if message:
            self.message = message

    def __str__(self):
        return self.message


class BadArgument(OAIPMHException):
    code = 'badArgument'
    message = """
    The request includes illegal arguments, is missing required arguments, 
    includes a repeated argument, or values for arguments have an illegal 
    syntax.
    """


class BadResumptionToken(OAIPMHException):
    code = 'badResumptionToken'
    message = 'The value of the resumptionToken argument is invalid or expired.'


class BadVerb(OAIPMHException):
    code = 'badVerb'
    message = """
    Value of the verb argument is not a legal OAI-PMH verb, the verb
    argument is missing, or the verb argument is repeated.
    """


class CannotDisseminateFormat(OAIPMHException):
    code = 'cannotDisseminateFormat'
    message = """
    The metadata format identified by the value given for the metadataPrefix
    argument is not supported by the item or by the repository.
    """


class IDDoesNotExist(OAIPMHException):
    code = 'idDoesNotExist'
    message = """
    The value of the identifier argument is unknown or illegal in this 
    repository.
    """


class NoRecordsMatch(OAIPMHException):
    code = 'noRecordsMatch'
    
    message = """
    The combination of the values of the from, until, set and metadataPrefix 
    arguments results in an empty list.
    """


class NoMetadataFormats(OAIPMHException):
    code = 'noMetadataFormats'
    message = 'There are no metadata formats available for the specified item.'


class NoSetHierarchy(OAIPMHException):
    code = 'noSetHierarchy'
    message = 'The repository does not support sets.'
