class SunsukuError(Exception):
    '''Base exception class for Sunsuku errors.'''


class InvalidProviderError(SunsukuError):
    '''raised when invalid model provider'''

