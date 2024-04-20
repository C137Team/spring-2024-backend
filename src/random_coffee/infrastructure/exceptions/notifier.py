from .base import InfrastructureError


class NotifierError(InfrastructureError):
    pass


class NotifierBackendError(NotifierError):
    pass
