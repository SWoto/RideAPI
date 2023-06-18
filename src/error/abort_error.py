
class BaseAbortError():
    DEFAULT_ERROR_SERVER = 'The request cannot be carried out by the server'

    def __init__(self, http_code, internal_code, message=DEFAULT_ERROR_SERVER) -> None:
        self.internal_code=internal_code
        self.http_code=http_code
        self.message=message

    def abort_parameters(self):
        return self.http_code, {'internal_code':self.internal_code,'message': self.message}