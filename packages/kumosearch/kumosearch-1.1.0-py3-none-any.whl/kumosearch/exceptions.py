class KumosearchClientError(IOError):
    def __init__(self, *args, **kwargs):
        super(KumosearchClientError, self).__init__(*args, **kwargs)


class ConfigError(KumosearchClientError):
    pass


class Timeout(KumosearchClientError):
    pass


class RequestMalformed(KumosearchClientError):
    pass


class RequestUnauthorized(KumosearchClientError):
    pass


class RequestForbidden(KumosearchClientError):
    pass


class ObjectNotFound(KumosearchClientError):
    pass


class ObjectAlreadyExists(KumosearchClientError):
    pass


class ObjectUnprocessable(KumosearchClientError):
    pass


class ServerError(KumosearchClientError):
    pass


class ServiceUnavailable(KumosearchClientError):
    pass


class HTTPStatus0Error(KumosearchClientError):
    pass


class InvalidParameter(KumosearchClientError):
    pass
